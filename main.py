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

def get_projection(v1, v2):
    return (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / get_vector_length(v1)

def rotate_vector(vector, axis, angle):
    #print(degrees(acos((vector[0] * axis[0] + vector[1] * axis[1] + vector[2] * axis[2]) / (get_vector_length(axis) * get_vector_length(vector)))))
    k = get_projection(axis, vector) / get_vector_length(axis)
    r_projection_on_axis = np.array([axis[0] * k, axis[1] * k, axis[2] * k])
    r = np.array([vector[0] - r_projection_on_axis[0], vector[1] - r_projection_on_axis[1], vector[2] - r_projection_on_axis[2]]) #перпендикуляр от конца вектора к оси
    p = np.array([r[1] * axis[2] - r[2] * axis[1], r[2] * axis[0] - r[0] * axis[2], r[0] * axis[1] - r[1] * axis[0]])
    #p = np.array([axis[1] * r[2] - axis[2] * r[1], axis[2] * r[0] - axis[0] * r[2], axis[0] * r[1] - axis[1] * r[0]])
    if get_vector_length(r) != 0:
        k_r = (2 * sin(radians(angle / 2)) * get_vector_length(r) * sin(radians(angle / 2))) / get_vector_length(r)
        k_p = (2 * sin(radians(angle / 2)) * get_vector_length(r) * cos(radians(angle / 2))) / get_vector_length(p)
        a = np.array([p[0] * k_p, p[1] * k_p, p[2] * k_p])
        b = np.array([-r[0] * k_r, -r[1] * k_r, -r[2] * k_r])
        v = np.array([a[0] + b[0], a[1] + b[1], a[2] + b[2]]) #вектор перемещения
        vector1 = np.array([vector[0] + v[0], vector[1] + v[1], vector[2] + v[2],])
        return v
    return np.array([0, 0, 0])

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
    def __init__(self, position: np.ndarray, angle_x: Union[int, float], angle_y: Union[int, float], angle_z: Union[int, float], screen, width, height):
        self.position = position
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.vision_x = 55
        self.vision_y = 60
        self.width = width  
        self.height = height 
        self.fps = 30
        self.background = 30
        self.screen = screen
        self.axes = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


    def translate_points(self, points):
        translated_points = []
        translation_vector = self.position
        for i in points:
            translated_points.append(i - translation_vector)
        return translated_points

    def render_points(self, points):
        return_list = []
        points = self.translate_points(points)
        points = self.rotate_around_axis(-self.angle_y, self.axes[1], points)
        points = self.rotate_around_axis(-self.angle_z, self.axes[2], points)
        points = self.rotate_around_axis(-self.angle_x, self.axes[0], points)
        for vector in points:
            try:
                if vector[0] >= 0:
                    new_x = asin(vector[2] / sqrt(vector[0] ** 2 + vector[2] ** 2))
                    new_y = asin(vector[1] / sqrt(vector[0] ** 2 + vector[1] ** 2))
                else:
                    new_x = radians(180) - asin(vector[2] / sqrt(vector[0] ** 2 + vector[2] ** 2))
                    new_y = radians(180) - asin(vector[1] / sqrt(vector[0] ** 2 + vector[1] ** 2))
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
            return_list.append((new_x * (self.width / radians(self.vision_x)) + self.width // 2, -1 * new_y * (self.height / radians(self.vision_y)) + self.height // 2))

        #print(return_list)

        return return_list
    
    def rotate_around_axis(self, angle, axis, points):
        rotated_points = []   
        for i in points:
            v = rotate_vector(i, axis, angle)
            rotated_points.append(np.array([i[0] + v[0], i[1] + v[1], i[2] + v[2]]))

        return rotated_points
    
    def change_orientation(self, axis, angle):
        new_axes = []
        for i in range(3):
            v = rotate_vector(self.axes[i], axis, angle)
            new_axes.append([self.axes[i][0] + v[0], self.axes[i][1] + v[1], self.axes[i][2] + v[2]])
        self.axes = np.array(new_axes)
    
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
        return [max(i * polygon.cos_theta, self.background) for i in polygon.color], points
    
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
        self.acceleration = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation_v = np.array([0.0, 0.0, 0.0])
        self.rotation_a = np.array([0.0, 0.0, 0.0])
        self.rotational_mass = 1
        self.mass = 1
        self.collision_sphere_rad = min(map(lambda x: min(x), [[sqrt((point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2 + (point[2] - self.center[2]) ** 2 ) for point in polygon.points] for polygon in self.polygons]))
        self.visible = True
        self.axes = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


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
    
    def move(self):
        for polygon in self.polygons:
            polygon.points = list(map(lambda point:  point + self.velocity, polygon.points))
            polygon.update()

    def rotate_around_axis(self, axis, angle, center):
        for polygon in self.polygons:
            new_points = []
            for point in polygon.points:
                radius = np.array([point[0] - center[0], point[1] - center[1], point[2] - center[2]]) #радиус-вектор точки
                v = rotate_vector(radius, axis, angle)
                new_points.append(np.array([point[0] + v[0], point[1] + v[1], point[2] + v[2]]))
            polygon.points = new_points
            polygon.update()

        new_axes = []
        for i in range(3):
            v = rotate_vector(self.axes[i], axis, angle)
            new_axes.append([self.axes[i][0] + v[0], self.axes[i][1] + v[1], self.axes[i][2] + v[2]])
        self.axes = np.array(new_axes)

    def update(self):
        self.velocity = np.array([self.velocity[i] + self.acceleration[i]  for i in range(3)])
        self.move()
        self.rotation_v = np.array([self.rotation_v[i] + self.rotation_a[i] for i in range(3)])
        self.rotate_around_axis(self.axes[0], self.rotation_v[0], self.center)
        self.rotate_around_axis(self.axes[1], self.rotation_v[1], self.center)
        self.rotate_around_axis(self.axes[2], self.rotation_v[2], self.center)

    '''def check_collision(self, other_mesh):
        for other_polygon in filter(lambda i: get_projection(i.normal, np.array([self.center[0] - i.center[0], self.center[1] - i.center[1], self.center[2] - i.center[2]])), other_mesh.polygons):
            for own_polygon in self.polygons:
                for point in own_polygon.points:
                    BC = np.array([other_polygon.points[0][0] - other_polygon.points[1][0], other_polygon.points[0][1] - other_polygon.points[1][1], other_polygon.points[0][2] - other_polygon.points[1][2]])
                    BA = np.array([other_polygon.points[2][0] - other_polygon.points[1][0], other_polygon.points[2][1] - other_polygon.points[1][1], other_polygon.points[2][2] - other_polygon.points[1][2]])
                    CA = np.array([other_polygon.points[0][0] - other_polygon.points[2][0], other_polygon.points[0][1] - other_polygon.points[2][1], other_polygon.points[0][2] - other_polygon.points[2][2]])
                    normal = np.array([BA[1] * BC[2] - BA[2] * BC[1], BA[2] * BC[0] - BA[0] * BC[2], BA[0] * BC[1] - BA[1] * BC[0]])
                    length = abs(normal[0] * point[0] + normal[1] * point[1] + normal[2] * point[2] - (normal[0] * other_polygon.points[1][0] + normal[1] * other_polygon.points[1][1] + normal[2] * other_polygon.points[1][2])) / sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
                    normal = normal * (length / sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2))
                    antinormal = normal * -1

                    

                    intersec_point = point + normal
                    if normal[0] * intersec_point[0] + normal[1] * intersec_point[1] + normal[2] * intersec_point[2] - (normal[0] * other_polygon.points[1][0] + normal[1] * other_polygon.points[1][1] + normal[2] * other_polygon.points[1][2]) != 0:
                        intersec_point = point + antinormal
                    
                    #print(normal[0], normal[1], normal[2])
                    #print(intersec_point[0], intersec_point[1], intersec_point[2])
                        

                    #новая проверка на вхождение точки пересечения в треугольник
                    DA = np.array([intersec_point[0] - other_polygon.points[0][0], intersec_point[1] - other_polygon.points[0][1], intersec_point[2] - other_polygon.points[0][2]])
                    DB = np.array([intersec_point[0] - other_polygon.points[1][0], intersec_point[1] - other_polygon.points[1][1], intersec_point[2] - other_polygon.points[1][2]])
                    DC = np.array([intersec_point[0] - other_polygon.points[2][0], intersec_point[1] - other_polygon.points[2][1], intersec_point[2] - other_polygon.points[2][2]])

                    s_ABC = get_vector_length(np.array([BA[1] * BC[2] - BA[2] * BC[1], BA[2] * BC[0] - BA[0] * BC[2], BA[0] * BC[1] - BA[1] * BC[0]])) / 2
                    s_ABD = get_vector_length(np.array([DA[1] * DB[2] - DA[2] * DB[1], DA[2] * DB[0] - DA[0] * DB[2], DA[0] * DB[1] - DA[1] * DB[0]])) / 2
                    s_BCD = get_vector_length(np.array([DB[1] * DC[2] - DB[2] * DC[1], DB[2] * DC[0] - DB[0] * DC[2], DB[0] * DC[1] - DB[1] * DC[0]])) / 2
                    s_DCA = get_vector_length(np.array([DA[1] * DC[2] - DA[2] * DC[1], DA[2] * DC[0] - DA[0] * DC[2], DA[0] * DC[1] - DA[1] * DC[0]])) / 2

                    if s_ABD + s_BCD + s_DCA > s_ABC:
                        return True
                    return False'''

    

'''class LightSource():
    def __init__(self, x, y, z):
        super().__init__(x, y, z)'''
    