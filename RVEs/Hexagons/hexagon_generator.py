# Python Script, API Version = V18 Beta
import math

class ContiniousLine():
    def __init__(self, points):
        self.points = points

    def draw(self):
        for i in range(len(self.points)):
            current = self.points[i]
            next = None
            if i + 1 != len(self.points):
                next = self.points[i + 1]
            else:
                next = self.points[0]
            SketchLine.Create(current, next)


class Hexagon(ContiniousLine):
    def __init__(self, center, line_length, leaver_length, angle, thickness= 0):
        self.start = center
        self.thickness = thickness
        self.line_length = line_length
        self.leaver_length = leaver_length
        self.angle = angle
        self.setup()
        ContiniousLine.__init__(self, self.generate_points())

    def setup(self):
        self.delta_x = leaver_length * math.cos(angle)
        self.delta_y = leaver_length * math.sin(angle)

        self.dist_x = line_length + self.delta_x
        self.dist_y = 2 * self.delta_y

    def set_thickness(self, thickness):
        self.thickness = thickness
        self.points = self.generate_points()


    def generate_points(self):
        points = [0, 1, 2, 3, 4, 5]
        dx = self.thickness / math.sin(self.angle)
        dtop = self.thickness / math.tan(self.angle)

        x = self.start.X - self.line_length / 2 - dx + dtop
        y = self.start.Y + self.delta_y + self.thickness
        points[0] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + dx - dtop
        y = self.start.Y + self.delta_y + self.thickness
        points[1] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + self.delta_x + dx
        y = self.start.Y
        points[2] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + dx - dtop
        y = self.start.Y - self.delta_y - self.thickness
        points[3] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 - dx + dtop
        y = self.start.Y - self.delta_y - self.thickness
        points[4] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 - self.delta_x - dx
        y = self.start.Y
        points[5] = Point2D.Create(x, y)
        return points


class OuterHexagon(Hexagon):
    def __init__(self, center, line_length, leaver_length, angle, thickness=0):
        Hexagon.__init__(self, center, line_length, leaver_length, angle, thickness)

    def generate_points(self):
        points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        dx = self.thickness / math.sin(self.angle)
        dtop = self.thickness / math.tan(self.angle)

        x = self.start.X - self.line_length / 2 - dx - dtop
        y = self.start.Y + self.delta_y - self.thickness
        points[0] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 + dx + dtop
        y = self.start.Y + self.delta_y + self.thickness
        points[1] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 - dx - dtop
        y = self.start.Y + self.delta_y + self.thickness
        points[2] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + dx + dtop
        y = self.start.Y + self.delta_y - self.thickness
        points[3] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + self.delta_x + dx
        y = self.start.Y
        points[4] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 + dx + dtop
        y = self.start.Y - self.delta_y + self.thickness
        points[5] = Point2D.Create(x, y)

        x = self.start.X + self.line_length / 2 - dx - dtop
        y = self.start.Y - self.delta_y - self.thickness
        points[6] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 + dx + dtop
        y = self.start.Y - self.delta_y - self.thickness
        points[7] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 - dx - dtop
        y = self.start.Y - self.delta_y + self.thickness
        points[8] = Point2D.Create(x, y)

        x = self.start.X - self.line_length / 2 - self.delta_x - dx
        y = self.start.Y
        points[9] = Point2D.Create(x, y)
        return points

