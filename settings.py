import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

res_multiplier = true_res[0]/2880

max_speed = 1260 * res_multiplier * 60
max_back_speed = -450 * res_multiplier * 60
acceleration = 3 * res_multiplier * 60
decceleration = 2.28 * res_multiplier * 60
braking = 9 * res_multiplier * 60
activate_turning_speed = 60 * res_multiplier * 60
turning_speed = 90   