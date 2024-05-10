import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *

# Init
pygame.init()
pygame.display.set_caption("racing game")
fpsClock = pygame.time.Clock()


# Setting up screen
screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2
bg_color = (154, 218, 111)

cam = camera((0,0), 1)

# Setting up current track and colliders for the track
current_track = 1

def setup_track(current_track):
    global track_img
    track_img = make_track(tracks[current_track])

    col_line_count = 2

    global col_data
    col_data = []
    for i in range(0, col_line_count):
        col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))

setup_track(current_track)

# Setting up car object
car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)
player_car = car_module.car_object(car_img, tracks[current_track][2], angle = tracks[current_track][3])

# Time variables
getTicksLastFrame = 0
reset_time = 0
finish_time = 0

# State is scene that will be rendered
state = "menu"


# Setting up buttons
def play():
    global state
    state = "game"
    global reset_time
    reset_time = pygame.time.get_ticks()/1000

def next_track():
    global state
    state = "game"
    
    global reset_time
    reset_time = pygame.time.get_ticks()/1000
    
    global current_track
    current_track += 1

    setup_track(current_track)
    player_car.reset(tracks[current_track][2], tracks[current_track][3])
def train():
    global state
    state = "train"

def exit_to_menu():
    global state
    state = "menu"

def exit():
    pygame.quit()
    sys.exit()

button_play = Button(pygame.rect.Rect(h_w-100,h_h-50,200,100), bg_color, play, text = "Play", **BUTTON_STYLE) 
button_train = Button(pygame.rect.Rect(h_w-100,h_h+100,200,100),bg_color, train, text = "Train", **BUTTON_STYLE)
button_exit = Button(pygame.rect.Rect(h_w-100,h_h+250,200,100),bg_color, exit, text = "Exit", **BUTTON_STYLE)

button_next_track = Button(pygame.rect.Rect(h_w-100,h_h-50,200,100),bg_color, next_track, text = "Next", **BUTTON_STYLE) 
button_exit_menu = Button(pygame.rect.Rect(h_w-100,h_h+100,200,100),bg_color, exit_to_menu, text = "Menu", **BUTTON_STYLE)



# Main game loop
while True:
    
    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if state == "menu":
            button_play.check_event(event)
            button_train.check_event(event)
            button_exit.check_event(event)

        if state == "win":
            button_next_track.check_event(event)
            button_exit_menu.check_event(event)  
  


    if state == "menu":        
        screen.fill(bg_color)

        button_play.update(screen)
        button_train.update(screen)
        button_exit.update(screen)
        
        # Header
        render_text(screen, (h_w, h_h - 500 * world_pos), "The Racing Game", 200, pygame.Color("Black"), center=True)
        
        pygame.display.update()
    
    if state == "win":        
        screen.fill(bg_color)

        button_next_track.update(screen)
        button_exit_menu.update(screen) 
        
        # Header
        render_text(screen, (h_w, h_h - 500 * world_pos), "Track " + str(current_track+1) + " completed", 200, pygame.Color("Black"), center=True)
        render_text(screen, (h_w, h_h - 350 * world_pos), str((int)(finish_time)) + " seconds", 200, pygame.Color("Black"), center=True)
        
        pygame.display.update()
        
    if state == "game":    
        
        # calculating deltaTime
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        time = t/1000 - reset_time

        # GAME LOGIC START
        # updating
        player_car.update_pos(deltaTime)
        cam.pos = (player_car.x - h_w, player_car.y - h_h)
        raycast_origin = cam.r_pos((player_car.x, player_car.y))
        lengths, intersections = player_car.raycast(raycast_origin, 1500, 25, 120, col_data, cam, debug_mode = debug)
        game_over = player_car.check_collisions(raycast_origin, col_data, cam)
        win = player_car.check_win(raycast_origin, cam)
        
        if game_over:
            player_car.reset(tracks[current_track][2], tracks[current_track][3])
            reset_time += time

        if win:
            finish_time = time
            state = "win"


        # drawing background first
        screen.fill(bg_color)
        cam.blit(screen, track_img, (0,0))

        # drawing
        player_car.show(cam, screen)
        
        # GUI
        render_text(screen, (h_w,80*world_pos), "time: " + str(int(time)), size = 80, color = pygame.Color("White"), center= True)

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

            render_text(screen, (screen.get_width() - 90 * world_pos, 0), "fps: " + str(int(fpsClock.get_fps())), size=40, color = pygame.Color("Red"))

        pygame.display.update()

        # GAME LOGIC END

        fpsClock.tick()
