import pygame
from main import Camera, Polygon, Mesh, rotate_vector, get_vector_length
from math import radians, degrees, acos
from stl import mesh
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HEIGHT = 600
WIDTH = 900


pygame.init()
#pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
camera = Camera(np.array([-5.0, 0.0, 0.0]), 0, 0, 0, screen, WIDTH, HEIGHT)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


A = np.array([-2.0, -1.0, 1.0])
B = np.array([-2.0, 1.0, 1.0])
C = np.array([-2.0, 1.0, -1.0])
D = np.array([-2.0, -1.0, -1.0])

A1 = np.array([2.0, -1.0, 1.0])
B1 = np.array([2.0, 1.0, 1.0])
C1 = np.array([2.0, 1.0, -1.0])
D1 = np.array([2.0, -1.0, -1.0])

A2 = np.array([1.0, -1.0, 3.0])
B2 = np.array([1.0, 1.0, 3.0])
C2 = np.array([1.0, 1.0, 2.0])
D2 = np.array([1.0, -1.0, 2.0])

A3 = np.array([3.0, -1.0, 3.0])
B3 = np.array([3.0, 1.0, 3.0])
C3 = np.array([3.0, 1.0, 2.0])
D3 = np.array([3.0, -1.0, 2.0])



p1 = np.array([1.0, -1.0, 1.0])
p2 = np.array([2.0, 0.0, 2.0])
p3 = np.array([1.0, 1.0, 1.0])

LIGHTSOURCE = np.array([-30, 0, 0])

POLYGONS = [Polygon([A, B, C], BLUE, LIGHTSOURCE), Polygon([A, C, D], BLUE, LIGHTSOURCE), #называем вершины против часовой стрелки             Polygon([C, C1, D1], WHITE, LIGHTSOURCE), Polygon([C, D1, D], WHITE, LIGHTSOURCE),
            Polygon([A1, B, A], GREEN, LIGHTSOURCE), Polygon([A1, B1, B], GREEN, LIGHTSOURCE),
            Polygon([A, D1, A1], WHITE, LIGHTSOURCE), Polygon([A, D, D1], WHITE, LIGHTSOURCE),
            Polygon([B, B1, C1], WHITE, LIGHTSOURCE), Polygon([B, C1, C], WHITE, LIGHTSOURCE),
            Polygon([C, C1, D], WHITE, LIGHTSOURCE), Polygon([C1, D1, D], WHITE, LIGHTSOURCE),
           Polygon([A1, C1, B1], WHITE, LIGHTSOURCE), Polygon([D1, C1, A1], WHITE, LIGHTSOURCE),
           Polygon([A2, B2, C2], WHITE, LIGHTSOURCE), Polygon([A2, C2, D2], WHITE, LIGHTSOURCE),
           Polygon([C2, C3, D3], WHITE, LIGHTSOURCE), Polygon([C2, D3, D2], WHITE, LIGHTSOURCE),
            Polygon([A3, B3, B2], WHITE, LIGHTSOURCE), Polygon([A3, B2, A2], WHITE, LIGHTSOURCE), 
            Polygon([B3, C3, C2], WHITE, LIGHTSOURCE), Polygon([C2, B2, B3], WHITE, LIGHTSOURCE),
            Polygon([D3, A3, A2], WHITE, LIGHTSOURCE), Polygon([D2, D3, A2], WHITE, LIGHTSOURCE),
            Polygon([C3, B3, A3], WHITE, LIGHTSOURCE), Polygon([D3, C3, A3], WHITE, LIGHTSOURCE)]

#MESHES = [Mesh.from_file('Chest_01.stl', WHITE, LIGHTSOURCE)]
#MESHES = [Mesh(POLYGONS[:12])]
#ship = Mesh.from_file('cube3.stl', WHITE, LIGHTSOURCE)
MESHES = [Mesh.from_file('player_ship.stl', WHITE, LIGHTSOURCE)]
#MESHES = [Mesh.from_file('asteroid.stl', WHITE, LIGHTSOURCE)]
#MESHES = [Mesh.from_file('ship.stl', WHITE, LIGHTSOURCE)]
MESHES[0].rotation_v[2] = 3
#MESHES = [Mesh([Polygon([A, B, C], BLUE, LIGHTSOURCE)])]
#print(MESHES[0].polygons[0].points[0].x)



#POLYGONS = [Polygon([np.array([0, 0, 0), np.array([0, 1, 0), np.array([0, 0, 1)])]

running = True
while running:
    clock.tick(camera.fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            camera.angle_y += 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            camera.angle_y -= 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            camera.angle_z -= 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            camera.angle_z += 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            camera.position[0] += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            camera.position[0] -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            camera.position[2] += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            camera.position[2] -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            camera.position[1] += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            camera.position[1] -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            MESHES[0].rotate_around_axis(MESHES[0].axes[2], 3, MESHES[0].center)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            MESHES[0].rotate_around_axis(MESHES[0].axes[2], -3, MESHES[0].center)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            MESHES[0].rotate_around_axis(MESHES[0].axes[1], 3, MESHES[0].center)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            MESHES[0].rotate_around_axis(MESHES[0].axes[1], -3, MESHES[0].center)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
            MESHES[0].rotate_around_axis(MESHES[0].axes[0], -3, MESHES[0].center)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            MESHES[0].rotate_around_axis(MESHES[0].axes[0], 3, MESHES[0].center)

    #render_edges([AB, BC, CD, DA, AA1, BB1, CC1, DD1, A1B1, B1C1, C1D1, D1A1])

    screen.fill(BLACK)
    #MESHES[0].move(Vector(0, 0, 1))
    #MESHES[0].rotate_y(1, np.array([3, 0, 0]))
    #MESHES[0].rotate_z(1, np.array([3, 0, 0))
    pos = camera.render_points([LIGHTSOURCE])[0]
    pos = (pos[0] * (camera.width / radians(camera.vision_x)) + camera.width // 2, -1 * pos[1] * (camera.height / radians(camera.vision_y)) + camera.height // 2)
    pygame.draw.circle(screen, WHITE, pos, 5)
    # for i in sorted(POLYGONS, key=lambda x: (camera.getDistance(x), camera.get_distance_to_point(x.center)), reverse=True):
    #         if camera.get_projection(i.normal, Vector(camera.position.x - i.center.x, camera.position.y - i.center.y, camera.position.z - i.center.z)) > 0: #AAAAAAAA
    #             pygame.draw.polygon(camera.screen, *camera.render_polygon(i))
    for i in MESHES:
        i.update()
        for j in MESHES:
            if i != j:
                pass
                #print(i.check_collision(j))
        camera.render_mesh(i)
    pygame.display.flip()
    #print(1)
    

pygame.quit()
#TODO: write vector multiplication as vector's magic method
#TODO: fix visibility of objects behind the camera
#TODO: consider implementing Möller–Trumbore intersection algorithm