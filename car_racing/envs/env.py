import gym
from gym import spaces
import pygame
import numpy as np
import pygame, random
from pygame.locals import *
import random
from Object import Ball, Rectangle, Collision

class CustomEnv(gym.Env):
    metadata = { "render_fps": 120}
    
    def __init__(self, render_mode=True):
        super().__init__()
        self.action_space = gym.spaces.Discrete(3)           #left, right, stay
        
        
        self.SCREEN_WIDTH = 450
        self.SCREEN_HEIGHT = 800

        
        #self.render_mode = bool(int(input("Input the render mode: ")))     # need to change to input (later) 
        self.render_mode = render_mode
        self.clock = None
        self.window = None

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
        
        
        if self.clock is None and self.render_mode == True:
            self.clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))
        self.ball.draw(self.screen)
        self.bar.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        if self.render_mode == True:
            pygame.display.update()
            self.clock.tick()
            pygame.display.flip()


    def get_state(self):
        state = []
        # ball_coor
        ball_coor_state = np.array(self.ball.rect)
        ball_coor_state[2:4] += self.ball.rect[0:2]
        state.append(ball_coor_state)

        #bar coor 
        bar_coor_state = np.array(self.bar.rect)
        bar_coor_state[2:4] += self.bar.rect[0:2]
        state.append(bar_coor_state)

        #obs_coor
        for obstacle in self.obstacles:
            one_obs_coor = np.array(obstacle.rect)
            one_obs_coor[2:4] += obstacle.rect[0:2]
            state.append(one_obs_coor)
        
        state = np.concatenate(state,0).reshape(-1,4)
        #print(state.shape)
        return state
        

    def reset(self):
        # generate screen
        if self.window == None:

            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        # Need to further check self. 
        self.ball = Ball.Ball(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        self.bar = Rectangle.ControlBar((225, 650), 450, 10, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.obstacles = [Rectangle.Obstacle(self.SCREEN_WIDTH) for i in range(10)]


        state = self.get_state()
        

        while True:
            self.render()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: 
                        pygame.quit()

        

        return state #ball, bar and obstaicles cooridnate

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()




ball_world = CustomEnv()
ball_world.reset()