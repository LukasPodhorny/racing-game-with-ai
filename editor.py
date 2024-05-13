import sys
import pygame
from pygame.locals import *
from camera import *
from settings import *
import csv
from usefulfunctions import *
 
# Init
pygame.init()
fpsClock = pygame.time.Clock()
pygame.display.set_caption("track editor")

# Setting up screen
screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
h_w = screen.get_width()/2
h_h = screen.get_height()/2

cam = camera((0,0))



#---------------------------SETTINGS-------------------------------- 
track_index = 1
scalar = 0.2
centered = False
offset = (0,0)
obj = pygame.transform.smoothscale_by(pygame.image.load(tracks[track_index][0]).convert_alpha(), tracks[track_index][1]* scalar * world_pos)
obj_name = "track"
data = "win" 
connect_lines = False
file_counter = 0
collision_data = []
#---------------------------SETTINGS-------------------------------- 



# Save array as .csv
def save_data(identifier, collision_data):
    collision_data.insert(0,('x', 'y'))

    with open("collider_data/" + obj_name + "_"+data+"_data_" + identifier, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(collision_data)


while True:
    
    mouse_down = False
    space = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = True
    
    screen.fill((154, 218, 111))
    
    img_pos = (0,0)
    if centered:
        img_pos = obj.get_rect(center = (0, 0))
    
    cam.blit(screen, obj, add_points(img_pos, offset))

    if space:
        save_data(str(track_index) + '_' + str(file_counter), collision_data)
        collision_data = []
        file_counter += 1
        space = False
    if mouse_down:
        collision_data.append((((pygame.mouse.get_pos()[0] - offset[0])/scalar/world_pos), ((pygame.mouse.get_pos()[1] - offset[1])/scalar/world_pos)))
        mouse_down = False
    

    # drawing editing line and some debuging info
    if len(collision_data) > 0:
        if not connect_lines:
            for i in range(0, (int)(len(collision_data)/2)):

                a = add_points(multi_point(collision_data[2*i  ], scalar * world_pos), offset)
                b = add_points(multi_point(collision_data[2*i+1], scalar * world_pos), offset)

                pygame.draw.line(screen, pygame.Color("RED"),a, b)
        else:
            for i in range(0, len(collision_data)-1):

                a = add_points(multi_point(collision_data[i  ], scalar * world_pos), offset)
                b = add_points(multi_point(collision_data[i+1], scalar * world_pos), offset)

                pygame.draw.line(screen, pygame.Color("RED"),a, b)
                

        if connect_lines or len(collision_data)%2 != 0:
            a = add_points(multi_point(collision_data[len(collision_data)-1], scalar * world_pos), offset)
            b = pygame.mouse.get_pos()   

        pygame.draw.line(screen, pygame.Color("RED"), a, b)
    
    pygame.draw.circle(screen, pygame.Color("Green"), offset, 5)
    pygame.draw.circle(screen, pygame.Color("Red"), multi_point(tracks[track_index][2], scalar), 7)


    pygame.display.update()
