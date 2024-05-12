
class camera:
    # you can also include scale, but I didn't chose to, because of performance
    def __init__(self, pos):
        self.pos = pos
    
    def blit(self, screen, image, pos):
        screen.blit(image, (pos[0]-self.pos[0],pos[1]-self.pos[1]))
    
    def r_pos(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])
    