class HexCoreMaterial():
    def __init__(self, line_length, leaver_length, angle, wall_thickness, height):
        self.wall_thickness = wall_thickness
        self.height = height
        self.line_length = line_length
        self.leaver_length = leaver_length
        self.angle = angle

        self.delta_x = leaver_length * math.cos(angle)
        self.delta_y = leaver_length * math.sin(angle)

        self.dist_x = line_length + self.delta_x
        self.dist_y = 2 * self.delta_y
        self.create_cores()
        self.create_matrix()


    def draw_core(self, start):
        Hexagon(start, self.line_length, self.leaver_length, angle, - wall_thickness / 2).draw()
        if angle <= DEG(90):
            Hexagon(start, self.line_length, self.leaver_length, angle, wall_thickness / 2).draw()
        else:
            OuterHexagon(start, self.line_length, self.leaver_length, angle, wall_thickness / 2).draw()


    def create_core(self, start):
        self.draw_core(start)
        # Solidify Sketch
        mode = InteractionMode.Solid
        result = ViewHelper.SetViewMode(mode, None)
        # EndBlock

        face_id = 0
        max_area = 0
        faces = GetRootPart().Bodies[-1].Faces[:]
        for i in range(len(faces)):
            area = faces[i].Area
            if area > max_area:
                face_id = i
                max_area = area

        # Auswahl löschen
        selection = Selection.Create(GetRootPart().Bodies[-1].Faces[face_id])
        result = Delete.Execute(selection)
        # EndBlock

        # 1 Fläche strecken
        selection = Selection.Create(GetRootPart().Bodies[-1].Faces[:])
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.Cut
        result = ExtrudeFaces.Execute(selection, self.height, options)
        # EndBlock

    def create_cores(self):
        pos = [[-1, 0, 1], [-0.5, 0.5]]
        for i in [-1, 0, 1]:
            for j in pos[i]:
                # Set Sketch Plane
                sectionPlane = Plane.PlaneXY
                result = ViewHelper.SetSketchPlane(sectionPlane, None)
                # EndBlock
                p = Point2D.Create(i * self.dist_x, j * self.dist_y)
                self.create_core(p)

        # Bezugsebene erstellen
        sectionPlane = Plane.PlaneXY
        result = DatumPlaneCreator.Create(sectionPlane)
        # EndBlock

        # Translate Along Z Handle
        selection = Selection.Create(GetRootPart().DatumPlanes[0])
        direction = Direction.DirZ
        options = MoveOptions()
        result = Move.Translate(selection, direction, MM(-1), options)
        # EndBlock

        # Set Sketch Plane
        selection = Selection.Create(GetRootPart().DatumPlanes[0])
        result = ViewHelper.SetSketchPlane(selection, None)
        # EndBlock

        # Sketch Inner Rectangle
        point1 = Point2D.Create(-self.dist_x, self.dist_y)
        point2 = Point2D.Create(self.dist_x, self.dist_y)
        point3 = Point2D.Create(self.dist_x, -self.dist_y)
        result = SketchRectangle.Create(point1, point2, point3)
        # EndBlock

        dx = self.dist_x + self.line_length + self.delta_x + self.wall_thickness / 2
        dy = self.dist_y + self.delta_y + self.wall_thickness / 2
        # Sketch Inner Rectangle
        point1 = Point2D.Create(-dx, dy)
        point2 = Point2D.Create(dx, dy)
        point3 = Point2D.Create(dx, -dy)
        result = SketchRectangle.Create(point1, point2, point3)
        # EndBlock

        # Solidify Sketch
        mode = InteractionMode.Solid
        result = ViewHelper.SetViewMode(mode, None)
        # EndBlock

        # Auswahl löschen
        selection = Selection.Create(GetRootPart().Bodies[1].Faces[0])
        result = Delete.Execute(selection)
        # EndBlock

        # 1 Fläche strecken
        selection = Selection.Create(GetRootPart().Bodies[1].Faces[0])
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.ForceCut
        result = ExtrudeFaces.Execute(selection, self.height + MM(1), options)
        # EndBlock

        # Objekte löschen
        selection = Selection.Create(GetRootPart().DatumPlanes[0])
        result = Delete.Execute(selection)
        # EndBlock

    def create_matrix(self):
        # Set Sketch Plane
        sectionPlane = Plane.PlaneXY
        result = ViewHelper.SetSketchPlane(sectionPlane, None)
        # EndBlock

        # Sketch Inner Rectangle
        point1 = Point2D.Create(-self.dist_x, self.dist_y)
        point2 = Point2D.Create(self.dist_x, self.dist_y)
        point3 = Point2D.Create(self.dist_x, -self.dist_y)
        result = SketchRectangle.Create(point1, point2, point3)
        # EndBlock

        # Solidify Sketch
        mode = InteractionMode.Solid
        result = ViewHelper.SetViewMode(mode, None)
        # EndBlock

        # 7 Flächen strecken
        selection = Selection.Create(GetRootPart().Bodies[1].Faces[:])
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.ForceIndependent
        result = ExtrudeFaces.Execute(selection, self.height, options)
        # EndBlock


#### Hier gehts los ####


wall_thickness = UM(5)
height  = UM(50)
line_length = UM(80)
leaver_length = UM(50)
angle = DEG(120)


ClearAll()

material = HexCoreMaterial(line_length, leaver_length, angle, wall_thickness, height)

# Benannte Auswahlgruppe erstellen
primarySelection = Selection.Create(GetRootPart().Bodies[0])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Benannte Auswahl umbenennen
result = NamedSelection.Rename("Gruppe1", "Core")
# EndBlock

# Benannte Auswahlgruppe erstellen
primarySelection = Selection.Create(GetRootPart().Bodies[1:])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Benannte Auswahl umbenennen
result = NamedSelection.Rename("Gruppe1", "Matrix")
# EndBlock

# 4 Objekte vereinfachen
result = FixExtraEdges.FindAndFix()
# EndBlock