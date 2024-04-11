import sys
import car_module
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Auto, který jede")
width, height = 640, 480
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

car_img = pygame.image.load("cardownsize.png")
 
while True:
    screen.fill((154, 218, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # hra
            
    mycar = car_module.car_object(car_img)
    mycar.show(screen)

    # hra
              
    pygame.display.flip()
    fpsClock.tick(fps)

