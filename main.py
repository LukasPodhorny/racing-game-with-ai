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

# setting up current track and colliders for the track
current_track = 0
track_img = make_track(tracks[current_track])
col_line_count = 2

car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)
player_car = car_module.car_object(car_img, tracks[current_track][2], tracks[current_track][3])


col_data = []
for i in range(0, col_line_count):
    col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))

getTicksLastFrame = 1000
time = 0
 
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

    # calculating deltaTime and time
    time = pygame.time.get_ticks()
    deltaTime = (time - getTicksLastFrame) / 1000.0
    getTicksLastFrame = time

    
    # GAME LOGIC START
    # updating
    player_car.update_pos(deltaTime)
    cam.pos = (player_car.x - h_w, player_car.y - h_h)
    raycast_origin = cam.r_pos((player_car.x, player_car.y))
    lengths, intersections = player_car.raycast(raycast_origin, 1500, 25, 120, col_data, cam, debug_mode = True)
    game_over = player_car.check_collisions(raycast_origin, col_data, cam)
    win = player_car.check_win(raycast_origin, cam)

    if game_over:
        player_car.reset(tracks[current_track][2])
    
    if win:
        pygame.quit()
        sys.exit()
    

    # drawing background first
    screen.fill(bg_color)
    cam.blit(screen, track_img, (0,0))

    # drawing
    player_car.show(cam, screen)

    # rendering gizmos for debugging
    if debug:
        car_col_data = read_col_data("collider_data/car_col_data_0_0")

        # drawing track collider boundaries
        for i in range(0,len(col_data[0])-1):
            pygame.draw.line(screen, pygame.Color("Red"), cam.r_pos(col_data[0][i]), cam.r_pos(col_data[0][i+1]), 2)
        for i in range(0,len(col_data[1])-1):
            pygame.draw.line(screen, pygame.Color("Red"), cam.r_pos(col_data[1][i]), cam.r_pos(col_data[1][i+1]), 2)

        for i in range(0,(int)(len(car_col_data)/2)):
            pygame.draw.line(screen, pygame.Color("Green"), add_points(raycast_origin, car_col_data[2*i]), add_points(raycast_origin, car_col_data[2*i+1]), 2)
        pygame.draw.circle(screen, pygame.Color("White"), raycast_origin, 3)
        
        # drawing raycast
        if intersections:
            i = 0  
            for intersection in intersections:
                pygame.draw.line(screen, raycast_color, raycast_origin, intersection, 1)
                if lengths[i] < 2000:
                    pygame.draw.circle(screen, pygame.Color("White"), intersection, 5)
                i += 1

        render_fps()
    
    pygame.display.update()

    # GAME LOGIC END

    fpsClock.tick()

