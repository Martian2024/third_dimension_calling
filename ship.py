from main import Mesh, Polygon
import numpy as np
from math import cos, sin, radians, sqrt
from stl import mesh

class Player(Mesh):
    def __init__(self, color, lightsource):
        self.polygons = []
        m = mesh.Mesh.from_file('ship.stl')
        for i in range(len(m.x)):
            p0 = np.array([m.x[i][0], m.z[i][0], m.y[i][0]])
            p1 = np.array([m.x[i][1], m.z[i][1], m.y[i][1]])
            p2 = np.array([m.x[i][2], m.z[i][2], m.y[i][2]])
            polygon = Polygon([p0, p2, p1], color, lightsource)
            self.polygons.append(polygon)
        self.center = np.array([0.0, 0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.angles = np.array([0.0, 0.0, 0.0])
        self.rotation_v = np.array([0.0, 0.0, 0.0])
        self.rotation_a = np.array([0.0, 0.0, 0.0])
        self.rotational_mass = 1
        self.mass = 1
        self.collision_sphere_rad = min(map(lambda x: min(x), [[sqrt((point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2 + (point[2] - self.center[2]) ** 2 ) for point in polygon.points] for polygon in self.polygons]))
        self.visible = True
        self.thrust = 0.001
        


    def burn_forward(self):
        print(self.angles)
        self.acceleration = np.array([self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[1] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[2] + self.thrust / self.mass * sin(radians(self.angles[1]))])

    def burn_right(self):
        self.velocity = np.array([self.velocity[0] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[1] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[2] + self.thrust / self.mass * sin(radians(self.angles[1]))])

    def burn_left(self):
        self.velocity = np.array([self.velocity[0] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[1] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[2] + self.thrust / self.mass * sin(radians(self.angles[1]))])
    
    def burn_backwards(self):
        self.velocity = np.array([self.velocity[0] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[1] + self.thrust / self.mass * cos(radians(self.angles[1])),
                                  self.velocity[2] + self.thrust / self.mass * sin(radians(self.angles[1]))])

    