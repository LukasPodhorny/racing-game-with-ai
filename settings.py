import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

res_multiplier = true_res[0]/2880

max_speed = 1260 * res_multiplier
max_back_speed = -450 * res_multiplier
acceleration = 3 * res_multiplier
decceleration = 2.28 * res_multiplier
braking = 9 * res_multiplier
activate_turning_speed = 60 * res_multiplier
turning_speed = 90   