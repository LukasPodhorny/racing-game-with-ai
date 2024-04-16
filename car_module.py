import pygame

class car_object:

    def __init__(self, img, fps):
        self.img = img
        self.fps = fps
        
        self.carx = 100
        self.cary = 100
        self.angle = 20
        self.wheel_rotation = 0  # hodnota mezi 0 - neco jako 0.7 !ne jedna!

        self.pix_per_sec = 100
        self.speed = 0
    
    def get_input():
        keys = pygame.key.get_pressed()
        input = [0,0]
        
        if keys[pygame.K_LEFT]:
            input[0] = -1
        if keys[pygame.K_RIGHT]:
            input[0] = 1
        if keys[pygame.K_DOWN]:
            input[1] = 1
        if keys[pygame.K_UP]:
            input[1] = -1
        
        return input


    def show(self, screen):

        screen.blit(pygame.transform.rotate(self.img, self.angle), (self.carx + (self.img.get_width() / 2), self.cary + (self.img.get_height() / 2)))
        
    
    def update(self):
        h_input = car_object.get_input()[0]
        v_input = car_object.get_input()[1]

        self.speed = (self.pix_per_sec/self.fps) # udelat by jel dopredu pouze stranou kterou faceuje
        self.angle += -h_input
        pass




    
        