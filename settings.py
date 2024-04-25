import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))

max_speed = 21
max_back_speed = -7.5
acceleration = 0.05
decceleration = 0.038
braking = 0.15
activate_turning_speed = 1
turning_speed = 1.5   