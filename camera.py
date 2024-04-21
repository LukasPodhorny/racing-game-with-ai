
class camera:
    def __init__(self, pos, scale = 1):
        self.pos = pos
        self.scale = scale
    
    def blit(self, screen, image, pos):
        screen.blit(image, (pos[0]-self.pos[0],pos[1]-self.pos[1]))
    