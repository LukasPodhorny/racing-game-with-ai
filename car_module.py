import pygame

class car_object:

    def __init__(self, img, fps):
        self.img = img
        self.fps = fps
        
        self.carx = 0
        self.cary = 0
        self.angle = 0
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
    
    def display(self, surface, image, pos, originPos, angle):

        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        
        surface.blit(rotated_image, rotated_image_rect)
    

    def show(self, screen):
        self.display(screen, self.img, (self.carx, self.cary), (150, 250), self.angle)
        
    
    def update(self):
        h_input = car_object.get_input()[0] 
        v_input = car_object.get_input()[1]
                         
        self.speed = (self.pix_per_sec/self.fps) # udelat by jel dopredu pouze stranou kterou faceuje
        self.angle += -h_input
        pass




    
        