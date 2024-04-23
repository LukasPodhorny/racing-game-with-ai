import pygame
import math

class car_object:

    def __init__(self, img, fps):
        self.img = img
        self.fps = fps
        
        self.carx = 150
        self.cary = 150
        self.angle = 0

        self.max_speed = 21
        self.max_back_speed = -7.5
        self.acceleration = 0.05
        self.decceleration = 0.038
        self.braking = 0.15
        self.activate_turning_speed = 1
        self.turning_speed = 1.5
        
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

    def show(self, camera, screen):
        img = pygame.transform.rotozoom(self.img,self.angle,1)
        img_rect = img.get_rect(center = (self.carx, self.cary))
        camera.blit(screen, img, img_rect)
        
    
    def update(self):
        input = car_object.get_input() # input bud provede ai, nebo clovek

        if input[1] < 0:
            self.speed = min(self.max_speed,self.speed + self.acceleration) #w
        elif input[1] > 0:
            self.speed = max(self.max_back_speed,self.speed - self.braking) #s
        elif input[1] == 0:
            if self.speed > 0:
                self.speed = max(0,self.speed - self.decceleration)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.decceleration)
        
        if self.speed > self.activate_turning_speed:
            self.angle -= input[0] * self.turning_speed
        elif self.speed < -self.activate_turning_speed:
            self.angle += input[0] * self.turning_speed

        fwd_dir = self.normalize((math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))))

        self.carx += fwd_dir[0] * self.speed
        self.cary += fwd_dir[1] * self.speed


        pass