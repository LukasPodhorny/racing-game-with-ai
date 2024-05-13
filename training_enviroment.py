from gymnasium import Env
from gymnasium.spaces import Box, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import sys
import car_module
import pygame
from pygame.locals import *
from camera import *
from settings import *
from usefulfunctions import *


# Enviroment made specifically for this racing game
class RacingEnv(Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    def __init__(self, render_mode=None, size=5):
        
        # Initialization
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        pygame.init()
        pygame.display.set_caption("racing game training enviroment")

        self.screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN,vsync=1)
        self.h_w = self.screen.get_width()/2
        self.h_h = self.screen.get_height()/2
        self.bg_color = (154, 218, 111)

        self.cam = camera((0,0))

        current_track = random.randint(0,len(tracks)-2)
        self.track_img = make_track(tracks[current_track])
        self.col_line_count = 2

        self.col_data = []
        for i in range(0, self.col_line_count):
            self.col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))
        
        
        self.rewardgates_data = read_col_data("collider_data/track_rewardgate_data_"+str(current_track)+"_0")
        self.car_img = pygame.transform.smoothscale_by(pygame.image.load("images/car.png").convert_alpha(), car_scale*world_pos)
        self.train_car = car_module.car_object(self.car_img, tracks[current_track][2], angle = tracks[current_track][3])
        self.max_ray_length = 1500
        self.max_ray_count = 25
        self.spread_angle = 120

        self.getTicksLastFrame = None
        self.last_gate = 0
        self.last_episode_t = 0
        
        # Can press one of four keys: w, a, s, d but not both, because for example pressing w and s, cuz this is just doing nothing
        self.action_space = MultiDiscrete([3,3])
       
        # Raycast length array space
        self.observation_space = Box(low = 0, high = self.max_ray_length, shape = (self.max_ray_count,), dtype=np.float32)

        # Set start raycast for observations and so on
        self.car_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))    
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin,self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode=True)
        self.state = self.lengths

        # Set episode length
        self.episode_length = 60 
        
    def step(self, action):

        # calculating deltatime and time
        t = pygame.time.get_ticks()
        if self.getTicksLastFrame:
            deltaTime = (t - self.getTicksLastFrame) / 1000.0
        else:
            deltaTime = 0.015

        self.getTicksLastFrame = t
        time = (t - self.last_episode_t)/1000


        # updating the game
        self.train_car.update_pos(deltaTime, action)
        self.cam.pos = (self.train_car.x - self.h_w, self.train_car.y - self.h_h)
        self.car_origin = self.cam.r_pos((self.train_car.x, self.train_car.y))
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin, self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode = True)
        game_over = self.train_car.check_collisions(self.car_origin, self.col_data, self.cam)
        win = self.train_car.check_win(self.car_origin, self.cam)


        # Setting new state, cuz it was updated
        self.state = self.lengths


        # Reduce episode length by 1 second
        self.episode_length -= (1 * deltaTime)
        
        # Calculating rewards
        reward = (self.train_car.speed * deltaTime) * 10

        gate_check = self.train_car.check_reward_gates(self.car_origin,self.cam,self.rewardgates_data)
        
        if gate_check:
            self.rewardgates_data.pop(gate_check[0])
            self.rewardgates_data.pop(gate_check[1])

            reward += 1000
        
        if game_over:
            reward -= 15_000
        
        if win:
            reward += 30_000
        

        # Check if the episode is done
        if self.episode_length <= 0 or game_over or win: 
            done = True
        else:
            done = False
        
        
        # Return step information
        return self.state, reward, done, False, {}

    def render(self):
        
        # drawing background first
        self.screen.fill(self.bg_color)
        self.cam.blit(self.screen, self.track_img, (0,0))
        

        # drawing objects
        self.train_car.show(self.cam, self.screen)
        
        
        # drawing gizmos for debugging
        car_col_data = read_col_data("collider_data/car_col_data_0_0")
        
        # drawing track collider boundaries
        for i in range(0,len(self.col_data[0])-1):
            pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[0][i]), self.cam.r_pos(self.col_data[0][i+1]), 2)
        for i in range(0,len(self.col_data[1])-1):
            pygame.draw.line(self.screen, pygame.Color("Red"), self.cam.r_pos(self.col_data[1][i]), self.cam.r_pos(self.col_data[1][i+1]), 2)
        for i in range(0,(int)(len(self.rewardgates_data)/2)):
            pygame.draw.line(self.screen, pygame.Color("Blue"), self.cam.r_pos(self.rewardgates_data[2*i]), self.cam.r_pos(self.rewardgates_data[2*i+1]), 2)
        

        # drawing car collider
        for i in range(0,(int)(len(car_col_data)/2)):
            pygame.draw.line(self.screen, pygame.Color("Green"), add_points(self.car_origin, car_col_data[2*i]), add_points(self.car_origin, car_col_data[2*i+1]), 2)
        pygame.draw.circle(self.screen, pygame.Color("White"), self.car_origin, 3)
        

        # drawing raycast
        if self.intersections:
            i = 0  
            for intersection in self.intersections:
                pygame.draw.line(self.screen, raycast_color, self.car_origin, intersection, 1)
                if self.lengths[i] < self.max_ray_length:
                    pygame.draw.circle(self.screen, pygame.Color("White"), intersection, 5)
                i += 1

        pygame.display.update()
    

    # Restarting the enviroment
    def reset(self, seed = random.randint(0,10000), options = None):
        super().reset(seed=seed)

        self.last_episode_t = pygame.time.get_ticks()
        self.last_reward_gate = 0

        current_track = random.randint(0,len(tracks)-2)
        self.track_img = make_track(tracks[current_track])

        self.col_data = []    
        for i in range(0, self.col_line_count):
            self.col_data.append(read_col_data("collider_data/track_col_data_" + str(current_track) + "_" + str(i)))
        
        self.rewardgates_data = read_col_data("collider_data/track_rewardgate_data_"+str(current_track)+"_0")
        
        self.train_car.reset(tracks[current_track][2], tracks[current_track][3])
        self.lengths, self.intersections = self.train_car.raycast(self.car_origin,self.max_ray_length, self.max_ray_count, self.spread_angle, self.col_data, self.cam, debug_mode=True)
        self.state = self.lengths

        # Reset episode length
        self.episode_length = 60 
        return self.state, {}



# function for testing enviroment on random actions
def test_env(env, episodes = 5):

    for episode in range(0,episodes):
        state, info = env.reset()
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

def test_model(name, env, episodes = 5):
    path = os.path.join('Training', 'Saved Models', name)
    model = PPO.load(path)

    for episode in range(0,episodes):
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
            obs, reward, done, trancustated, info = env.step(action)
            score += reward

        print('Episode:{} Score:{}'.format(episode+1, score))

    env.close()

def train(timesteps, name, env):
    log_path = os.path.join('Training', 'Logs')
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path, ent_coef=0.01)
    model.learn(timesteps)
    model_path = os.path.join('Training', 'Saved Models', name)
    model.save(model_path)


#----------------CHOOSE WHAT TYPE OF ACTION YOU WANT TO DO HERE----------------

env = RacingEnv(render_mode = "human")

# train(5_000_000,"5_000_000selfdrivingtest", env)
test_model("5_000_000selfdrivingtest", env)
# test_env(env)
# evaluate_policy(PPO.load(os.path.join('Training', 'Saved Models', "5_000_000selfdrivingtest")),env, render = True)
# tensorboard --logdir="Training/Logs/PP0_38"

#----------------CHOOSE WHAT TYPE OF ACTION YOU WANT TO DO HERE----------------
