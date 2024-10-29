import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *
from stable_baselines3 import PPO
import os

# Initialization
pygame.init()
pygame.display.set_caption("racing game")
fpsClock = pygame.time.Clock()


# Setting up screen
screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2
bg_color = (154, 218, 111)

cam = camera((0,0))

# Setting up current track and colliders for the track
current_track = 0

track_img = make_track(tracks[current_track])
col_data = [read_col_data("collider_data/track_col_data_"+str(current_track)+"_0"), 
                    read_col_data("collider_data/track_col_data_"+str(current_track)+"_1")]



# Player car
car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)
player_car = car_module.car_object(car_img, tracks[current_track][2], angle = tracks[current_track][3])

# Ai car
ai_car = car_module.car_object(car_img, tracks[current_track][2], angle = tracks[current_track][3])
ai_origin = cam.r_pos((ai_car.x, ai_car.y))
lengths, intersections = ai_car.raycast(ai_origin, 1500, 25, 120, current_track, cam, debug_mode = debug)
path = os.path.join('Training', 'Saved Models', '5_000_000selfdrivingtest')
model = PPO.load(path)


# Time variables
getTicksLastFrame = None
reset_time = 0
finish_time = 0
ai_finish_time = None

# State is scene that will be rendered
state = "menu"
win_number = 0
max_win_number = 2


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

    global track_img
    track_img = make_track(tracks[current_track])

    global col_data
    col_data = [read_col_data("collider_data/track_col_data_"+str(current_track)+"_0"), 
                    read_col_data("collider_data/track_col_data_"+str(current_track)+"_1")]


    player_car.reset(tracks[current_track][2], tracks[current_track][3])
    ai_car.reset(tracks[current_track][2], tracks[current_track][3])
def train():
    global state
    state = "train"

def exit_to_menu():   
    global reset_time
    reset_time = pygame.time.get_ticks()/1000
    
    global current_track
    current_track = 0

    global track_img
    track_img = make_track(tracks[current_track])

    global col_data
    col_data = [read_col_data("collider_data/track_col_data_"+str(current_track)+"_0"), 
                    read_col_data("collider_data/track_col_data_"+str(current_track)+"_1")]

    player_car.reset(tracks[current_track][2], tracks[current_track][3])
    ai_car.reset(tracks[current_track][2], tracks[current_track][3])

    global state
    state = "menu"

def exit():
    pygame.quit()
    sys.exit()

