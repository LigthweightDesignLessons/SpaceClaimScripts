# Python Script, API Version = V17
from random import *

# Parameters
radius = 10
spacing = 5
tol_rad = 1
tol_dist = 2
width = 100
length = 100


# helpers
distance = radius *2 + spacing
n_width = int(width/distance) +2
n_length = int(length/distance) +2
n_total = n_length*n_width

def unit(number):
    return UM(number)

def modify(toleranz):
    return (random()*2 -1) * toleranz

def draw_sym_rect(width, length):
    # Sketch Rectangle
    point1 = Point2D.Create(unit(-width/2),unit(-length/2))
    point2 = Point2D.Create(unit(width/2),unit(-length/2))
    point3 = Point2D.Create(unit(width/2),unit(length/2))
    result = SketchRectangle.Create(point1, point2, point3)
    # EndBlock


# Clear Up
selection = Selection.SelectAll()
result = Delete.Execute(selection)
# EndBlock

# Objekte löschen
selection = Selection.Create(GetRootPart().Components)
result = Delete.Execute(selection)
# EndBlock


# rename Root into "RVE"
root = Selection.Create(GetRootPart())
result = RenameObject.Execute(root,"RVE")
# EndBlock

# Create Fiber
result = ComponentHelper.CreateNewComponent(root, None)
fiber = Selection.CreateByNames("Komponente1")
result = RenameObject.Execute(fiber,"Fiber")
# EndBlock

# Create Matrix
result = ComponentHelper.CreateNewComponent(root, None)
matrix = Selection.CreateByNames("Komponente1")
result = RenameObject.Execute(matrix,"Matrix")
# EndBlock

fiber = Selection.Create(GetRootPart().Components[0])
matrix = Selection.Create(GetRootPart().Components[1])



# Teil aktivieren: Fiber
result = ComponentHelper.SetActive (fiber, None)
# EndBlock

# Set Sketch Plane
sectionPlane = Plane.PlaneZX
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Sketch Circle
for i in range(n_width):
    xi = -width/2 + (i - 0.5) * distance
    for j in range(n_length):
        yj = -length/2 + (j - 0.5) * distance
        x = xi + modify(tol_dist)
        y = yj + modify(tol_dist)
        r = radius + modify(tol_rad)
        origin = Point2D.Create(unit(x), unit(y))
        result = SketchCircle.Create(origin, unit(r))

draw_sym_rect(width, length)

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

height = unit(10)

##########################################

square_id = 0
for face in GetRootPart().Components[0].Content.Bodies[0].Faces[:]:
    if len(face.Edges[:]) >3:
        break
    else:
        square_id = square_id +1
        

# 1 Fläche strecken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0].Faces[square_id])
options = ExtrudeFaceOptions()
options.Copy = True
options.ExtrudeType = ExtrudeType.Add
result = ExtrudeFaces.Execute(selection, height, options)
# EndBlock


# Rest löschen
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0])
result = Delete.Execute(selection)
# EndBlock


# Set Sketch Plane
sectionPlane = Plane.Create(Frame.Create(Point.Create(0, height, 0), 
    Direction.DirZ, 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

draw_sym_rect(width, length)

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# 1 Fläche strecken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0].Faces[-1])
options = ExtrudeFaceOptions()
options.Copy = True
options.ExtrudeType = ExtrudeType.Cut
result = ExtrudeFaces.Execute(selection, -height, options)
# EndBlock

# Oberfläche verschieben
selections = Selection.Create(GetRootPart().Components[0].Content.Bodies[1])
component = Selection.Create(GetRootPart().Components[1])
result = ComponentHelper.MoveBodiesToComponent(selections, component, False, None)
# EndBlock


# 1 Fläche strecken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0].Faces[0:-1])
options = ExtrudeFaceOptions()
options.Copy = True
options.ExtrudeType = ExtrudeType.Cut
result = ExtrudeFaces.Execute(selection, -height, options)
# EndBlock

# Objekte löschen
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0])
result = Delete.Execute(selection)
# EndBlock

####################################


# Benannte Auswahlgruppe erstellen
primarySelection = Selection.Create(GetRootPart().Components[0].Content.Bodies[:])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Gruppe1", "Fiber")
# EndBlock

# Benannte Auswahlgruppe erstellen
primarySelection = Selection.Create(GetRootPart().Components[1].Content.Bodies[0])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Benannte Auswahl umbenennen
result = NamedSelection.Rename("Gruppe1", "Matrix")
# EndBlock