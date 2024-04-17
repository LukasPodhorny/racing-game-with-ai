import pygame
import math

class car_object:

    def __init__(self, img, fps):
        self.img = img
        self.fps = fps
        
        self.carx = 150
        self.cary = 150
        self.angle = 0
        self.wheel_rotation = 0  # hodnota mezi 0 - neco jako 0.7 !ne jedna!

        self.pix_per_sec = 100
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

    def show(self, screen):
        img = pygame.transform.rotozoom(self.img,self.angle,1)
        img_rect = img.get_rect(center = (self.carx, self.cary))
        screen.blit(img, img_rect)
        
    
    def update(self):
        input = car_object.get_input()

        self.angle += -input[0]
        fwd_dir = (math.cos(self.angle), math.sin(self.angle))

        self.carx += fwd_dir[0] * input[1]
        self.cary += fwd_dir[1] * input[1]

        pass




    
        