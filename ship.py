from main import Mesh, Polygon
import numpy as np
from math import cos, sin, radians, sqrt
from main import Mesh

class Player:
    def __init__(self, color, lightsource):
        self.meshes = [Mesh.from_file('ship.stl', color, lightsource)]
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation_v = np.array([0.0, 0.0, 0.0])
        self.max_rotation_v = np.array([5.0, 5.0, 5.0])

    def update(self):
        for mesh in self.meshes:
            mesh.rotation_v = self.rotation_v
            mesh.velocity = self.velocity
            mesh.update()
        
    def rotate(self, angle, axis):
        for mesh in self.meshes:
            mesh.rotate_around_axis(axis, angle, self.meshes[0].center)

    