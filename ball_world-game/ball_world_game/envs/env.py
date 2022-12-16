import gym
from gym import spaces
import pygame
import numpy as np
import pygame, random
from pygame.locals import *
import random
#from Object import Ball, Rectangle, Collision
from ball_world_game.envs.Object import Ball, Rectangle, Collision

class CustomEnv(gym.Env):
    metadata = { "render_fps": 120}
    
    def __init__(self, render_mode=True):
        super().__init__()

        self.action_space = gym.spaces.Discrete(3)           #left, right, stay
        max_speed = 20
        upper_bound = []
        lower_bound = []

        speed_lower_bound = np.array([-max_speed, -max_speed, 0, 0]).reshape(1, 4)
        speed_upper_bound = np.array([max_speed, max_speed, 0, 0]).reshape(1, 4)

        lower_bound.append(speed_lower_bound)
        upper_bound.append(speed_upper_bound)

        screen_lower_bound = np.array([0, 0, 0, 0]).repeat(2+10).reshape(-1, 4)
        print(screen_lower_bound.shape)
        lower_bound.append(screen_lower_bound)
        screen_upper_bound = np.array([450, 800, 450, 800]).repeat(2+10).reshape(-1, 4)
        upper_bound.append(screen_upper_bound)

        lower_bound = np.concatenate(lower_bound, axis=None)
        upper_bound = np.concatenate(upper_bound, axis=None)
        print(lower_bound.shape, upper_bound.shape)
        self.observation_space = spaces.box.Box(low=lower_bound, high=upper_bound, shape=((3+10)* 4,), dtype=np.float32)
        
        self.SCREEN_WIDTH = 450
        self.SCREEN_HEIGHT = 800

        
        #self.render_mode = bool(int(input("Input the render mode: ")))     # need to change to input (later) 
        self.render_mode = render_mode
        self.clock = None
        self.screen = None
        self.rng = None

        self.previous_obs_collision = -1
        self.cul_reward = 0


    def _get_info(self):
        return {"ball pos": np.array(self.ball.rect.center),
                "bar pos": np.array(self.bar.rect.center)}
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
            self.clock.tick(CustomEnv.metadata['render_fps'])
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

        #print('state:', state.shape)
        return state.reshape(-1)

    
    def step(self, action):
        self.bar.update(action)
        self.ball.update(self.bar)
        self.previous_obs_collision = Collision.ball_collide_with_obstacles(self.ball, self.obstacles, self.previous_obs_collision, self.np_random)

        terminated = not self.ball.survive
        reward = 10 if not terminated else -10000
        observation = self.get_state()
        info = self._get_info()

        if self.render_mode == True:
            self.render()

        return observation, reward, terminated, False, info


        

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # generate screen
        if self.screen == None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        # Need to further check self. 
        self.ball = Ball.Ball(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        self.bar = Rectangle.ControlBar((225, 650), 70, 10, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.obstacles = [Rectangle.Obstacle(self.SCREEN_WIDTH, self.np_random) for i in range(10)]


        state = self.get_state()
        info =self._get_info()

        
        self.render()
              

        return state, info #ball, bar and obstaicles cooridnate

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
