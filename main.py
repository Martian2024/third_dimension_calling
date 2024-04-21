from typing import Union
from math import sin, cos, tan, sqrt, atan, pi, radians, degrees, acos, asin
import pygame
from stl import mesh

def sign(x):
    if x < 0:
        return -1
    return 1

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    '''def scale(self, k):
        self.x *= k
        self.y *= k
        self.z *= k'''

    def __mul__(self, k: Union[int, float]):
        return Vector(self.x * k, self.y * k, self.z * k)
    
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def move(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def __add__(self, vector: Vector):
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)
    
    def __sub__(self, vector: Vector):
        return self + (vector * -1)
    
'''class Edge:
    def __init__(self, point1: Point, point2: Point):
        self.points = [point1, point2]'''

    

class Camera:
    def __init__(self, position: Point, angle_y: Union[int, float], angle_z: Union[int, float], screen, height, width):
        self.position = position
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.vision = 60
        self.plane_side = 2 * tan(radians(self.vision))
        self.width = width  
        self.height = height 
        self.fps = 30
        self.background = 30
        self.screen = screen

    def translate_points(self, points):
        translated_points = []
        translation_vector = Vector(self.position.x, self.position.y, self.position.z)
        for i in points:
            translated_points.append(i - translation_vector)
        return translated_points
    
    def rotate_points_y(self, points): #по часовой стрелке - положительный угол
        rotated_points = []
        for i in points:
            try:
                vector = Vector(i.x, i.y, i.z)
                if atan(vector.z / vector.x) > 0:
                    if vector.x > 0:
                        new_angle = degrees(atan(vector.z / vector.x)) - self.angle_y
                    else:
                        new_angle = -180 + degrees(atan(vector.z / vector.x)) - self.angle_y
                else:
                    if vector.x > 0:
                        new_angle = degrees(atan(vector.z / vector.x)) - self.angle_y
                    else:
                        new_angle = 180 + degrees(atan(vector.z / vector.x)) - self.angle_y
                        #print(90 + -1 * degrees(atan(vector.z / vector.x)) - self.angle_y)
                new_x = sqrt(vector.x ** 2 + vector.z ** 2) * cos(radians(new_angle))
                new_z = sqrt(vector.x ** 2 + vector.z ** 2) * sin(radians(new_angle))
                rotated_points.append(Point(new_x, i.y, new_z))
            except ZeroDivisionError:
                vector = Vector(i.x, i.y, i.z)  
                if vector.z > 0:
                    new_angle = 90 - self.angle_y
                    new_x = sqrt(vector.x ** 2 + vector.z ** 2) * cos(radians(new_angle))
                    new_z = sqrt(vector.x ** 2 + vector.z ** 2) * sin(radians(new_angle))
                elif vector.z < 0:
                    new_angle = -90 - self.angle_y
                    new_x = sqrt(vector.x ** 2 + vector.z ** 2) * cos(radians(new_angle))
                    new_z = sqrt(vector.x ** 2 + vector.z ** 2) * sin(radians(new_angle))
                else:
                    new_z = 0
                    new_x = 0
                rotated_points.append(Point(new_x, i.y, new_z))
            #print(list(map(lambda a: [a.x, a.y, a.z], rotated_points)))
        return rotated_points
    
    def rotate_points_z(self, points): #по часовой стрелке - положительный угол
        rotated_points = []   
        for i in points:
            try:
                vector = Vector(i.x, i.y, i.z)
                if atan(vector.y / vector.x) > 0:
                    if vector.x > 0:
                        new_angle = degrees(atan(vector.y / vector.x)) - self.angle_z
                    else:
                        new_angle = -180 + degrees(atan(vector.y / vector.x)) - self.angle_z
                else:
                    if vector.x > 0:
                        new_angle = degrees(atan(vector.y / vector.x)) - self.angle_z
                    else:
                        new_angle = 180 + degrees(atan(vector.y / vector.x)) - self.angle_z

                '''if vector.x > 0:
                    new_angle = degrees(atan(vector.y / vector.x)) - self.angle_z
                else:
                    new_angle = -1 * (180 - degrees(atan(vector.x / vector.y))) - self.angle_z'''
                new_x = sqrt(vector.x ** 2 + vector.y ** 2) * cos(radians(new_angle))
                new_y = sqrt(vector.x ** 2 + vector.y ** 2) * sin(radians(new_angle))
                rotated_points.append(Point(new_x, new_y, i.z))
            except ZeroDivisionError:
                vector = Vector(i.x, i.y, i.z)
                if vector.y > 0:
                    new_angle = 90 - self.angle_z
                    new_x = sqrt(vector.x ** 2 + vector.y ** 2) * cos(radians(new_angle))
                    new_y = sqrt(vector.x ** 2 + vector.y ** 2) * sin(radians(new_angle))
                elif vector.y < 0:
                    new_angle = -90 - self.angle_z
                    new_x = sqrt(vector.x ** 2 + vector.y ** 2) * cos(radians(new_angle))
                    new_y = sqrt(vector.x ** 2 + vector.y ** 2) * sin(radians(new_angle))
                else:                
                    new_x = 0
                    new_y = 0
                
                rotated_points.append(Point(new_x, new_y, i.z))

        return rotated_points


    def render_points(self, points):
        return_list = []
        points = self.translate_points(points)
        points = self.rotate_points_y(points)
        points = self.rotate_points_z(points)
        for i in points:
            vector = Vector(i.x, i.y, i.z)
            try:
                new_x = asin(vector.z / sqrt(vector.x ** 2 + vector.z ** 2))
                new_y = asin(vector.y / sqrt(vector.x ** 2 + vector.y ** 2))
                return_list.append((new_x, new_y))
                '''if new_x * (self.width / radians(self.vision)) + self.width // 2 > 500:
                    print(i.x, i.y, i.z, new_x, new_y, new_x * (self.width / radians(self.vision)) + self.width // 2)'''
                #print('AAAAAAAAAA', i.x, i.y, i.z, new_x, new_y)
            except ZeroDivisionError:
                if vector.x ** 2 + vector.y ** 2 == 0:
                    if vector.z > 0:
                        new_x = radians(90)
                    elif vector.z < 0:
                        new_x = radians(-90)
                    new_y = 0
                elif vector.x ** 2 + vector.z ** 2 == 0:
                    if vector.y > 0:
                        new_y = radians(90)
                    elif vector.y < 0:
                        new_y = radians(-90)
                    new_x = 0
                return_list.append((new_x, new_y))

        #print(return_list)

        return return_list
    
    '''def render_edges(self, edges):
        return_list = []
        for i in edges:
            return_list.append(self.render_points(i.points))
        return return_list'''
    
    def translate_to_new_basis(self, polygon, intersec_point, v1, v2, o_point):
        v1_args = {'x': v1.x, 'y': v1.y, 'z': v1.z}
        v2_args = {'x': v2.x, 'y': v2.y, 'z': v2.z}
        intersec_point_args = {'x': intersec_point.x, 'y': intersec_point.y, 'z': intersec_point.z}
        o_args = {'x': o_point.x, 'y': o_point.y, 'z': o_point.z}

        if v2.x != 0:
            c2 = 'x'
            if v1.y != 0:
                c1 = 'y'
            else:
                c1 = 'z'
        elif v2.y != 0:
            c2 = 'y'
            if v1.x != 0:
                c1 = 'x'                       #может наебнуться
            else:
                c1 = 'z'
        else:
            c2 = 'z'
            if v1.x != 0:
                c1 = 'x'
            else:
                c1 = 'y'
        
        y = (intersec_point_args[c2] - o_args[c2] - (intersec_point_args[c1] - o_args[c1]) * v1_args[c2] / v1_args[c1]) / (-1 * v2_args[c1] * v1_args[c2] / v1_args[c1] + v2_args[c2])
        x = (intersec_point_args[c1] - o_args[c1] - y * v2_args[c1]) / v1_args[c1]

        return x, y
    
    def getDistance(self, polygon):
        BC = Vector(polygon.points[0].x - polygon.points[1].x, polygon.points[0].y - polygon.points[1].y, polygon.points[0].z - polygon.points[1].z)
        BA = Vector(polygon.points[2].x - polygon.points[1].x, polygon.points[2].y - polygon.points[1].y, polygon.points[2].z - polygon.points[1].z)
        CA = Vector(polygon.points[0].x - polygon.points[2].x, polygon.points[0].y - polygon.points[2].y, polygon.points[0].z - polygon.points[2].z)
        normal = Vector(BA.y * BC.z - BA.z * BC.y, BA.z * BC.x - BA.x * BC.z, BA.x * BC.y - BA.y * BC.x)
        length = abs(normal.x * self.position.x + normal.y * self.position.y + normal.z * self.position.z - (normal.x * polygon.points[1].x + normal.y * polygon.points[1].y + normal.z * polygon.points[1].z)) / sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2)
        normal = normal * (length / sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2))
        antinormal = normal * -1

        

        intersec_point = self.position + normal
        if normal.x * intersec_point.x + normal.y * intersec_point.y + normal.z * intersec_point.z - (normal.x * polygon.points[1].x + normal.y * polygon.points[1].y + normal.z * polygon.points[1].z) != 0:
            intersec_point = self.position + antinormal
        
        #print(normal.x, normal.y, normal.z)
        #print(intersec_point.x, intersec_point.y, intersec_point.z)
            

        #новая проверка на вхождение точки пересечения в треугольник
        DA = Vector(intersec_point.x - polygon.points[0].x, intersec_point.y - polygon.points[0].y, intersec_point.z - polygon.points[0].z)
        DB = Vector(intersec_point.x - polygon.points[1].x, intersec_point.y - polygon.points[1].y, intersec_point.z - polygon.points[1].z)
        DC = Vector(intersec_point.x - polygon.points[2].x, intersec_point.y - polygon.points[2].y, intersec_point.z - polygon.points[2].z)

        s_ABC = Vector(BA.y * BC.z - BA.z * BC.y, BA.z * BC.x - BA.x * BC.z, BA.x * BC.y - BA.y * BC.x).length() / 2
        s_ABD = Vector(DA.y * DB.z - DA.z * DB.y, DA.z * DB.x - DA.x * DB.z, DA.x * DB.y - DA.y * DB.x).length() / 2
        s_BCD = Vector(DB.y * DC.z - DB.z * DC.y, DB.z * DC.x - DB.x * DC.z, DB.x * DC.y - DB.y * DC.x).length() / 2
        s_DCA = Vector(DA.y * DC.z - DA.z * DC.y, DA.z * DC.x - DA.x * DC.z, DA.x * DC.y - DA.y * DC.x).length() / 2

        in_triangle = True
        if s_ABD + s_BCD + s_DCA > s_ABC:
            in_triangle = False


        #вычисление расстояния
        if in_triangle:
            #print('AAA')
            return length
        
        c_BA = self.get_projection(BA, DB)
        
        if c_BA < 0:
            #print('ba1')
            dist_BA = DB.length()
        elif c_BA > 1:
            #print('ba2')
            dist_BA = DA.length()
        else:
            #print('ba3')
            dist_BA = Vector(DA.y * BA.z - DA.z * BA.y, DA.z * BA.x - DA.x * BA.z, DA.x * BA.y - DA.y * BA.x).length() / BA.length()

        c_BC = self.get_projection(BC, DB)
        
        if c_BC < 0:
            #print('bc1')
            dist_BC = DB.length()
        elif c_BC > 1:
            #print('bc2')
            dist_BC = DC.length()
        else:
            #print('bc3')
            dist_BC = Vector(DB.y * BC.z - DB.z * BC.y, DB.z * BC.x - DB.x * BC.z, DB.x * BC.y - DB.y * BC.x).length() / BC.length()

        c_CA = self.get_projection(CA, DC)
        
        if c_CA < 0:
            #print('ca1')
            dist_CA = DC.length()
        elif c_CA > 1:
            #print('ca2')
            dist_CA = DA.length()
        else:
            #print('ca3')
            dist_CA = Vector(DC.y * CA.z - DC.z * CA.y, DC.z * CA.x - DC.x * CA.z, DC.x * CA.y - DC.y * CA.x).length() / CA.length()

        #print([dist_BA, dist_BC, dist_CA])
        #print(length)
        #print(sqrt(min(dist_BA, dist_BC, dist_CA, DA.length(), DB.length(), DC.length()) ** 2 + length ** 2))
    

        return sqrt(min(dist_BA, dist_BC, dist_CA) ** 2 + length ** 2)
    
    def render_polygon(self, polygon):
        points = self.render_points(polygon.points)

        
        
        pos1 = (points[0][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[0][1] * (self.height / radians(self.vision)) + self.height // 2)
        pos2 = (points[1][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[1][1] * (self.height / radians(self.vision)) + self.height // 2)
        pos3 = (points[2][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[2][1] * (self.height / radians(self.vision)) + self.height // 2)
        #print([pos1, pos2, pos3])
        return [max(i * polygon.cos_theta, self.background) for i in polygon.color], [pos1, pos2, pos3]
    
    def get_distance_to_point(self, point):
        return sqrt((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2 + (point.z - self.position.z) ** 2 )
    
    def get_projection(self, v1, v2):
        return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z) / v1.length()
    
    def render_mesh(self, mesh):
        for i in sorted(mesh.polygons, key=lambda x: (self.getDistance(x), self.get_distance_to_point(x.center)), reverse=True):
            if self.get_projection(i.normal, Vector(self.position.x - i.center.x, self.position.y - i.center.y, self.position.z - i.center.z)) > 0: #AAAAAAAA
                pygame.draw.polygon(self.screen, *self.render_polygon(i))

class Polygon:
    def __init__(self, points, color, light_source):
        self.points = points
        midpoint = points[1] + Vector(points[2].x - points[1].x, points[2].y - points[1].y, points[2].z - points[1].z) * (1 / 2)
        self.center = points[0] + Vector(midpoint.x - points[0].x, midpoint.y - points[0].y, midpoint.z - points[0].z) * (2 / 3)
        self.color = color

        BC = Vector(points[0].x - points[1].x, points[0].y - points[1].y, points[0].z - points[1].z)
        BA = Vector(points[2].x - points[1].x, points[2].y - points[1].y, points[2].z - points[1].z)
        self.normal = Vector(BA.y * BC.z - BA.z * BC.y, BA.z * BC.x - BA.x * BC.z, BA.x * BC.y - BA.y * BC.x)
        pointing_vector = Vector(light_source.x - self.center.x, light_source.y - self.center.y, light_source.z - self.center.z)
        self.cos_theta = (pointing_vector.x * self.normal.x + pointing_vector.y * self.normal.y + pointing_vector.z * self.normal.z) / (pointing_vector.length() * self.normal.length())
        
class Mesh():
    def __init__(self, polygons, center=[0, 0, 0]):
        self.polygons = polygons
        self.center = center

    def from_file(filepath, color, lightsource, center=[0, 0, 0]):
        m = mesh.Mesh.from_file(filepath)
        polygons = []
        for i in range(len(m.x)):
            p0 = Point(m.x[i][0], m.z[i][0], m.y[i][0])
            p1 = Point(m.x[i][1], m.z[i][1], m.y[i][1])
            p2 = Point(m.x[i][2], m.z[i][2], m.y[i][2])
            polygon = Polygon([p0, p2, p1], color, lightsource)
            polygons.append(polygon)
        
        return Mesh(polygons, center)


class LightSource(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
    