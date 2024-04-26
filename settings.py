import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

res_multiplier = true_res[0]/2880

max_speed = 75600 * res_multiplier
max_back_speed = -27000* res_multiplier
acceleration = 180 * res_multiplier
decceleration = 136 * res_multiplier
braking = 540 * res_multiplier
activate_turning_speed = 60 * res_multiplier
turning_speed = 90