import pygame
from main import Point, Vector, Camera

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
C = Point(2, -1, -1)
D = Point(2, 1, -1)

A1 = Point(3, -1, 1)
B1 = Point(3, 1, 1)
C1 = Point(3, -1, -1)
D1 = Point(3, 1, -1)

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
    for i in camera.render_points([A, B, C, D, A1, B1, C1, D1]):
        pos = (i[0] * (WIDTH / camera.plane_side) + WIDTH // 2, -1 * i[1] * (HEIGHT / camera.plane_side) + HEIGHT // 2)
        pygame.draw.circle(screen, WHITE, pos, 5)
    pygame.display.flip()

pygame.quit()