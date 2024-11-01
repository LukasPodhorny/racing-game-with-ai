from gymnasium import Env
from gymnasium.spaces import Box, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *

class RacingEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, render_mode=None, size=5):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        pygame.init()
        pygame.display.set_caption("racing game training environment")

        self.screen = pygame.display.set_mode(true_res, pygame.FULLSCREEN, vsync=1)
        self.h_w = self.screen.get_width() / 2
        self.h_h = self.screen.get_height() / 2
        self.bg_color = (154, 218, 111)

        self.cam = camera((0, 0))

        self.current_track = random.randint(0, len(tracks) - 1)
        self.track_img = make_track(tracks[self.current_track])
        self.col_line_count = 2

        self.col_data = []
        for i in range(0, self.col_line_count):
            self.col_data.append(read_col_data("collider_data/track_col_data_" + str(self.current_track) + "_" + str(i)))
        
        self.rewardgates_data = read_col_data("collider_data/track_rewardgate_data_" + str(self.current_track) + "_0")
        self.car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale * world_pos)
        self.train_car = car_module.car_object(self.car_img, tracks[self.current_track][2], angle=tracks[self.current_track][3])
        self.max_ray_length = 1500
        self.max_ray_count = 25
        self.spread_angle = 120

        self.getTicksLastFrame = None
        self.last_gate = 0
        self.last_episode_t = 0

        self.action_space = MultiDiscrete([3, 3])
        self.observation_space = Box(low=0, high=self.max_ray_length, shape=(self.max_ray_count,), dtype=np.float32)

        self.car_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))    
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin, self.max_ray_length, self.max_ray_count, self.spread_angle, self.current_track, self.cam, debug_mode=True)
        self.state = self.lengths

        self.episode_length = 60 

    def step(self, action):
        t = pygame.time.get_ticks()
        if self.getTicksLastFrame:
            deltaTime = (t - self.getTicksLastFrame) / 1000.0
        else:
            deltaTime = 0.015

        self.getTicksLastFrame = t
        time = (t - self.last_episode_t) / 1000

        self.train_car.update_pos(deltaTime, action)
        self.cam.pos = (self.train_car.x - self.h_w, self.train_car.y - self.h_h)
        self.car_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin, self.max_ray_length, self.max_ray_count, self.spread_angle, self.current_track, self.cam, debug_mode=True)
        game_over = self.train_car.check_collisions(self.car_origin, self.cam, self.current_track)
        win = self.train_car.check_win(self.car_origin, self.cam, self.current_track)

        self.state = self.lengths
        self.episode_length -= (1 * deltaTime)
        
        reward = (self.train_car.speed * deltaTime) * 10

        gate_check = self.train_car.check_reward_gates(self.car_origin, self.cam, self.rewardgates_data)
        
        if gate_check:
            self.rewardgates_data.pop(gate_check[0])
            self.rewardgates_data.pop(gate_check[1])
            reward += 1000
        
        if game_over:
            reward -= 15000
        
        if win:
            reward += 50000
        
        done = self.episode_length <= 0 or game_over or win
        
        return self.state, reward, done, False, {}

    def render(self):
        self.screen.fill(self.bg_color)
        self.cam.blit(self.screen, self.track_img, (0, 0))
        self.train_car.show(self.cam, self.screen)
        
        for i in range(0, len(self.col_data[0]) - 1):
            pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[0][i]), self.cam.r_pos(self.col_data[0][i + 1]), 2)
        for i in range(0, len(self.col_data[1]) - 1):
            pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[1][i]), self.cam.r_pos(self.col_data[1][i + 1]), 2)
        for i in range(0, (int)(len(self.rewardgates_data) / 2)):
            pygame.draw.line(self.screen, pygame.Color("Blue"), self.cam.r_pos(self.rewardgates_data[2 * i]), self.cam.r_pos(self.rewardgates_data[2 * i + 1]), 2)
        
        pygame.draw.circle(self.screen, pygame.Color("White"), self.car_origin, 3)
        
        if self.intersections:
            i = 0  
            for intersection in self.intersections:
                pygame.draw.line(self.screen, raycast_color, self.car_origin, intersection, 1)
                if self.lengths[i] < self.max_ray_length:
                    pygame.draw.circle(self.screen, pygame.Color("White"), intersection, 5)
                i += 1

        pygame.display.update()
    
    def reset(self, options=None, seed=random.randint(0, 10000)):
        super().reset()
        self.last_episode_t = pygame.time.get_ticks()
        self.last_reward_gate = 0

        self.current_track = random.randint(0, len(tracks) - 1)
        self.track_img = make_track(tracks[self.current_track])

        self.col_data = []    
        for i in range(0, self.col_line_count):
            self.col_data.append(read_col_data("collider_data/track_col_data_" + str(self.current_track) + "_" + str(i)))
        
        self.rewardgates_data = read_col_data("collider_data/track_rewardgate_data_" + str(self.current_track) + "_0")
        
        self.train_car.reset(tracks[self.current_track][2], tracks[self.current_track][3])
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin, self.max_ray_length, self.max_ray_count, self.spread_angle, self.current_track, self.cam, debug_mode=True)
        self.state = self.lengths

        self.episode_length = 60 
        return self.state, {}


def make_env(env_id, rank, seed=0):
    def _init():
        env = RacingEnv()
        env.reset(seed=seed + rank)
        return env
    return _init

def train(timesteps, name, env):
    log_path = os.path.join('Training', 'Logs')
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path, ent_coef=0.01)
    model.learn(timesteps, progress_bar=True)
    model_path = os.path.join('Training', 'Saved Models', name)
    model.save(model_path)

def test_model(name, episodes=5):
    env = RacingEnv(render_mode = "human")

    path = os.path.join('Training', 'Saved Models', name)
    model = PPO.load(path)

    for episode in range(0, episodes):
        obs, info = env.reset()
        done = False
        score = 0

        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            env.render()

            action, _states = model.predict(obs)
            obs, reward, done, truncated, info = env.step(action)
            score += reward

        print('Episode:{} Score:{}'.format(episode + 1, score))

    env.close()




#----------------CHOOSE WHAT TYPE OF ACTION YOU WANT TO DO HERE----------------

# VECTORIZED ENVIROMENT
'''
if __name__ == "__main__":
    num_envs = 10
    envs = SubprocVecEnv([make_env("RacingEnv", i) for i in range(num_envs)])
    train(500_000, "500_000_selfdrivingtest", envs)
'''
    
# NON-VECTORIZED ENVIROMENT
# env = RacingEnv(render_mode="human")
# train(10_000_000,"10_000_000selfdrivingtest", env)
#
# TESTING    
# test_model("500_000_selfdrivingtest")
# test_env(env)
# evaluate_policy(PPO.load(os.path.join('Training', 'Saved Models', "500_000_selfdrivingtest")),env, render = True)
#    
# VIEWING LOGS
# tensorboard --logdir="Training/Logs/PP0_38"

#----------------CHOOSE WHAT TYPE OF ACTION YOU WANT TO DO HERE----------------