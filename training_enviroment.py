import gymnasium
from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *

# pygame.init()
# pygame.display.set_caption("racing game training enviroment")

# screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
# h_w = screen.get_width()/2
# h_h = screen.get_height()/2
# bg_color = (154, 218, 111)

# cam = camera((0,0), 1)
# car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)

# train_car = car_module.car_object(car_img)

# setting up current track and colliders for the track
# current_track = random.randint(0,len(tracks))
# track_img = make_track(tracks[current_track])
# col_line_count = 
# col_data = []
# for i in range(0, col_line_count):
#     col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))

# getTicksLastFrame = 0
 
# fps rendering for debugging
# debug_font = pygame.font.SysFont("Arial" , (int)(30 * world_pos) , bold = True)
# def render_fps():
#     fps_str = "fps: " + str(int(fpsClock.get_fps()))
#     fps_tex = debug_font.render(fps_str , 1, text_color)
#     screen.blit(fps_tex,(0,0))
    

# calculating deltaTime
# t = pygame.time.get_ticks()
# deltaTime = (t - getTicksLastFrame) / 1000.0
# getTicksLastFrame = t

# GAME LOGIC START

# updating
# player_car.update_pos(deltaTime)
# cam.pos = (player_car.x - h_w, player_car.y - h_h)
# raycast_origin = cam.r_pos((player_car.x, player_car.y))
# lengths, intersections = player_car.raycast(raycast_origin, 1500, 25, 120, col_data, cam, debug_mode = True)
# game_over = player_car.check_collisions(raycast_origin, col_data, cam)
# win = player_car.check_win(raycast_origin, cam)

#if game_over:
#    player_car.reset((1900 * world_pos, 1900 * world_pos))
#if win:
#    pygame.quit()
#    sys.exit()

class RacingEnv(Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    def __init__(self, render_mode=None, size=5):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        pygame.init()
        pygame.display.set_caption("racing game training enviroment")

        self.screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
        self.h_w = self.screen.get_width()/2
        self.h_h = self.screen.get_height()/2
        self.bg_color = (154, 218, 111)

        self.cam = camera((0,0), 1)

        
        current_track = random.randint(0,len(tracks)-2)
        self.track_img = make_track(tracks[current_track])
        self.col_line_count = 2

        self.col_data = []
        for i in range(0, self.col_line_count):
            self.col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))
        
        
        self.rewardgates_data = read_col_data("collider_data/track_rewardgate_data_"+str(current_track)+"_0")
        self.car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)
        self.train_car = car_module.car_object(self.car_img, tracks[current_track][2])
        self.max_ray_length = 1500
        self.max_ray_count = 25
        self.spread_angle = 120

        
        self.getTicksLastFrame = 1000
        
        # Can press one of four keys: w, a, s, d 
        self.action_space = Box(0, 1, shape = (2,2), dtype = np.int32) # * fix after installing libraries to int
       
        # Raycast length array space
        self.observation_space = Box(low=0, high= self.max_ray_length, shape = (self.max_ray_count,), dtype=np.float32)

        # Set start temp
        self.raycast_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))    
        self.lengths, self.intersections = self.train_car.raycast(self.raycast_origin,self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode=True)
        self.state = self.lengths

        # Set episode length to 60 seconds
        self.episode_length = 60 
        
    def step(self, action):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.getTicksLastFrame) / 1000.0

        self.getTicksLastFrame = t


        # updating alert you need to add action as argument to update the car
        self.train_car.update_pos(deltaTime, True, action)
        self.cam.pos = (self.train_car.x - self.h_w, self.train_car.y - self.h_h)
        self.raycast_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))
        self.lengths, self.intersections = self.train_car.raycast(self.raycast_origin, self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode = True)
        self.game_over = self.train_car.check_collisions(self.raycast_origin, self.col_data, self.cam)
        self.win = self.train_car.check_win(self.raycast_origin, self.cam)

        self.state = self.lengths

        # Reduce shower length by 1 second
        self.episode_length -= 1 * deltaTime 
        
        # Calculate reward
        reward = -1 * deltaTime

        gate_check = self.train_car.check_reward_gates(self.raycast_origin,self.cam,self.rewardgates_data)
        if gate_check != None:
            print(gate_check)
            print(len(self.rewardgates_data))
            self.rewardgates_data.pop(gate_check[0])
            self.rewardgates_data.pop(gate_check[1])

            reward += 50
        
        if self.game_over:
            reward -= 700
        
        if self.win:
            reward += 700
        
        # Check if shower is done
        if self.episode_length <= 0 or self.game_over or self.win: 
            done = True
        else:
            done = False
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, False, info

    def render(self):
        
        # drawing background first
        self.screen.fill(self.bg_color)
        self.cam.blit(self.screen, self.track_img, (0,0))
        
        # drawing
        self.train_car.show(self.cam, self.screen)
        
        # rendering gizmos for debugging
        if debug:
            car_col_data = read_col_data("collider_data/car_col_data_0_0")
            # drawing track collider boundaries
            for i in range(0,len(self.col_data[0])-1):
                pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[0][i]), self.cam.r_pos(self.col_data[0][i+1]), 2)
            for i in range(0,len(self.col_data[1])-1):
                pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[1][i]), self.cam.r_pos(self.col_data[1][i+1]), 2)
            for i in range(0,len(car_col_data)-1):
                pygame.draw.line(self.screen, pygame.Color("Red"), add_points(self.raycast_origin, car_col_data[i]), add_points(self.raycast_origin, car_col_data[i + 1]), 2)
            pygame.draw.circle(self.screen, pygame.Color("White"), self.raycast_origin, 5)
            
            # drawing raycast
            if self.intersections:
                i = 0  
                for intersection in self.intersections:
                    pygame.draw.line(self.screen, raycast_color, self.raycast_origin, intersection, 1)
                    if self.lengths[i] < 2000:
                        pygame.draw.circle(self.screen, pygame.Color("White"), intersection, 5)
                    i += 1

        pygame.display.update()
    
    def reset(self, seed = None, options = None):
        super().reset(seed=seed)
        
        current_track = random.randint(0,len(tracks)-2)
        self.track_img = make_track(tracks[current_track])

        col_data = []
        
        for i in range(0, self.col_line_count):
            col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))
        
        self.train_car.reset(tracks[current_track][2])
        self.lengths, self.intersections = self.train_car.raycast(self.raycast_origin,self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode=True)
        self.state = self.lengths

        # Reset episode length
        self.episode_length = 60 
        return self.state, {}

env = RacingEnv(render_mode = "human")

def test():
    
    episodes = 5

    for episode in range(0,episodes):
        state = env.reset()
        done = False
        score = 0
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            env.render()
            action = env.action_space.sample()
            n_state, reward, done, trancustated, info = env.step(action)
            score += reward

        print('Episode:{} Score:{}'.format(episode+1, score))

    env.close()

def train():
    log_path = os.path.join('Training', 'Logs')
    
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
    model.learn(total_timesteps=10000)
    
    model_path = os.path.join('Training', 'Saved Models', '400000_PPO_Self_Driving')
    model.save(model_path)


log_path = os.path.join('Training', 'Logs')
model_path = os.path.join('training_data', '400000_self_driving')
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
model.load(model_path)

episodes = 5

for episode in range(0,episodes):
    obs = env.reset()
    done = False
    score = 0
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        env.render()
        action, _states = model.predict(np.ndarray((env.max_ray_count,)), obs, deterministic = True)
        print(action)
        print(obs)
        obs, reward, done, truncated, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode+1, score))
env.close()