button_play = Button(pygame.rect.Rect(h_w-100,h_h-50,200,100), bg_color, play, text = "Play", **BUTTON_STYLE) 
button_exit = Button(pygame.rect.Rect(h_w-100,h_h+175,200,100),bg_color, exit, text = "Exit", **BUTTON_STYLE)

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
            button_exit.check_event(event)

        if state == "win":
            button_next_track.check_event(event)
            button_exit_menu.check_event(event) 

        if state == "wingame":
           button_exit_menu.check_event(event)  
        
  

    if state == "menu":        
        screen.fill(bg_color)

        button_play.update(screen)
        button_exit.update(screen)
        
        # Header
        render_text(screen, (h_w, h_h - 500 * world_pos), "The Racing Game", 200, pygame.Color("Black"), center=True)
        
        pygame.display.update()
    
    if state == "win":        
        screen.fill(bg_color)

        button_next_track.update(screen)
        button_exit_menu.update(screen)
        
        # Header and time score
        render_text(screen, (h_w, h_h - 500 * world_pos), "Track " + str(current_track+1) + " completed", 200, pygame.Color("Black"), center=True)
        render_text(screen, (h_w, h_h - 350 * world_pos), "You: " + str((int)(finish_time)) + " seconds", 115, pygame.Color("Blue"), center=True)
        
        if ai_finish_time:
            render_text(screen, (h_w, h_h - 250 * world_pos), "AI: " + str((int)(ai_finish_time)) + " seconds", 115, pygame.Color("Red"), center=True)
        else:
            render_text(screen, (h_w, h_h - 250 * world_pos), "AI: didin't finish", 115, pygame.Color("Red"), center=True)

        pygame.display.update()
    
    if state == "wingame":
        screen.fill(bg_color)

        button_exit_menu.update(screen) 
        
        # Header and time score
        render_text(screen, (h_w, h_h - 500 * world_pos), "Last track completed!", 200, pygame.Color("Black"), center=True)
        render_text(screen, (h_w, h_h - 350 * world_pos), "You: " + str((int)(finish_time)) + " seconds", 115, pygame.Color("Blue"), center=True)
        
        if ai_finish_time:
            render_text(screen, (h_w, h_h - 250 * world_pos), "AI: " + str((int)(ai_finish_time)) + " seconds", 115, pygame.Color("Red"), center=True)
        else:
            render_text(screen, (h_w, h_h - 250 * world_pos), "AI: didin't finish", 115, pygame.Color("Red"), center=True)
        
        pygame.display.update()
        
    if state == "game":    
        
        # calculating deltaTime and time
        t = pygame.time.get_ticks()
        if getTicksLastFrame:
            deltaTime = (t - getTicksLastFrame) / 1000.0
        else:
            deltaTime = 0.015
        getTicksLastFrame = t

        time = t/1000 - reset_time

        # updating
        player_car.update_pos(deltaTime)
        ai_car.update_pos(deltaTime, model.predict(lengths)[0])

        cam.pos = (player_car.x - h_w, player_car.y - h_h)
        
        ai_origin = cam.r_pos((ai_car.x, ai_car.y))
        player_origin = cam.r_pos((player_car.x, player_car.y))
        lengths, intersections = ai_car.raycast(ai_origin, 1500, 25, 120, current_track, cam, debug_mode = debug)
        
        game_over = player_car.check_collisions(player_origin, cam, current_track)
        win = player_car.check_win(player_origin, cam, current_track)

        ai_game_over = ai_car.check_collisions(ai_origin, cam, current_track)
        ai_win = ai_car.check_win(ai_origin, cam, current_track)
        
        if game_over:
            player_car.reset(tracks[current_track][2], tracks[current_track][3])
            reset_time += time
        if win:
            finish_time = time
            win_number += 1
            state = "win"

            if win_number == max_win_number:
                state = "wingame"
        
        if ai_win:
            ai_finish_time = time
        if ai_game_over:
            ai_car.reset(tracks[current_track][2], tracks[current_track][3])


        # drawing background first
        screen.fill(bg_color)
        cam.blit(screen, track_img, (0,0))

        # drawing sprites
        ai_car.show(cam, screen)
        player_car.show(cam, screen)
        
        # drawing GUI
        render_text(screen, (h_w,100*world_pos), str(int(time)), size = 100, color = pygame.Color("White"), center= True)


        # rendering gizmos for debugging
        if debug:
    
            # drawing track collider boundaries
            for i in range(0,len(col_data[0])-1):
                pygame.draw.line(screen, pygame.Color("Red"), cam.r_pos(col_data[0][i]), cam.r_pos(col_data[0][i+1]), 2)
            for i in range(0,len(col_data[1])-1):
                pygame.draw.line(screen, pygame.Color("Red"), cam.r_pos(col_data[1][i]), cam.r_pos(col_data[1][i+1]), 2)

            pygame.draw.circle(screen, pygame.Color("Blue"), player_origin, 4)

            # drawing raycast
            if intersections:
                i = 0  
                for intersection in intersections:
                    pygame.draw.line(screen, raycast_color, ai_origin, intersection, 1)

                    if lengths[i] < 1500:
                        pygame.draw.circle(screen, pygame.Color("White"), intersection, 5)
                        
                    i += 1

            render_text(screen, (screen.get_width() - 90 * world_pos, 0), "fps: " + str(int(fpsClock.get_fps())), size=40, color = pygame.Color("Purple"))

        
        pygame.display.update()
        fpsClock.tick()
