import math
import pygame
from settings import *
import csv

def lerp(a: float, b: float, percentage: float) -> float:
    return a + (b-a) * percentage 

def normalize(vector):
        magnitude = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        return (vector[0]/magnitude, vector[1]/magnitude)

def calculateOffsets (A, B, C, D):   
    
    top = (D[1] - C[1]) * (A[0] - C[0]) - (D[0] - C[0]) * (A[1] - C[1])
    bottom = (D[0] - C[0]) * (B[1] - A[1]) - (D[1] - C[1]) * (B[0] - A[0])
    if bottom != 0.0:
        offset = top / bottom
        if (offset >= 0 and offset <= 1):
            return offset
    
    return None

def getIntersection(A, B, C, D):
    t = calculateOffsets(A, B, C, D)
    u = calculateOffsets(C, D, A, B)
    
    if t and u:
        interp_x = lerp(A[0], B[0], t)
        interp_y = lerp(A[1], B[1], t)
        return (interp_x,interp_y)
                    
    return None

def isIntersection(A, B, C, D):
    t = calculateOffsets(A, B, C, D)
    u = calculateOffsets(C, D, A, B)
    
    return t and u

def make_track(parameters):
    return pygame.transform.smoothscale_by(pygame.image.load(parameters[0]).convert_alpha(), parameters[1]*world_pos)

def read_col_data(route):
    data = []
    
    with open(route, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((float(row['x'])*world_pos, float(row['y'])*world_pos))
    
    return data

def multi_point(point, scalar, divide = False):
    if divide:
        return (point[0] / scalar, point[1] / scalar)
    return (point[0] * scalar, point[1] * scalar)

def add_points(point1, point2, substract = False):
    if substract:
        return (point1[0] - point2[0], point1[1] - point2[1])
    return (point1[0] + point2[0], point1[1] + point2[1])

def render_text(screen, pos, text, size = 30, color = pygame.Color("Black"), bold = False, font = "Arial"):
    
    font_ = pygame.font.Font(None,(int)(size * world_pos))
    font_obj = font_.render(text , 1, color)
    font_rect = font_obj.get_rect(center = pos)
    screen.blit(font_obj, font_rect)
            
            
class Button(object):
    """A fairly straight forward button class."""
    def __init__(self,rect,color,function,**kwargs):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {"text" : None,
                    "font" : pygame.font.Font(None,(int)(150 * world_pos)),
                    "call_on_release" : True,
                    "hover_color" : None,
                    "clicked_color" : None,
                    "font_color" : pygame.Color("white"),
                    "hover_font_color" : None,
                    "clicked_font_color" : None,
                    "click_sound" : None,
                    "hover_sound" : None}
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)

    def check_event(self,event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self,event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self,event):
        if self.clicked and self.call_on_release:
            self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self,surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        #surface.fill(pygame.Color("black"),self.rect)
        surface.fill(color,self.rect.inflate(-4,-4))
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text,text_rect)