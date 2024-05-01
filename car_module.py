import pygame
import math
from settings import *
from usefulfunctions import *

class car_object:

    def __init__(self, img):
        self.img = img
        
        self.carx = 1200 * world_pos
        self.cary = 1200 * world_pos
        self.angle = 0

        self.speed = 0
    
    def get_input():
        keys = pygame.key.get_pressed()
        input = [0,0]
        
        if keys[pygame.K_a]:
            input[0] = -1
        if keys[pygame.K_d]:
            input[0] = 1
        
        if keys[pygame.K_s]:
            input[1] = 1
        if keys[pygame.K_w]:
            input[1] = -1
        
        return input

    # draw car on the screen
    def show(self, camera, screen):
        # add rotzoom for better quality, but worse performance
        img = pygame.transform.rotate(self.img,self.angle)
        img_rect = img.get_rect(center = (self.carx, self.cary))
        camera.blit(screen, img, img_rect)
    
    def raycast(self, origin, max_length, line_count, spread_angle, col_data, cam, debug_mode = False):
        lengths = []
        end_points = []
        
        current_angle = -spread_angle/2
        angle_step = spread_angle / (line_count-1)

        for _ in range(0,line_count):
            new_x = origin[0] +  math.cos(math.radians(current_angle + self.angle)) * max_length
            new_y = origin[1] + -math.sin(math.radians(current_angle + self.angle)) * max_length
        
            length = max_length
            end_point = (new_x, new_y)

            for line_data in col_data:
                for i in range(0, len(line_data)-1):
                    intersection = getIntersection((origin[0], origin[1]), (new_x, new_y), (line_data[i][0]-cam.pos[0],line_data[i][1]-cam.pos[1]),(line_data[i+1][0]-cam.pos[0],line_data[i+1][1]-cam.pos[1]))
                    
                    if intersection != None:
                        if debug_mode:
                            new_length = distance(origin,intersection)

                            if length > new_length:
                                end_point = intersection
                                length = new_length
                        else:
                            length = min(length,distance(origin,intersection))
            
            lengths.append(length)
            end_points.append(end_point)

            current_angle += angle_step
        
        if debug_mode:
            return (lengths,end_points)
        return lengths
            

        
    def update_pos(self, deltaTime):
        # input bud provede ai, nebo clovek
        input = car_object.get_input()

        if input[1] < 0:                                                    # w
            self.speed = min(max_speed,self.speed + acceleration * deltaTime) 
        elif input[1] > 0:                                                  # s
            self.speed = max(max_back_speed,self.speed - braking * deltaTime)
        elif input[1] == 0:
            if self.speed > 0:
                self.speed = max(0,self.speed - decceleration * deltaTime)
            elif self.speed < 0:
                self.speed = min(0, self.speed + decceleration * deltaTime)

        if abs(self.speed) > activate_turning_speed:
            self.angle -= input[0] * turning_speed * deltaTime
        

        fwd_dir = normalize((math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))))

        self.carx += fwd_dir[0] * self.speed * deltaTime
        self.cary += fwd_dir[1] * self.speed * deltaTime