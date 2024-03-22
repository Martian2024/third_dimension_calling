from typing import Union
from math import sin, cos, tan, sqrt, atan, pi, radians, degrees

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def scale(self, k):
        self.x *= k
        self.y *= k
        self.z *= k

    def __mul__(self, k: Union[int, float]):
        return Vector(self.x * k, self.y * k, self.z * k)


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
    
class Edge:
    def __init__(self, point1: Point, point2: Point):
        self.points = [point1, point2]

    

class Camera:
    def __init__(self, position: Point, angle: Union[int, float]):
        self.position = position
        self.angle = angle
        self.vision = 60
        self.plane_side = 2 * tan(radians(self.vision))

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
                new_angle = degrees(atan(vector.z / vector.x)) - self.angle
                new_x = sqrt(vector.x ** 2 + vector.z ** 2) * cos(radians(new_angle))
                new_z = sqrt(vector.x ** 2 + vector.z ** 2) * sin(radians(new_angle))
                rotated_points.append(Point(new_x, i.y, new_z))
            except ZeroDivisionError:
                pass
        return rotated_points

            


    def render_points(self, points):
        return_list = []
        points = self.translate_points(points)
        points = self.rotate_points_y(points)
        for i in points:
            vector = Vector(i.x, i.y, i.z)
            k = vector.x 
            try:
                new_x = vector.z / k #не исправлять, тут должен быть z
                new_y = vector.y / k
                return_list.append((new_x, new_y))
            except ZeroDivisionError:
                pass

        return return_list
    
    def render_edges(self, edges):
        return_list = []
        for i in edges:
            return_list.append(self.render_points(i.points))
        return return_list


