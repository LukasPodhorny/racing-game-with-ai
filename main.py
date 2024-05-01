import sys
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
bg_color = (154, 218, 111)

cam = camera((0,0), 1)

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), 0.06*world_pos)
mycar = car_module.car_object(car_img)

# setting up current track and colliders for the track
current_track = 0
track_img = make_track(tracks[current_track])
col_line_count = 2

col_data = []
for i in range(0, col_line_count):
    col_data.append(read_col_data("collider_data/col_data_" + str(current_track) + "_" + str(i)))

getTicksLastFrame = 0
 
# fps rendering for debugging
debug_font = pygame.font.SysFont("Arial" , (int)(30 * world_pos) , bold = True)
def render_fps():
    fps_str = "fps: " + str(int(fpsClock.get_fps()))
    fps_tex = debug_font.render(fps_str , 1, text_color)
    screen.blit(fps_tex,(0,0))

while True:
    
    # events
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
    lengths, intersections = mycar.raycast((mycar.carx - cam.pos[0], mycar.cary - cam.pos[1]), 3000, 40, 90, col_data, cam, True)

    # drawing background first
    screen.fill(bg_color)
    cam.blit(screen, track_img, (0,0))

    # drawing
    mycar.show(cam, screen)

    # rendering gizmos for debugging
    if debug:
        for i in range(0,len(col_data[0])-1):
            pygame.draw.line(screen, pygame.Color(255,0,0), (col_data[0][i][0] - cam.pos[0],col_data[0][i][1] - cam.pos[1]), (col_data[0][i+1][0] - cam.pos[0],col_data[0][i+1][1] - cam.pos[1]), 2)
        for i in range(0,len(col_data[1])-1):
            pygame.draw.line(screen, pygame.Color(255,0,0), (col_data[1][i][0] - cam.pos[0],col_data[1][i][1] - cam.pos[1]), (col_data[1][i+1][0] - cam.pos[0],col_data[1][i+1][1] - cam.pos[1]), 2)

        i = 0  
        for pos in intersections:
            pygame.draw.line(screen, raycast_color, (mycar.carx - cam.pos[0], mycar.cary - cam.pos[1]), pos, 2)
            if lengths[i] < 2000:
                pygame.draw.circle(screen, pygame.Color("White"), pos, 5)
            i += 1

        render_fps()
    
    pygame.display.update()

    # GAME LOGIC END

    fpsClock.tick()

