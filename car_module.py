import pygame
import math
from settings import *
from usefulfunctions import *

class car_object:

    def __init__(self, img):
        self.img = img

        self.x = 1900 * world_pos
        self.y = 1900 * world_pos
        self.pos = (self.x, self.y)
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
    
    def reset(self, start_pos):
        self.speed = 0
        self.angle = 0
        self.x, self.y = start_pos

    # draw car on the screen
    def show(self, camera, screen):
        # add rotzoom for better quality, but worse performance
        img = pygame.transform.rotate(self.img,self.angle)
        img_rect = img.get_rect(center = (self.x, self.y))
        camera.blit(screen, img, img_rect)

    def raycast(self, origin, max_length, line_count, spread_angle, col_data, cam, offset = (0,0), debug_mode = False):
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
                    
                    if intersection != None:
                        if debug_mode:
                            new_length = distance(new_origin,intersection)

                            if length > new_length:
                                end_point = intersection
                                length = new_length
                        else:
                            length = min(length,distance(new_origin,intersection))
            
            lengths.append(length)
            end_points.append(end_point)

            current_angle += angle_step
        
        if debug_mode:
            return lengths, end_points
        
        return length, None

    def check_collisions(self, origin, col_data, cam):
        car_col_data = read_col_data("collider_data/car_col_data_0_0") 

        for i in range(0, len(car_col_data)-1): 
            c = add_points(origin,car_col_data[i])
            d = add_points(origin,car_col_data[i+1])

            for line_data in col_data:
                
                for j in range(0, len(line_data)-1):
                    a = cam.r_pos(line_data[j  ])
                    b = cam.r_pos(line_data[j+1])

                    if isIntersection(a, b, c, d):
                        return True               
        return False

        
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

        self.x += fwd_dir[0] * self.speed * deltaTime
        self.y += fwd_dir[1] * self.speed * deltaTime