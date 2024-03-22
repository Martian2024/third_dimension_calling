import pygame
from main import Point, Vector, Camera, Edge

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

camera = Camera(Point(0, 0, 0), 0)

A = Point(2, -1, 1)
B = Point(2, 1, 1)
C = Point(2, 1, -1)
D = Point(2, -1, -1)

A1 = Point(3, -1, 1)
B1 = Point(3, 1, 1)
C1 = Point(3, 1, -1)
D1 = Point(3, -1, -1)

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

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            camera.angle += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            camera.angle -= 1
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

    screen.fill(BLACK)
    for i in camera.render_edges([AB, BC, CD, DA, AA1, BB1, CC1, DD1, A1B1, B1C1, C1D1, D1A1]):
        pos1 = (i[0][0] * (WIDTH / camera.plane_side) + WIDTH // 2, -1 * i[0][1] * (HEIGHT / camera.plane_side) + HEIGHT // 2)
        pos2 = (i[1][0] * (WIDTH / camera.plane_side) + WIDTH // 2, -1 * i[1][1] * (HEIGHT / camera.plane_side) + HEIGHT // 2)
        pygame.draw.line(screen, WHITE, pos1, pos2, 5)
    pygame.display.flip()

pygame.quit()
#TODO: fix edges points that are not rendering