import gym
from gym import spaces
import pygame
import numpy as np
import pygame, random
from pygame.locals import *
import random

class CustomEnv(gym.Env):
    metadata = { "render_fps": 120}
    
    def __init__(self, render_mode=None):
        super().__init__()
        self.action_space = gym.space.Discrete(3)           #left, right, stay
        
        
        self.SCREEN_WIDTH = 450
        self.SCREEN_HEIGHT = 800

        self.render_mode = True     # need to change to input (later)
        self.clock = None
        self.window = None
        pass

    def step(self, action):  
        if action in self.action_space():
            self.render()
        state = 1    
        reward =  1           
        done = True
        info = {}

        if self.render_mode == True:
            self.rend
        return state, reward, done, info

    def render(self):
        


        if self.clock is None and self.render_mode == "True":
            self.clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))


    def reset(self):
        # generate screen
        if self.window == None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        # Need to further check self. 
        self.ball = Ball(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        self.bar = ControlBar((225, 650), 450, 10)
        self.obstacles = [Obstacle() for i in range(10)]

        if self.render_mode == True:
            self.render()

        return state #ball, bar and obstaicles cooridnate

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
