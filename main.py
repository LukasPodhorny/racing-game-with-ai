import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
import ctypes
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("racing game")

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)

cam = camera((0,0))

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), 0.06)
mycar = car_module.car_object(car_img, fps)

bg = pygame.transform.smoothscale_by(pygame.image.load("images/topdowntrack.png"), 4.5)
 
while True:
    screen.fill((154, 218, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    cam.blit(screen, bg, (0,0))
    
    # hra
    mycar.update()
    cam.pos = (mycar.carx - screen.get_width()/2, mycar.cary - screen.get_height()/2)
    mycar.show(cam, screen)

    # hra
    pygame.display.flip()
    fpsClock.tick(fps)
