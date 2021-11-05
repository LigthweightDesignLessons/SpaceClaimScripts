# Python Script, API Version = V18 Beta
from math import *
import sys

complete = False
ClearAll()

seat_tube_angle = DEG(72)
seat_tube_center_length = MM(402)
seat_tube_length = MM(503)
seat_tupe_diameter = MM(40)

top_tupe_angle = DEG(8)
eff_top_tupe_length = MM(589)
top_tupe_height = MM(100)

head_tube_angle = DEG(72.5)
head_tube_diameter = MM(40)
head_tube_length = MM(95)

bottom_tupe_height = MM(120)

chain_stay_inner_angle = DEG(60)
chain_stay = MM(410)
chain_bearing_diameter = MM(40)
chain_bearing_thickness = MM(50)

shaft_width = MM(100)
chain_diameter = MM(20)
shaft_bearing_diameter = MM(30)
shaft_bearing_thickness = MM(30)

form_thickness = MM(35)


chain_center =  Point.Create(0, 0, 0)
DatumPointCreator.Create(chain_center)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]),"chain_center")

height = sin(seat_tube_angle) * seat_tube_center_length
width = -cos(seat_tube_angle) * seat_tube_center_length
seat_tupe_center = Point.Create(width, 0, height)
DatumPointCreator.Create(seat_tupe_center)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]),"seat_tupe_center")

height = height + sin(top_tupe_angle) * seat_tube_center_length
width = width + eff_top_tupe_length
head_tupe_center = Point.Create(width, 0, height)
DatumPointCreator.Create(head_tupe_center)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]),"head_tupe_center")

angle = seat_tube_angle - chain_stay_inner_angle
height = sin(angle) * chain_stay
width = -cos(angle) * chain_stay

shaft_center_left = Point.Create(width, -shaft_width/2, height)
DatumPointCreator.Create(shaft_center_left)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]), "shaft_center_left")

shaft_center_right = Point.Create(width, shaft_width/2, height)
DatumPointCreator.Create(shaft_center_right)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]), "shaft_center_right")

back_center = Point.Create(width, 0, height)
DatumPointCreator.Create(back_center)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]), "back_center")


width = eff_top_tupe_length
front_center = Point.Create(width, 0, height)
DatumPointCreator.Create(front_center)
RenameObject.Execute( Selection.Create(GetRootPart().DatumPoints[-1]), "front_center")


def creat_rectangle(width, height):
    p1 = Point2D.Create(-height/2, width/2)
    p2 = Point2D.Create(height/2, width/2)
    p3 = Point2D.Create(height/2, -width/2)
    SketchRectangle.Create(p1, p2, p3)

def create_cicle(diameter):
    SketchCircle.Create(Point2D.Create(0, 0) , diameter/2)

# Set Sketch Plane
sectionPlane = Plane.PlaneZX
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

def create_extrusion(start, vector, generator, extrusiontype, extra_length=0, direction=False, symmetric=False):
    length = vector.Magnitude + extra_length
    if direction:
        length = extra_length
    frame = Frame.Create(start, vector.Direction)
    plane = Plane.Create(frame)
    ViewHelper.SetSketchPlane(plane)
    generator()
    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode, None)
    selection = Selection.Create(GetRootPart().Bodies[-1].Faces[:])
    options = ThickenFaceOptions()
    options.PullSymmetric = symmetric
    options.ExtrudeType = extrusiontype#ExtrudeType.Add #ForceIndependent
    result = ThickenFaces.Execute(selection,  vector.Direction, length, options)

def create_beam(start, end, generator, extra_length =0):
    vector = end.Vector - start.Vector
    create_extrusion(start, vector, generator, ExtrudeType.ForceIndependent, extra_length)

create_extrusion(chain_center, Vector.Create(0, 1, 0),
                                lambda : create_cicle(chain_bearing_diameter), 
                                ExtrudeType.ForceIndependent,
                                chain_bearing_thickness/2, direction=True, symmetric=True)

