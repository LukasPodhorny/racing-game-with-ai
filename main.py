import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("racing game")

screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0), 1)

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), 0.06*res_multiplier)
mycar = car_module.car_object(car_img, fps)

bg = pygame.transform.smoothscale_by(pygame.image.load("images/maintrack.png").convert(), 5*res_multiplier)

getTicksLastFrame = 0
 
debug_font = pygame.font.SysFont("Arial" , 30 , bold = True)
def render_fps():
    fps_str = "fps: " + str(int(fpsClock.get_fps()))
    fps_tex = debug_font.render(fps_str , 1, pygame.Color("PURPLE"))
    screen.blit(fps_tex,(0,0))

while True:

    # handling exiting game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # calculating deltaTime
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    # GAME LOGIC START
    
    mycar.update_pos(deltaTime)
    cam.pos = (mycar.carx - h_w, mycar.cary - h_h)

    screen.fill((154, 218, 111))
    cam.blit(screen, bg, (0,0))
    mycar.show(cam, screen)

    # fps counter
    render_fps()
    
    pygame.display.update()

    # GAME LOGIC END

    fpsClock.tick()

