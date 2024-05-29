from main import Mesh, Camera, rotate_vector
from ship import Player
from ambient import Star
import pygame
import numpy as np
from random import randint
from math import degrees, asin, sqrt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HEIGHT = 900
WIDTH = 1200

pygame.init()
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

camera = Camera(np.array([-5.0, 0.0, 0.0]), 0, 0, 0, screen, WIDTH, HEIGHT)
LIGHTSOURCE = np.array([0, 50, 0])
player = Player(WHITE, LIGHTSOURCE)

MESHES = []
STARS = []

running = True

flag_start_menu = False
flag_pause = False

def generate_world():
    for i in range(200):
        vector = np.array([100000000000000.0, 0.0, 0.0])
        v = rotate_vector(vector, np.array([0, 0, 1]), randint(0, 360))
        vector += v
        v = rotate_vector(vector, np.array([0, 1, 0]), randint(0, 360))
        vector += v
        STARS.append(Star(vector))
    #print(STARS)

def draw_start():
    pass

def draw_pause():
    pass

def draw_game():    
    for star in STARS:
        pygame.draw.circle(screen, WHITE, camera.render_points([star.pos])[0], star.size)
    #player.rotation_v[1] = player.max_rotation_v[1] * (pygame.mouse.get_pos()[0] - WIDTH / 2) / WIDTH
    #player.rotation_v[2] = player.max_rotation_v[2] * (pygame.mouse.get_pos()[1] - HEIGHT / 2) / HEIGHT
    player.update()
    camera.position = player.meshes[0].center + player.meshes[0].axes[0] * -5 + player.meshes[0].axes[1] * 2
    camera_pointing_vector = player.meshes[0].center - camera.position
    camera.angle_y = degrees(asin(camera_pointing_vector[2] / sqrt(camera_pointing_vector[0] ** 2 + camera_pointing_vector[2] ** 2)))
    camera.change_orientation(camera.axes[1], camera.angle_y)
    camera.angle_z = -degrees(asin(camera_pointing_vector[1] / sqrt(camera_pointing_vector[0] ** 2 + camera_pointing_vector[1] ** 2)))
    camera.change_orientation(camera.axes[2], camera.angle_z)
    for mesh in player.meshes:
        mesh.update()
        camera.render_mesh(mesh)
    for mesh in MESHES:
        mesh.update()
        camera.render_mesh(mesh)

generate_world()

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        elif keys[pygame.K_RIGHT]:
            camera.angle_y += 3
        elif keys[pygame.K_LEFT]:
            camera.angle_y -= 3
        elif keys[pygame.K_UP]:
            camera.angle_z -= 3
        elif keys[pygame.K_DOWN]:
            camera.angle_z += 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            player.rotation_v[2] += 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            player.rotation_v[2] -= 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            player.rotation_v[1] += 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            player.rotation_v[1] -= 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            player.rotation_v[0] -= 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            player.rotation_v[0] += 0.07



    if flag_start_menu:
        draw_start()
    elif flag_pause:
        draw_pause()
    else:
        draw_game() 

    pygame.display.flip()
    #print(1)
    

pygame.quit()