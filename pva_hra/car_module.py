import pygame

class car_object:

    def __init__(self, img):
        self.img = img
        
        self.carx = 0
        self.cary = 0
    
    def get_input():
        keys = pygame.key.get_pressed()
        input = (0,0)
        
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
        screen.blit(self.img, (self.carx + (self.img.get_width() / 2), self.cary + (self.img.get_height() / 2)))
    
    def update(self):
        self.carx = car_object.get_input()[0]
        self.cary = car_object.get_input()[1]
        pass


    
        