import sys
import pygame.camera
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *
 
pygame.init()
 
fpsClock = pygame.time.Clock()

pygame.display.set_caption("racing game")

screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0), 1)

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), 0.06*world_pos)
mycar = car_module.car_object(car_img)

current_track = 0
track_img = make_track(tracks[current_track])
col_data = "collider_data/col_data_" + current_track + "_" 

getTicksLastFrame = 0
 
debug_font = pygame.font.SysFont("Arial" , (int)(30 * world_pos) , bold = True)
def render_fps():
    fps_str = "fps: " + str(int(fpsClock.get_fps()))
    fps_tex = debug_font.render(fps_str , 1, pygame.Color("PURPLE"))
    screen.blit(fps_tex,(0,0))

while True:
    mouse_down = False
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
    
    # updating
    mycar.update_pos(deltaTime)
    cam.pos = (mycar.carx - h_w, mycar.cary - h_h)
    poses = mycar.raycast((mycar.carx - cam.pos[0], mycar.cary - cam.pos[1]), 400, 20, 90, None)

    # background
    screen.fill((154, 218, 111))
    cam.blit(screen, track_img, (0,0))

    # ploting
    for pos in poses:
        pygame.draw.line(screen, pygame.Color(255,0,0), (mycar.carx - cam.pos[0], mycar.cary - cam.pos[1]), pos, 2)
    mycar.show(cam, screen)

    # ploting fps for debug
    render_fps()
    
    pygame.display.update()

    # GAME LOGIC END

    fpsClock.tick()

