import sys
import pygame.camera
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
import csv
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("racing game")

screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0), 1)

track = pygame.transform.smoothscale_by(pygame.image.load("images/maintrack5.png").convert_alpha(), 0.7*world_pos)# deleno 5
 
collision_data = []

while True:
    mouse_down = False
    # handling exiting game
    for event in pygame.event.get():
        if event.type == QUIT:
            
            collision_data.insert(0,('x', 'y'))

            with open("line_collider_data", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(collision_data)

            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

    # background
    screen.fill((154, 218, 111))
    cam.blit(screen, track, (0,0))

    if mouse_down:
        collision_data.append((pygame.mouse.get_pos()[0] * world_pos, pygame.mouse.get_pos()[1]* world_pos))
        mouse_down = False
    
    # ploting editing line
    if len(collision_data) > 0:
        for i in range(0, len(collision_data)-1):
            pygame.draw.line(screen, pygame.Color("RED"),(collision_data[i][0] / world_pos, collision_data[i][1] / world_pos), (collision_data[i+1][0] / world_pos,collision_data[i+1][1] / world_pos))
        pygame.draw.line(screen, pygame.Color("RED"),(collision_data[len(collision_data)-1][0] / world_pos,collision_data[len(collision_data)-1][1] / world_pos), pygame.mouse.get_pos())

    pygame.display.update()
