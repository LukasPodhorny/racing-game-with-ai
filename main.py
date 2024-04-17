import sys
import car_module
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Auto, který jede")
screen = pygame.display.set_mode((1020,820))

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png"), 0.05)
mycar = car_module.car_object(car_img, fps)
 
while True:
    screen.fill((154, 218, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # hra
    mycar.update()
    mycar.show(screen)

    # hra
              
    pygame.display.flip()
    fpsClock.tick(fps)
