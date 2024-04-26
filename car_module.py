import pygame
import math
from settings import *

class car_object:

    def __init__(self, img, fps):
        self.img = img
        self.fps = fps
        
        self.carx = 150
        self.cary = 150
        self.angle = 0

        self.speed = 0
    
    def normalize(self, vector):
        magnitude = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        return (vector[0]/magnitude, vector[1]/magnitude)
    
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

    # plot car on the screen
    def show(self, camera, screen):
        img = pygame.transform.rotozoom(self.img,self.angle,1)
        img_rect = img.get_rect(center = (self.carx, self.cary))
        camera.blit(screen, img, img_rect)
    
    # return list of lengths from point at given range
    def raycast(mask, start_point, count, spread_angle):
        current_angle = 0
        step_angle = spread_angle/count
        
        for i in range(0, count):
            current_angle += i*step_angle

        
    def update_pos(self, deltaTime):
        input = car_object.get_input() # input bud provede ai, nebo clovek

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
        

        fwd_dir = self.normalize((math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))))

        self.carx += fwd_dir[0] * self.speed * deltaTime
        self.cary += fwd_dir[1] * self.speed * deltaTime