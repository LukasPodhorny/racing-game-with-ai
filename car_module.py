import pygame
import math
from settings import *
from usefulfunctions import *

class car_object:

    def __init__(self, img, start_pos, angle = 0):
        self.img = img

        self.x = start_pos[0]
        self.y = start_pos[1]
        self.pos = (self.x, self.y)
        self.last_pos = (self.x, self.y)
        self.angle = angle

        self.speed = 0

    def get_input():
        keys = pygame.key.get_pressed()
        input = [0,0]
        
        if keys[pygame.K_a]:
            input[0] += -1
        if keys[pygame.K_d]:
            input[0] += 1
        
        if keys[pygame.K_s]:
            input[1] += 1
        if keys[pygame.K_w]:
            input[1] += -1
        
        return input
    
    def convert_ai_input(ai_input):
        input = [0,0]
        
        if ai_input[0] == 1:
            input[0] = -1
        if ai_input[0] == 2:
            input[0] = 1
        
        if ai_input[1] == 1:
            input[1] = 1
        if ai_input[1] == 2:
            input[1] = -1
        
        return input

    # reset pos
    def reset(self, start_pos, start_angle):
        self.speed = 0
        self.angle = start_angle
        self.x, self.y = start_pos

    # draw car on the screen
    def show(self, camera, screen):
        # rotzoom is for better quality, but for performance choose rotate
        img = pygame.transform.rotozoom(self.img,self.angle, 1)
        img_rect = img.get_rect(center = (self.x, self.y))
        camera.blit(screen, img, img_rect)

    def raycast(self, origin, max_length, line_count, spread_angle, current_track, cam, offset = (0,0), debug_mode = False):
        col_data = [read_col_data("collider_data/track_col_data_"+str(current_track)+"_0"), 
                    read_col_data("collider_data/track_col_data_"+str(current_track)+"_1")]
        
        new_origin = add_points(origin, offset)
        
        lengths = []
        end_points = []
        
        current_angle = -spread_angle/2
        angle_step = spread_angle / (line_count-1)

        for _ in range(0,line_count):
            new_x = new_origin[0] +  math.cos(math.radians(current_angle + self.angle)) * max_length
            new_y = new_origin[1] + -math.sin(math.radians(current_angle + self.angle)) * max_length
        
            length = max_length
            end_point = (new_x, new_y)

            for line_data in col_data:
                for i in range(0, len(line_data)-1):
                    a = cam.r_pos(line_data[i  ])
                    b = cam.r_pos(line_data[i+1])
    
                    intersection = getIntersection(new_origin, (new_x, new_y), a, b)
                    if intersection:
                        if debug_mode:
                            new_length = math.dist(new_origin,intersection)
                            if length > new_length:
                                end_point = intersection
                                length = new_length
                        else:
                            length = min(length,math.dist(new_origin,intersection))
            
            lengths.append(length)
            end_points.append(end_point)

            current_angle += angle_step
        
        if debug_mode:
            return lengths, end_points
        
        return lengths, None

    def check_collisions(self, origin, cam, current_track):
        col_data = [read_col_data("collider_data/track_col_data_"+str(current_track)+"_0"), 
                    read_col_data("collider_data/track_col_data_"+str(current_track)+"_1")]

        c = cam.r_pos((self.x * world_pos, self.y * world_pos)) 
        d = cam.r_pos(multi_point(self.last_pos, world_pos))

        for line_data in col_data:
            
            for j in range(0, len(line_data)-1):
                
                a = cam.r_pos(line_data[j  ])
                b = cam.r_pos(line_data[j+1])
                if isIntersection(a, b, c, d):
                    return True               
        return False
    
    def check_reward_gates(self, origin, cam, current_track):
        col_data = read_col_data("collider_data/track_rewardgate_data_"+str(current_track)+"_0")
        
        c = cam.r_pos((self.x * world_pos, self.y * world_pos)) 
        d = cam.r_pos(multi_point(self.last_pos, world_pos))

        for j in range(0,(int)(len(col_data)/2)):
            a = cam.r_pos(col_data[2*j])
            b = cam.r_pos(col_data[2*j+1])
            
            if isIntersection(a, b, c, d):
                return (2*j , 2*j)                    
        return None
    
    def check_win(self, origin, cam, current_track):
        col_data = read_col_data("collider_data/track_win_data_"+str(current_track)+"_0")
 
        c = cam.r_pos((self.x * world_pos, self.y * world_pos)) 
        d = cam.r_pos(multi_point(self.last_pos, world_pos))
        a = cam.r_pos(col_data[0])
        b = cam.r_pos(col_data[1])

        return isIntersection(a, b, c, d)                     

        
    def update_pos(self, deltaTime, ai_input = None):
        self.last_pos = (self.x, self.y)

        # input will provide either person or ai model
        if ai_input is None:
            input = car_object.get_input()
        else:
            input = car_object.convert_ai_input(ai_input)

        # logic for driving the car
        if input[1] < 0:                                                    # w
            self.speed = min(max_speed,self.speed + acceleration * deltaTime) 
        elif input[1] > 0:                                                  # s
            self.speed = max(max_back_speed,self.speed - braking * deltaTime)
        elif input[1] == 0:
            if self.speed > 0:
                self.speed = max(0,self.speed - decceleration * deltaTime)
            elif self.speed < 0:
                self.speed = min(0, self.speed + decceleration * deltaTime)

        # logic for turning the car
        if abs(self.speed) > activate_turning_speed:
            self.angle -= input[0] * turning_speed * deltaTime
        
        # applying the speed correctly
        fwd_dir = normalize((math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))))
        self.x += fwd_dir[0] * self.speed * deltaTime
        self.y += fwd_dir[1] * self.speed * deltaTime