create_extrusion(head_tupe_center, Vector.Create(-cos(head_tube_angle), 0, sin(head_tube_angle)), 
                                lambda : create_cicle(head_tube_diameter), 
                                ExtrudeType.ForceIndependent,
                                head_tube_length/2 + MM(10), direction=True, symmetric=True)

create_extrusion(shaft_center_left, Vector.Create(0, 1, 0), 
                                lambda : create_cicle(shaft_bearing_diameter), 
                                ExtrudeType.ForceIndependent,
                                shaft_bearing_thickness/2, direction=True, symmetric=True)

create_extrusion(shaft_center_right, Vector.Create(0, 1, 0), 
                                lambda : create_cicle(shaft_bearing_diameter), 
                                ExtrudeType.ForceIndependent,
                                shaft_bearing_thickness/2, direction=True, symmetric=True)

create_beam(chain_center, seat_tupe_center, lambda : create_cicle(seat_tupe_diameter), 
                    seat_tube_length - seat_tube_center_length)

# create_beam(chain_center, head_tupe_center, lambda : creat_rectangle(bottom_tupe_width, bottom_tupe_height))
# create_beam(seat_tupe_center, head_tupe_center,  lambda : creat_rectangle(top_tupe_height, top_tupe_width))

def draw_curve(points):
    length = len(points)
    for i in range(length):
        start = points[i]
        end = None
        if i+1 < length:
             end =  points[i+1]
        else:
             end = points[0]
        SketchLine.Create(start, end)

# Form
sectionPlane = Plane.PlaneZX
result = ViewHelper.SetSketchPlane(sectionPlane, None)
points = [0] *4
points[0] = Point2D.Create(chain_center.Z, chain_center.X)
points[1] = Point2D.Create(head_tupe_center.Z - sin(head_tube_angle) * head_tube_length/2,
                                            head_tupe_center.X + cos(head_tube_angle) * head_tube_length/2)
points[2] = Point2D.Create(head_tupe_center.Z + sin(head_tube_angle) * head_tube_length/2,
                                            head_tupe_center.X - cos(head_tube_angle) * head_tube_length/2)
points[3] = Point2D.Create(seat_tupe_center.Z, seat_tupe_center.X)
draw_curve(points)

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# 1 Fläche verstärken
selection = Selection.Create(GetRootPart().Bodies[-1].Faces[:])
options = ThickenFaceOptions()
options.PullSymmetric = True
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ThickenFaces.Execute(selection, Direction.DirY, form_thickness/2, options)
# EndBlock

# 4 Rundungen erstellen
selection = Selection.Create([GetRootPart().Bodies[5].Edges[8],
    GetRootPart().Bodies[5].Edges[5],
    GetRootPart().Bodies[5].Edges[0],
    GetRootPart().Bodies[5].Edges[10]])
options = ConstantRoundOptions()
result = ConstantRound.Execute(selection, MM(10), options, None)
# EndBlock

def trim_bodies(targets, tools):
    length_before = len(GetRootPart().Bodies[:])
    targets = Selection.Create(targets)
    tools = Selection.Create(tools)
    options = MakeSolidsOptions()
    result = Combine.Intersect(targets, tools, options)
    
    length_after = len(GetRootPart().Bodies[:])
    
    diff = length_before - length_after
    if diff < 0:
        selection = Selection.Create(GetRootPart().Bodies[diff:])
        result = Delete.Execute(selection)
        
        
# trim main
length = len(GetRootPart().Bodies[:])
for i in range(4, length):
    trim_bodies(GetRootPart().Bodies[i], GetRootPart().Bodies[:i])

draw = lambda : create_cicle(chain_diameter)
create_beam(chain_center, shaft_center_left, draw)
create_beam(chain_center, shaft_center_right, draw)
create_beam(seat_tupe_center, shaft_center_left, draw)
create_beam(seat_tupe_center, shaft_center_right, draw)


