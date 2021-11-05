# Python Script, API Version = V17
from random import *

# Parameters
radius = 10
spacing = 5
tol_rad = 1
tol_dist = 2
width = 100
length = 150
height = 10


# helpers
distance = radius *2 + spacing
n_width = int(width/distance) +2
n_length = int(length/distance) +2
n_total = n_length*n_width

def modify(toleranz):
    return (random()*2 -1) * toleranz


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


#######################################
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
        origin = Point2D.Create(MM(x), MM(y))
        result = SketchCircle.Create(origin, MM(r))
        
# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock


# 36 Flächen strecken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[0].Faces[0:(n_total+1)])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.Add
result = ExtrudeFaces.Execute(selection, MM(height), options)
# EndBlock

#################
# Cut 1
######################
# Set Sketch Plane
sectionPlane = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Sketch Rectangle
point1 = Point2D.Create(MM(length/2),MM(0))
point2 = Point2D.Create(MM(length/2+2*distance),MM(0))
point3 = Point2D.Create(MM(length/2+2*distance),MM(height))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Sketch Rectangle
point1 = Point2D.Create(MM(-length/2),MM(0))
point2 = Point2D.Create(MM(-length/2-2*distance),MM(0))
point3 = Point2D.Create(MM(-length/2-2*distance),MM(height))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# 2 Flächen verstärken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[-1].Faces[0:2])
options = ThickenFaceOptions()
options.PullSymmetric = True
options.ExtrudeType = ExtrudeType.ForceCut
result = ThickenFaces.Execute(selection, Direction.DirZ, MM(width), options)
# EndBlock

#################
# Cut 2
######################
# Set Sketch Plane
sectionPlane = Plane.PlaneYZ
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Sketch Rectangle
point1 = Point2D.Create(MM(0), MM(width/2))
point2 = Point2D.Create(MM(0), MM(width/2+2*distance))
point3 = Point2D.Create(MM(height), MM(width/2+2*distance))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Sketch Rectangle
point1 = Point2D.Create(MM(0), MM(-width/2))
point2 = Point2D.Create(MM(0), MM(-width/2-2*distance))
point3 = Point2D.Create(MM(height), MM(-width/2-2*distance))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# 2 Flächen verstärken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[-1].Faces[0:2])
options = ThickenFaceOptions()
options.PullSymmetric = True
options.ExtrudeType = ExtrudeType.ForceCut
result = ThickenFaces.Execute(selection, Direction.DirX, MM(78.71), options)
# EndBlock

##################
# Matrix
#################

# Set Sketch Plane
sectionPlane = Plane.PlaneZX
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock
        
# Sketch Rectangle
point1 = Point2D.Create(MM(-width/2),MM(-length/2))
point2 = Point2D.Create(MM(width/2),MM(-length/2))
point3 = Point2D.Create(MM(width/2),MM(length/2))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock       

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# 1 Fläche strecken
selection = Selection.Create(GetRootPart().Components[0].Content.Bodies[-1].Faces[0])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ExtrudeFaces.Execute(selection, MM(height), options)
# EndBlock

# Volumenkörper verschieben
selections = Selection.Create(GetRootPart().Components[0].Content.Bodies[-1])
component = Selection.Create(GetRootPart().Components[1])
result = ComponentHelper.MoveBodiesToComponent(selections, component, False, None)
# EndBlock

#######################