import pygame
from main import Point, Vector, Camera, Edge, Polygon, LightSource
from math import radians


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
#pygame.mixer.init()  # для звука
camera = Camera(Point(0, 0, 0), 0, 0)
screen = pygame.display.set_mode((camera.width, camera.height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


A = Point(2, -1, 1)
B = Point(2, 1, 1)
C = Point(2, 1, -1)
D = Point(2, -1, -1)

A1 = Point(4, -1, 1)
B1 = Point(4, 1, 1)
C1 = Point(4, 1, -1)
D1 = Point(4, -1, -1)

A2 = Point(1, -1, 3)
B2 = Point(1, 1, 3)
C2 = Point(1, 1, 2)
D2 = Point(1, -1, 2)

A3 = Point(3, -1, 3)
B3 = Point(3, 1, 3)
C3 = Point(3, 1, 2)
D3 = Point(3, -1, 2)

AB = Edge(A, B)
BC = Edge(B, C)
CD = Edge(C, D)
DA = Edge(D, A)
AA1 = Edge(A, A1)
BB1 = Edge(B, B1)
CC1 = Edge(C, C1)
DD1 = Edge(D, D1)
A1B1 = Edge(A1, B1)
B1C1 = Edge(B1, C1)
C1D1 = Edge(C1, D1)
D1A1 = Edge(D1, A1)

p1 = Point(1, -1, 1)
p2 = Point(2, 0, 2)
p3 = Point(1, 1, 1)

LIGHTSOURCE = LightSource(5, 5, 5)

POLYGONS = [#Polygon([A, B, C], BLUE, LIGHTSOURCE), Polygon([A, C, D], BLUE, LIGHTSOURCE), #называем вершины против часовой стрелки
            #Polygon([C, C1, D1], WHITE, LIGHTSOURCE), Polygon([C, D1, D], WHITE, LIGHTSOURCE),
            Polygon([A1, B, A], WHITE, LIGHTSOURCE), 
            #Polygon([A, A1, D1], WHITE, LIGHTSOURCE), Polygon([A, D1, D], WHITE, LIGHTSOURCE),
            #Polygon([B, B1, C1], WHITE, LIGHTSOURCE), Polygon([B, C1, C], WHITE, LIGHTSOURCE),
            #Polygon([A1, B1, C1], WHITE, LIGHTSOURCE), Polygon([A1, C1, D1], WHITE, LIGHTSOURCE),
            #Polygon([A2, B2, C2], WHITE, LIGHTSOURCE), Polygon([A2, C2, D2], WHITE, LIGHTSOURCE),
            #Polygon([C2, C3, D3], WHITE, LIGHTSOURCE), Polygon([C2, D3, D2], WHITE, LIGHTSOURCE),
            #Polygon([A3, B3, B2], WHITE, LIGHTSOURCE), Polygon([A3, B2, A2], WHITE, LIGHTSOURCE), 
            #Polygon([B3, C3, C2], WHITE, LIGHTSOURCE), Polygon([C2, B2, B3], WHITE, LIGHTSOURCE),
            #Polygon([A2, A3, D3], WHITE, LIGHTSOURCE), Polygon([A2, D3, D2], WHITE, LIGHTSOURCE),
            #Polygon([B2, B3, C3], WHITE, LIGHTSOURCE), Polygon([B2, C3, C2], WHITE, LIGHTSOURCE),
            #Polygon([A3, B3, C3], WHITE, LIGHTSOURCE), Polygon([A3, C3, D3], WHITE, LIGHTSOURCE)]
]

#POLYGONS = [Polygon([Point(0, 0, 0), Point(0, 1, 0), Point(0, 0, 1)])]

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
            camera.angle_z += 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            camera.angle_z -= 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            camera.position.x += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            camera.position.x -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            camera.position.z += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            camera.position.z -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            camera.position.y += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            camera.position.y -= 1

    #render_edges([AB, BC, CD, DA, AA1, BB1, CC1, DD1, A1B1, B1C1, C1D1, D1A1])

    screen.fill(BLACK)
    pos = camera.render_points([LIGHTSOURCE])[0]
    pos = (pos[0] * (camera.width / radians(camera.vision)) + camera.width // 2, -1 * pos[1] * (camera.height / radians(camera.vision)) + camera.height // 2)
    pygame.draw.circle(screen, WHITE, pos, 5)
    for i in sorted(POLYGONS, key=lambda x: (camera.getDistance(x), camera.get_distance_to_point(x.center)), reverse=True):
        pygame.draw.polygon(screen, *camera.render_polygon(i))
    pygame.display.flip()
    

pygame.quit()
#TODO: fix edges points that are not rendering
#TODO: write vector multiplication as vector's magic method
#TODO: rewrite translation to new basis as a new method
#TODO: fix visibility of objects behind the camera
#TODO: fix zero division in rotation methods
#TODO: consider implementing Möller–Trumbore intersection algorithm