for i in range(length, length+4):
    trim_bodies(GetRootPart().Bodies[i], GetRootPart().Bodies[:length])
    
    
counter = length
for i in range(4):
    selection = Selection.Create(GetRootPart().Bodies[counter])
    SplitBody.ByCutter(selection, Plane.PlaneZX)
    selection = None
    if GetRootPart().Bodies[counter].Shape.Volume > GetRootPart().Bodies[-1].Shape.Volume:
        selection = Selection.Create(GetRootPart().Bodies[-1])
        counter = counter +1
    else:
        selection = Selection.Create(GetRootPart().Bodies[counter])
    result = Combine.RemoveRegions(selection)


# Ursprung erstellen
x_Direction = Direction.DirX
y_Direction = Direction.DirY
result = DatumOriginCreator.Create(back_center, x_Direction, y_Direction, None)
result = DatumOriginCreator.Create(front_center, x_Direction, y_Direction, None)
# EndBlock

RenameObject.Execute( Selection.Create(GetRootPart().CoordinateSystems[0]), "back")
RenameObject.Execute( Selection.Create(GetRootPart().CoordinateSystems[1]), "front")

if not complete:
    sys.exit(0)

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[0].Faces[0]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[1].Faces[0]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[2].Faces[0]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[3].Faces[0]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[4].Faces[2]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create([GetRootPart().Bodies[5].Faces[4],
    GetRootPart().Bodies[5].Faces[5],
    GetRootPart().Bodies[5].Faces[6],
    GetRootPart().Bodies[5].Faces[7],
    GetRootPart().Bodies[5].Faces[8],
    GetRootPart().Bodies[5].Faces[9],
    GetRootPart().Bodies[5].Faces[10],
    GetRootPart().Bodies[5].Faces[11]]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[6].Faces[4]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[7].Faces[2]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[8].Faces[4]))
result = Paste.FromClipboard()
# EndBlock

# Copy to Clipboard
result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[9].Faces[2]))
result = Paste.FromClipboard()
# EndBlock

labels = [ "Chain_Tupe", "Head_Tupe", "Right_Wheel", "Left_Wheel", "Seat_Tupe",  "Form_Right", "Right_Bottom_Tupe", "Right_Top_Tupe",  "Left_Bottom_Tupe", "Left_Top_Tupe", "Form_Left"]

# Objekte löschen
selection = Selection.Create(GetRootPart().Bodies[:len(labels)-1])
result = Delete.Execute(selection)
# EndBlock

# Schneiden
DatumPlaneCreator.Create(Point.Create(0,0,0),Direction.DirY)

selection = Selection.Create(GetRootPart().Bodies[5])
datum = Selection.Create(GetRootPart().DatumPlanes[0])
result = SplitBody.ByCutter(selection, datum)

selection = Selection.Create(GetRootPart().DatumPlanes[0])
result = Delete.Execute(selection)
# EndBlock

for i in range(len(labels)):
    selection = Selection.Create(GetRootPart().Bodies[i])
    result = RenameObject.Execute(selection, labels[i])



for i in range(len(labels)):
    primarySelection = Selection.Create(GetRootPart().Bodies[i])
    secondarySelection = Selection()
    result = NamedSelection.Create(primarySelection, secondarySelection)
    result = NamedSelection.Rename("Gruppe1",  labels[i])

sys.exit(0)

# Bezugslinie erstellen
for i in range(len(labels)):
    if labels[i] == "Form":
        continue
    selection = Selection.Create(GetRootPart().Bodies[i].Faces[0])
    result = DatumLineCreator.Create(selection, False, None)
    primarySelection = Selection.Create(GetRootPart().DatumLines[-1])
    secondarySelection = Selection()
    result = NamedSelection.Create(primarySelection, secondarySelection)
    result = NamedSelection.Rename("Gruppe1",  labels[i]+"_Axis")
    result = RenameObject.Execute(primarySelection, labels[i]+"_Axis")

