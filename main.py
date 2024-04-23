import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
import ctypes
import random
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("racing game")

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0))

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), 0.06*true_res[0] / 2880)
mycar = car_module.car_object(car_img, fps)

bg = pygame.transform.smoothscale_by(pygame.image.load("images/track6.png").convert_alpha(), 5*true_res[0] / 2880)
 
font = pygame.font.SysFont("Arial" , 36 , bold = True)
def render_fps():
    fpscount = "fps: " + str(int(fpsClock.get_fps()))
    fps_t = font.render(fpscount , 1, pygame.Color("BLACK"))
    screen.blit(fps_t,(0,0))

while True:
    screen.fill((154, 218, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # hra
    mycar.update()
    cam.pos = (mycar.carx - h_w, mycar.cary - h_h)

    cam.blit(screen, bg, (0,0))
    mycar.show(cam, screen)

    # temporary fps counter
    render_fps()
    # temporary fps counter
    
    # hra
    pygame.display.flip()
    fpsClock.tick(fps)
