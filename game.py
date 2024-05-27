from main import Mesh, Camera
from ship import Player
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
FPS = 60
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

camera = Camera(np.array([-5.0, 0.0, 0.0]), 0, 0, screen, 500, 500)
LIGHTSOURCE = np.array([0, 50, 0])
player = Player(WHITE, LIGHTSOURCE)

MESHES = [player, 
          Mesh.from_file('cube3.stl', WHITE, LIGHTSOURCE, center=np.array([10, 0, 0])),
          Mesh.from_file('cube3.stl', WHITE, LIGHTSOURCE, center=np.array([0, 10, 0])),
          Mesh.from_file('cube3.stl', WHITE, LIGHTSOURCE, center=np.array([0, 0, 10])),
          ]


running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        elif keys[pygame.K_w]:
            player.burn_forward()
        elif keys[pygame.K_s]:
            player.burn_backwards()
        elif keys[pygame.K_d]:
            player.burn_right()
        elif keys[pygame.K_a]:
            player.burn_left()


    for mesh in MESHES:
        mesh.update()
        camera.render_mesh(mesh)
    


    #render_ui

    pygame.display.flip()
    #print(1)
    

pygame.quit()