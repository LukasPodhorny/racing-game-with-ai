import sys
import pygame
from pygame.locals import *
from camera import *
from settings import *
import csv
from usefulfunctions import *
 
pygame.init()
fpsClock = pygame.time.Clock()

pygame.display.set_caption("track editor")

screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0), 1)

track_index = 0
scalar = 0.2
track = make_track((tracks[track_index][0],tracks[track_index][1]*scalar))
file_counter = 0
collision_data = []

def save_data(identifier, collision_data):
    collision_data.insert(0,('x', 'y'))

    with open("collider_data/col_data_" + identifier, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(collision_data)

while True:
    
    mouse_down = False
    space = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = True
    
    screen.fill((154, 218, 111))
    cam.blit(screen, track, (0,0))

    if space:
        save_data(str(track_index) + '_' + str(file_counter), collision_data)
        collision_data = []
        file_counter += 1
        space = False
    if mouse_down:
        collision_data.append(((pygame.mouse.get_pos()[0]/scalar/world_pos), (pygame.mouse.get_pos()[1]/scalar/world_pos)))
        mouse_down = False
    
    # drawing editing line
    if len(collision_data) > 0:
        for i in range(0, len(collision_data)-1):
            pygame.draw.line(screen, pygame.Color("RED"),(collision_data[i][0] * scalar, collision_data[i][1] * scalar), (collision_data[i+1][0] * scalar,collision_data[i+1][1] * scalar))
        pygame.draw.line(screen, pygame.Color("RED"),(collision_data[len(collision_data)-1][0] * scalar,collision_data[len(collision_data)-1][1] * scalar), pygame.mouse.get_pos())

    pygame.display.update()
