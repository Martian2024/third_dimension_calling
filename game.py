from main import Mesh, Camera, rotate_vector, get_projection, get_vector_length
from game_classes import Player
from game_classes import Star
import pygame
import numpy as np
from random import randint
from math import degrees, asin, sqrt, acos, cos

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

ASTEROIDS = []
STARS = []
BULLETS = []

running = True

flag_start_menu = False
flag_pause = False
flag_traking_mouse = False
mouse_prev_pos = []
add_angle_y = 0
add_angle_z = 0

def generate_world():
    vector = np.array([100000000000000.0, 0.0, 0.0])
    v = rotate_vector(vector, np.array([0, 1, 0]), randint(0, 360))
    vector += v
    sun = Star(vector)
    sun.size = 20
    STARS.append(sun)

    for i in range(200):
        vector = np.array([100000000000000.0, 0.0, 0.0])
        v = rotate_vector(vector, np.array([0, 0, 1]), randint(0, 360))
        vector += v
        v = rotate_vector(vector, np.array([0, 1, 0]), randint(0, 360))
        vector += v
        STARS.append(Star(vector))

    for i in range(2):
        asteroid = Mesh.from_file('asteroid.stl', (98, 59, 59), STARS[0].pos, center=[randint(-50, 50), randint(-50, 50), randint(-50, 50)])
        asteroid.velocity = np.array([randint(0, 0) / 100, randint(0, 0) / 100, randint(0, 0) / 100])
        asteroid.rotation_v = np.array([randint(0, 100) / 100, randint(0, 9) / 100, randint(0, 9) / 100])
        ASTEROIDS.append(asteroid)


def draw_start():
    pass

def draw_pause():
    pass

generate_world()
camera = Camera(np.array([-5.0, 0.0, 0.0]), 0, 0, 0, screen, WIDTH, HEIGHT)
player = Player(WHITE, STARS[0].pos)
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
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #     player.rotation_v[0] -= 0.07
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
        #     player.rotation_v[0] += 0.07
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            player.meshes[0].velocity *= 1.1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
            player.meshes[0].velocity /= 1.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            flag_traking_mouse = True
            mouse_prev_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            flag_traking_mouse = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            bullet = Mesh.from_file('bullet.stl', (0, 255, 51), STARS[0].pos, center=np.copy(player.meshes[0].center))
            bullet.radiating = True
            if player.meshes[0].velocity[0] >= 0:
                angle_y = degrees(asin(player.meshes[0].axes[0][2] / sqrt(player.meshes[0].axes[0][0] ** 2 + player.meshes[0].axes[0][2] ** 2)))
            else:
                angle_y = 180 - degrees(asin(player.meshes[0].axes[0][2] / sqrt(player.meshes[0].axes[0][0] ** 2 + player.meshes[0].axes[0][2] ** 2)))
            angle_z = -degrees(asin(player.meshes[0].axes[0][1] / get_vector_length(player.meshes[0].axes[0])))
            bullet.velocity = np.array([10.0, 0.0, 0.0])
            bullet.rotate_around_axis(np.array([0, 1, 0]), angle_y, center=bullet.center)
            bullet.rotate_around_axis(np.array([0, 0, 1]), angle_z, center=bullet.center)
            bullet.velocity += rotate_vector(bullet.velocity, np.array([0, 1, 0]), angle_y)
            bullet.velocity += rotate_vector(bullet.velocity, np.array([0, 0, 1]), angle_z)
            BULLETS.append(bullet)


    if flag_traking_mouse:
        add_angle_y += (pygame.mouse.get_pos()[0] - mouse_prev_pos[0]) / 10
        add_angle_z += (pygame.mouse.get_pos()[1] - mouse_prev_pos[1]) / 10
        mouse_prev_pos = pygame.mouse.get_pos()

    if flag_start_menu:
        draw_start()
    elif flag_pause:
        draw_pause()
    else:
        for star in STARS:
            pygame.draw.circle(screen, WHITE, camera.render_points([star.pos])[0], star.size)

        player.update()
        camera.position = player.meshes[0].center + player.meshes[0].axes[0] * -7 + player.meshes[0].axes[1] * 3
        #print(camera.position)
        if player.meshes[0].velocity[0] >= 0:
            camera.angle_y = degrees(asin(player.meshes[0].velocity[2] / sqrt(player.meshes[0].velocity[0] ** 2 + player.meshes[0].velocity[2] ** 2))) + add_angle_y
        else:
            camera.angle_y = 180 - degrees(asin(player.meshes[0].velocity[2] / sqrt(player.meshes[0].velocity[0] ** 2 + player.meshes[0].velocity[2] ** 2))) + add_angle_y
        camera.angle_z = -degrees(asin(player.meshes[0].velocity[1] / get_vector_length(player.meshes[0].velocity)))  + add_angle_z

        for mesh in sorted(player.meshes + ASTEROIDS + BULLETS, key=lambda x: (camera.get_distance_to_point(x.center)), reverse=True):
            if camera.get_distance_to_point(mesh.center) < camera.visibility_rad:
                mesh.update()
                camera.render_mesh(mesh)
            else:
                if mesh in BULLETS:
                    BULLETS.remove(mesh)
                else:
                    mesh.update()
                    camera.render_mesh(mesh)
            for j in camera.render_points([mesh.center]):
                pygame.draw.circle(screen, GREEN, j, 5)

        for i in ASTEROIDS:
            if player.meshes[0].check_collision(i):
                running = False
            for j in BULLETS:
                if i.check_collision(j):
                    ASTEROIDS.remove(i)

    pygame.display.flip()
    

pygame.quit()