import pygame
from main import Point, Vector, Camera, Edge, Polygon
from math import radians

WIDTH = 500  
HEIGHT = 500 
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

camera = Camera(Point(0, 0, 0), 0, 0)

A = Point(2, -1, 1)
B = Point(2, 1, 1)
C = Point(2, 1, -1)
D = Point(2, -1, -1)

A1 = Point(4, -1, 1)
B1 = Point(4, 1, 1)
C1 = Point(4, 1, -1)
D1 = Point(4, -1, -1)

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

POLYGONS = [
            Polygon([C, C1, D1]), Polygon([C, D1, D]),
            Polygon([A1, B1, B]), Polygon([A1, B, A]), 
            Polygon([B1, C1, C]), Polygon([C, B, B1]),
            Polygon([A, A1, D1]), Polygon([A, D1, D]),
            Polygon([B, B1, C1]), Polygon([B, C1, C]),
            Polygon([A1, B1, C1]), Polygon([A1, C1, D1])]

running = True
while running:
    clock.tick(FPS)

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
    starting_color = WHITE
    for i in sorted(POLYGONS, key=lambda x: (camera.getDistance(x), camera.get_distance_to_point(x.center)), reverse=True):
        points = camera.render_polygon(i)
        pos1 = (points[0][0] * (WIDTH / radians(camera.vision)) + WIDTH // 2, -1 * points[0][1] * (HEIGHT / radians(camera.vision)) + HEIGHT // 2)
        pos2 = (points[1][0] * (WIDTH / radians(camera.vision)) + WIDTH // 2, -1 * points[1][1] * (HEIGHT / radians(camera.vision)) + HEIGHT // 2)
        pos3 = (points[2][0] * (WIDTH / radians(camera.vision)) + WIDTH // 2, -1 * points[2][1] * (HEIGHT / radians(camera.vision)) + HEIGHT // 2)
        pygame.draw.polygon(screen, starting_color, [pos1, pos2, pos3])
        starting_color = (starting_color[0] - 255 / len(POLYGONS), *starting_color[1:])
    pygame.display.flip()
    

pygame.quit()
#TODO: fix edges points that are not rendering
#TODO: write vector multiplication as vector's magic method
#TODO: rewrite translation to new basis as a new method
#TODO: fix visibility of objects behind the camera