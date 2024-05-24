import ctypes
from pygame import Color

# UNITS
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

# essential for same sizing and moving on differently sized screens
world_pos = true_res[0]/2880

# CAR
max_speed = 2000 * world_pos
max_back_speed = 0 * world_pos # -400 for driving back
acceleration = 400 * world_pos
decceleration = 180 * world_pos
braking = 500 * world_pos
activate_turning_speed = 50 * world_pos
turning_speed = 90
car_scale = 0.06

# TRACKS
tracks = [("images/track1.png", 3.5, (3650*world_pos, 2550*world_pos), -35),("images/track2.png", 3.5, (2800*world_pos, 1400*world_pos), 0)]

# DEBUG
debug = False

text_color = Color("Purple")
raycast_color = Color("Red")
collider_color = Color("Red")

# BUTTON
BGCOLOR = (154, 218, 111)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)

BUTTON_STYLE = {"hover_color" : BGCOLOR,
                "clicked_color" : BGCOLOR,
                "clicked_font_color" : BLACK,
                "hover_font_color" : BLACK,}
