from typing import Union
from math import sin, cos, tan, sqrt, atan, pi, radians, degrees, acos, asin
import pygame
from stl import mesh
import numpy as np

def sign(x):
    if x < 0:
        return -1
    return 1

def get_vector_length(vector):
    return sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

'''class Vector:
    def __init__(self, x, y, z):
        self[0] = x
        self[1] = y
        self[2] = z

    # def scale(self, k):
    #     self[0] *= k
    #     self[1] *= k
    #     self[2] *= k

    def __mul__(self, k: Union[int, float]):
        return np.array([self[0] * k, self[1] * k, self[2] * k)
    
    def length(self):
        return sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)'''


'''class Point:
    def __init__(self, x, y, z):
        self[0] = x
        self[1] = y
        self[2] = z
    
    def move(self, vector):
        self[0] += vector[0]
        self[1] += vector[1]
        self[2] += vector[2]

    def __add__(self, vector: Vector):
        return np.array([self[0] + vector[0], self[1] + vector[1], self[2] + vector[2])
    
    def __sub__(self, vector: Vector):
        return self + (vector * -1)'''
    
'''class Edge:
    def __init__(self, point1: Point, point2: Point):
        self.points = [point1, point2]'''

    

class Camera:
    def __init__(self, position: np.ndarray, angle_y: Union[int, float], angle_z: Union[int, float], screen, height, width):
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
        translation_vector = np.array([self.position[0], self.position[1], self.position[2]])
        for i in points:
            translated_points.append(i - translation_vector)
        return translated_points
    
    def rotate_camera_y(self, points): #по часовой стрелке - положительный угол
        rotated_points = []
        for i in points:
            try:
                vector = np.array([i[0], i[1], i[2]])
                length = sqrt(vector[0] ** 2 + vector[2] ** 2)
                if length != 0:
                    if vector[0] > 0:
                        new_angle = degrees(asin(vector[2] / length)) - self.angle_y
                    else:
                        if vector[2] > 0:
                            new_angle = 180 - degrees(asin(vector[2] / length)) - self.angle_y
                        else:
                            new_angle = -180 - degrees(asin(vector[2] / length)) - self.angle_y
                else:
                    rotated_points.append(vector)
                new_x = sqrt(vector[0] ** 2 + vector[2] ** 2) * cos(radians(new_angle))
                new_z = sqrt(vector[0] ** 2 + vector[2] ** 2) * sin(radians(new_angle))
                rotated_points.append(np.array([new_x, i[1], new_z]))
            except ZeroDivisionError:
                vector = np.array([i[0], i[1], i[2]])  
                print('AAAAAAAAA')
                if vector[2] > 0:
                    new_angle = 90 - self.angle_y
                    new_x = sqrt(vector[0] ** 2 + vector[2] ** 2) * cos(radians(new_angle))
                    new_z = sqrt(vector[0] ** 2 + vector[2] ** 2) * sin(radians(new_angle))
                elif vector[2] < 0:
                    new_angle = -90 - self.angle_y
                    new_x = sqrt(vector[0] ** 2 + vector[2] ** 2) * cos(radians(new_angle))
                    new_z = sqrt(vector[0] ** 2 + vector[2] ** 2) * sin(radians(new_angle))
                else:
                    new_z = 0
                    new_x = 0
                rotated_points.append(np.array([new_x, i[1], new_z]))
            #print(list(map(lambda a: [a[0], a[1], a[2]], rotated_points)))
        return rotated_points
    
    def rotate_camera_z(self, points): #по часовой стрелке - положительный угол
        rotated_points = []   
        for i in points:
            try:
                vector = np.array([i[0], i[1], i[2]])
                length = sqrt(vector[0] ** 2 + vector[1] ** 2)
                if length != 0:
                    if vector[0] > 0:
                        new_angle = degrees(asin(vector[1] / length)) - self.angle_z
                    else:
                        if vector[1] > 0:
                            new_angle = 180 - degrees(asin(vector[1] / length)) - self.angle_z
                        else:
                            new_angle = -180 - degrees(asin(vector[1] / length)) - self.angle_z
                else:
                    rotated_points.append(vector)
                new_x = sqrt(vector[0] ** 2 + vector[1] ** 2) * cos(radians(new_angle))
                new_y = sqrt(vector[0] ** 2 + vector[1] ** 2) * sin(radians(new_angle))
                rotated_points.append(np.array([new_x, new_y, i[2]]))
            except ZeroDivisionError:
                print('AAAAAAA')
                vector = np.array([i[0], i[1], i[2]])
                if vector[1] > 0:
                    new_angle = 90 - self.angle_z
                    new_x = sqrt(vector[0] ** 2 + vector[1] ** 2) * cos(radians(new_angle))
                    new_y = sqrt(vector[0] ** 2 + vector[1] ** 2) * sin(radians(new_angle))
                elif vector[1] < 0:
                    new_angle = -90 - self.angle_z
                    new_x = sqrt(vector[0] ** 2 + vector[1] ** 2) * cos(radians(new_angle))
                    new_y = sqrt(vector[0] ** 2 + vector[1] ** 2) * sin(radians(new_angle))
                else:                
                    new_x = 0
                    new_y = 0
                
                rotated_points.append(np.array([new_x, new_y, i[2]]))

        return rotated_points


    def render_points(self, points):
        return_list = []
        points = self.translate_points(points)
        points = self.rotate_camera_y(points)
        points = self.rotate_camera_z(points)
        for i in points:
            vector = np.array([i[0], i[1], i[2]])
            try:
                new_x = asin(vector[2] / sqrt(vector[0] ** 2 + vector[2] ** 2))
                new_y = asin(vector[1] / sqrt(vector[0] ** 2 + vector[1] ** 2))
                return_list.append((new_x, new_y))
            except ZeroDivisionError:
                if vector[0] ** 2 + vector[1] ** 2 == 0:
                    if vector[2] > 0:
                        new_x = radians(90)
                    elif vector[2] < 0:
                        new_x = radians(-90)
                    new_y = 0
                elif vector[0] ** 2 + vector[2] ** 2 == 0:
                    if vector[1] > 0:
                        new_y = radians(90)
                    elif vector[1] < 0:
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
        v1_args = {'x': v1[0], 'y': v1[1], 'z': v1[2]}
        v2_args = {'x': v2[0], 'y': v2[1], 'z': v2[2]}
        intersec_point_args = {'x': intersec_point[0], 'y': intersec_point[1], 'z': intersec_point[2]}
        o_args = {'x': o_point[0], 'y': o_point[1], 'z': o_point[2]}

        if v2[0] != 0:
            c2 = 'x'
            if v1[1] != 0:
                c1 = 'y'
            else:
                c1 = 'z'
        elif v2[1] != 0:
            c2 = 'y'
            if v1[0] != 0:
                c1 = 'x'                       #может наебнуться
            else:
                c1 = 'z'
        else:
            c2 = 'z'
            if v1[0] != 0:
                c1 = 'x'
            else:
                c1 = 'y'
        
        y = (intersec_point_args[c2] - o_args[c2] - (intersec_point_args[c1] - o_args[c1]) * v1_args[c2] / v1_args[c1]) / (-1 * v2_args[c1] * v1_args[c2] / v1_args[c1] + v2_args[c2])
        x = (intersec_point_args[c1] - o_args[c1] - y * v2_args[c1]) / v1_args[c1]

        return x, y
    
    def getDistance(self, polygon):
        BC = np.array([polygon.points[0][0] - polygon.points[1][0], polygon.points[0][1] - polygon.points[1][1], polygon.points[0][2] - polygon.points[1][2]])
        BA = np.array([polygon.points[2][0] - polygon.points[1][0], polygon.points[2][1] - polygon.points[1][1], polygon.points[2][2] - polygon.points[1][2]])
        CA = np.array([polygon.points[0][0] - polygon.points[2][0], polygon.points[0][1] - polygon.points[2][1], polygon.points[0][2] - polygon.points[2][2]])
        normal = np.array([BA[1] * BC[2] - BA[2] * BC[1], BA[2] * BC[0] - BA[0] * BC[2], BA[0] * BC[1] - BA[1] * BC[0]])
        length = abs(normal[0] * self.position[0] + normal[1] * self.position[1] + normal[2] * self.position[2] - (normal[0] * polygon.points[1][0] + normal[1] * polygon.points[1][1] + normal[2] * polygon.points[1][2])) / sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        normal = normal * (length / sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2))
        antinormal = normal * -1

        

        intersec_point = self.position + normal
        if normal[0] * intersec_point[0] + normal[1] * intersec_point[1] + normal[2] * intersec_point[2] - (normal[0] * polygon.points[1][0] + normal[1] * polygon.points[1][1] + normal[2] * polygon.points[1][2]) != 0:
            intersec_point = self.position + antinormal
        
        #print(normal[0], normal[1], normal[2])
        #print(intersec_point[0], intersec_point[1], intersec_point[2])
            

        #новая проверка на вхождение точки пересечения в треугольник
        DA = np.array([intersec_point[0] - polygon.points[0][0], intersec_point[1] - polygon.points[0][1], intersec_point[2] - polygon.points[0][2]])
        DB = np.array([intersec_point[0] - polygon.points[1][0], intersec_point[1] - polygon.points[1][1], intersec_point[2] - polygon.points[1][2]])
        DC = np.array([intersec_point[0] - polygon.points[2][0], intersec_point[1] - polygon.points[2][1], intersec_point[2] - polygon.points[2][2]])

        s_ABC = get_vector_length(np.array([BA[1] * BC[2] - BA[2] * BC[1], BA[2] * BC[0] - BA[0] * BC[2], BA[0] * BC[1] - BA[1] * BC[0]])) / 2
        s_ABD = get_vector_length(np.array([DA[1] * DB[2] - DA[2] * DB[1], DA[2] * DB[0] - DA[0] * DB[2], DA[0] * DB[1] - DA[1] * DB[0]])) / 2
        s_BCD = get_vector_length(np.array([DB[1] * DC[2] - DB[2] * DC[1], DB[2] * DC[0] - DB[0] * DC[2], DB[0] * DC[1] - DB[1] * DC[0]])) / 2
        s_DCA = get_vector_length(np.array([DA[1] * DC[2] - DA[2] * DC[1], DA[2] * DC[0] - DA[0] * DC[2], DA[0] * DC[1] - DA[1] * DC[0]])) / 2

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
            dist_BA = get_vector_length(DB)
        elif c_BA > 1:
            #print('ba2')
            dist_BA = get_vector_length(DA)
        else:
            #print('ba3')
            dist_BA = get_vector_length(np.array([DA[1] * BA[2] - DA[2] * BA[1], DA[2] * BA[0] - DA[0] * BA[2], DA[0] * BA[1] - DA[1] * BA[0]])) / get_vector_length(BA)

        c_BC = self.get_projection(BC, DB)
        
        if c_BC < 0:
            #print('bc1')
            dist_BC = get_vector_length(DC)
        elif c_BC > 1:
            #print('bc2')
            dist_BC = get_vector_length(DC)
        else:
            #print('bc3')
            dist_BC = get_vector_length(np.array([DB[1] * BC[2] - DB[2] * BC[1], DB[2] * BC[0] - DB[0] * BC[2], DB[0] * BC[1] - DB[1] * BC[0]])) / get_vector_length(BC)

        c_CA = self.get_projection(CA, DC)
        
        if c_CA < 0:
            #print('ca1')
            dist_CA = get_vector_length(DC)
        elif c_CA > 1:
            #print('ca2')
            dist_CA = get_vector_length(DA)
        else:
            #print('ca3')
            dist_CA = get_vector_length(np.array([DC[1] * CA[2] - DC[2] * CA[1], DC[2] * CA[0] - DC[0] * CA[2], DC[0] * CA[1] - DC[1] * CA[0]])) / get_vector_length(CA)

        #print([dist_BA, dist_BC, dist_CA])
        #print(length)
        #print(sqrt(min(dist_BA, dist_BC, dist_CA, DA.length(), DB.length(), DC.length()) ** 2 + length ** 2))
    

        return sqrt(min(dist_BA, dist_BC, dist_CA) ** 2 + length ** 2)
    
    def render_polygon(self, polygon):
        polygon.update()
        points = self.render_points(polygon.points)

        
        
        pos1 = (points[0][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[0][1] * (self.height / radians(self.vision)) + self.height // 2)
        pos2 = (points[1][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[1][1] * (self.height / radians(self.vision)) + self.height // 2)
        pos3 = (points[2][0] * (self.width / radians(self.vision)) + self.width // 2, -1 * points[2][1] * (self.height / radians(self.vision)) + self.height // 2)
        #print([pos1, pos2, pos3])
        return [max(i * polygon.cos_theta, self.background) for i in polygon.color], [pos1, pos2, pos3]
    
    def get_distance_to_point(self, point):
        return sqrt((point[0] - self.position[0]) ** 2 + (point[1] - self.position[1]) ** 2 + (point[2] - self.position[2]) ** 2 )
    
    def get_projection(self, v1, v2):
        return (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / get_vector_length(v1)
    
    def render_mesh(self, mesh):
        for i in sorted(filter(lambda i: self.get_projection(i.normal, np.array([self.position[0] - i.center[0], self.position[1] - i.center[1], self.position[2] - i.center[2]])) > 0, mesh.polygons), key=lambda x: (self.getDistance(x), self.get_distance_to_point(x.center)), reverse=True):
            #pygame.draw.polygon(self.screen, *self.render_polygon(i))
            pygame.draw.polygon(self.screen, *self.render_polygon(i))

class Polygon:
    def __init__(self, points, color, light_source):
        self.points = points
        self.color = color
        self.light_source = light_source
        self.update()

    def update(self):
        midpoint = self.points[1] + np.array([self.points[2][0] - self.points[1][0], self.points[2][1] - self.points[1][1], self.points[2][2] - self.points[1][2]]) * (1 / 2)
        self.center = self.points[0] + np.array([midpoint[0] - self.points[0][0], midpoint[1] - self.points[0][1], midpoint[2] - self.points[0][2]]) * (2 / 3)

        BC = np.array([self.points[0][0] - self.points[1][0], self.points[0][1] - self.points[1][1], self.points[0][2] - self.points[1][2]])
        BA = np.array([self.points[2][0] - self.points[1][0], self.points[2][1] - self.points[1][1], self.points[2][2] - self.points[1][2]])
        self.normal = np.array([BA[1] * BC[2] - BA[2] * BC[1], BA[2] * BC[0] - BA[0] * BC[2], BA[0] * BC[1] - BA[1] * BC[0]])
        pointing_vector = np.array([self.light_source[0] - self.center[0], self.light_source[1] - self.center[1], self.light_source[2] - self.center[2]])
        self.cos_theta = (pointing_vector[0] * self.normal[0] + pointing_vector[1] * self.normal[1] + pointing_vector[2] * self.normal[2]) / (get_vector_length(pointing_vector) * get_vector_length(self.normal))

        
class Mesh():
    def __init__(self, polygons, center=[0, 0, 0]):
        self.polygons = polygons
        self.center = center

    def from_file(filepath, color, lightsource, center=[0, 0, 0]):
        m = mesh.Mesh.from_file(filepath)
        polygons = []
        for i in range(len(m.x)):
            p0 = np.array([m.x[i][0], m.z[i][0], m.y[i][0]])
            p1 = np.array([m.x[i][1], m.z[i][1], m.y[i][1]])
            p2 = np.array([m.x[i][2], m.z[i][2], m.y[i][2]])
            polygon = Polygon([p0, p2, p1], color, lightsource)
            polygons.append(polygon)
        
        return Mesh(polygons, center)
    
    def move(self, vector):
        for polygon in self.polygons:
            polygon.points = list(map(lambda point:  point + vector, polygon.points))
            polygon.update()

    def rotate_y(self, angle, center):
        for polygon in self.polygons:
            new_points = []
            for point in polygon.points:
                vector = np.array([point[0] - center[0], point[1] - center[1], point[2] - center[2]])
                length = sqrt(vector[0] ** 2 + vector[2] ** 2)
                if length != 0:
                    if vector[2] > 0:
                        old_angle = degrees(acos(vector[0] / length))
                    else:
                        old_angle = -degrees(acos(vector[0] / length))
                    new_angle = old_angle + angle
                    new_point = np.array([center[0] + length * cos(radians(new_angle)), point[1], center[2] + length * sin(radians(new_angle))])
                    new_points.append(new_point)
                else:
                    new_points.append(point)
            polygon.points = new_points
            polygon.update()
        
    def rotate_z(self, angle, center):
        for polygon in self.polygons:
            new_points = []
            for point in polygon.points:
                vector = np.array([point[0] - center[0], point[1] - center[1], point[2] - center[2]])
                length = sqrt(vector[1] ** 2 + vector[0] ** 2)
                if length != 0:
                    if vector[0] > 0:
                        old_angle = degrees(acos(vector[1] / length))
                    else:
                        old_angle = -degrees(acos(vector[1] / length))
                    new_angle = old_angle + angle
                    new_point = np.array([center[0] + length * sin(radians(new_angle)), center[1] + length * cos(radians(new_angle)), point[2]])
                    new_points.append(new_point)
                else:
                    new_points.append(point)
            polygon.points = new_points
            polygon.update()

    def rotate_x(self, angle, center):
        for polygon in self.polygons:
            new_points = []
            for point in polygon.points:
                vector = np.array([point[0] - center[0], point[1] - center[1], point[2] - center[2]])
                length = sqrt(vector[1] ** 2 + vector[2] ** 2)
                if length != 0:
                    if vector[2] > 0:
                        old_angle = degrees(acos(vector[1] / length))
                    else:
                        old_angle = -degrees(acos(vector[1] / length))
                    new_angle = old_angle + angle
                    new_point = np.array([point[0], center[1] + length * cos(radians(new_angle)), center[2] + length * sin(radians(new_angle))])
                    new_points.append(new_point)
                else:
                    new_points.append(point)
            polygon.points = new_points
            polygon.update()

'''class LightSource():
    def __init__(self, x, y, z):
        super().__init__(x, y, z)'''
    