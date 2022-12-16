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
        self.screen = None

        self.previous_obs_collision = -1
        self.cul_reward = 0



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
            self.clock.tick(240)
            pygame.display.flip()


    def get_state(self):
        state = []
        state.append([self.ball.speed[0], self.ball.speed[1], 0, 0])
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

        print(state.shape)
        return state

    
    def step(self, action):
        self.bar.update(action)
        self.ball.update(self.bar)
        self.previous_obs_collision = Collision.ball_collide_with_obstacles(self.ball, self.obstacles, self.previous_obs_collision)

        terminated = not self.ball.survive
        reward = 10 if not terminated else -10000
        observation = self.get_state()


        if self.render_mode == True:
            self.render()

        return observation, reward, terminated


        

    def reset(self):
        # generate screen
        if self.screen == None:
            print("HI")
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        # Need to further check self. 
        self.ball = Ball.Ball(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        self.bar = Rectangle.ControlBar((225, 650), 450, 10, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.obstacles = [Rectangle.Obstacle(self.SCREEN_WIDTH) for i in range(10)]


        state = self.get_state()
        

        
        self.render()
              

        return state #ball, bar and obstaicles cooridnate

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()


ball_world = CustomEnv()
ball_world.reset()

while True:
    
    
    pressed_keys = pygame.key.get_pressed()
    action = 1
    if pressed_keys[K_LEFT]:
        action = 0
    if pressed_keys[K_RIGHT]:
        action = 2
    
    ob, rew, term = ball_world.step(action)

    if term == True:
        ball_world.close()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                ball_world.close()
                #pygame.quit()
