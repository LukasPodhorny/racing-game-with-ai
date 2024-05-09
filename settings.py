import ctypes
from pygame import Color

# UNITS
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

world_pos = true_res[0]/2880

# CAR
max_speed = 2000 * world_pos
max_back_speed = 0 * world_pos # -400 ZMENENOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
acceleration = 400 * world_pos
decceleration = 180 * world_pos
braking = 500 * world_pos # UDELAT MENSI POKUD SE TO BUDE SPATNE TRENOVATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
activate_turning_speed = 50 * world_pos
turning_speed = 90
car_scale = 0.06

# TRACKS
tracks = [("images/maintrack5.png", 3.5, (3650*world_pos, 2550*world_pos), -35),("images/maintrack6.png", 3.5, (3650*world_pos, 2550*world_pos), -35)]

# DEBUG MODE
debug = False

text_color = Color("Purple")
raycast_color = Color("Red")
collider_color = Color("Red")

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