import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

res_multiplier = true_res[0]/2880

max_speed = 21 * res_multiplier
max_back_speed = -7.5 * res_multiplier
acceleration = 0.05 * res_multiplier
decceleration = 0.038 * res_multiplier
braking = 0.15 * res_multiplier
activate_turning_speed = 1 * res_multiplier
turning_speed = 1.5   