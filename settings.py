import ctypes
from pygame import Color

# UNITS
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

world_pos = true_res[0]/2880

# CAR
max_speed = 2000 * world_pos
max_back_speed = -400 * world_pos
acceleration = 400 * world_pos
decceleration = 180 * world_pos
braking = 500 * world_pos
activate_turning_speed = 20 * world_pos
turning_speed = 90
car_scale = 0.06

# TRACKS
tracks = [("images/maintrack5.png", 3.5, (3650*world_pos, 2600*world_pos)),("images/maintrack6.png", 3.5, (3900*world_pos, 2700*world_pos))]

# DEBUG MODE
debug = True

text_color = Color("Purple")
raycast_color = Color("Red")
collider_color = Color("Red")