import gym
from gym import spaces
import pygame
import numpy as np
import pygame, random
from pygame.locals import *
import random



#For test code 
#from Object import Ball, Rectangle, Collision

#For test AI
from ball_world_game.envs.Object import Ball, Rectangle, Collision

#For setup.py install
#from ball_world_game.envs.Object import Ball, Rectangle, Collision


class CustomEnv(gym.Env):
    metadata = { "render_fps": 120, "render_modes":['human', 'rgb_array']}
    
    def __init__(self, render_mode='human'):
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
        #print(screen_lower_bound.shape)
        lower_bound.append(screen_lower_bound)
        screen_upper_bound = np.array([450, 800, 450, 800]).repeat(2+10).reshape(-1, 4)
        upper_bound.append(screen_upper_bound)

        lower_bound = np.concatenate(lower_bound, axis=None)
        upper_bound = np.concatenate(upper_bound, axis=None)
        #print(lower_bound.shape, upper_bound.shape)
        self.num_of_obs = 5
        self.num_of_br = 5
        self.observation_space = spaces.box.Box(low=lower_bound, high=upper_bound, shape=((3+self.num_of_obs+self.num_of_br)* 4,), dtype=np.float32)
        
        self.SCREEN_WIDTH = 450
        self.SCREEN_HEIGHT = 800

        
        #self.render_mode = bool(int(input("Input the render mode: ")))     # need to change to input (later) 
        self.render_mode = render_mode
        self.clock = None
        self.screen = None
        self.rng = self.np_random

        pygame.font.init()
        self.font = pygame.font.Font("ball_world-game/ball_world_game/envs/breakout_font.ttf",20)
        #print(self.font)

        self.previous_obs_collision = -1
        self.cul_reward = 0
        self.mex_speed = 10


    def _get_info(self):
        return {"relative pos": ((np.array(self.ball.rect.center) - np.array(self.bar.rect.center))**2).sum(),
                }
    def render(self):
        
        if self.clock is None and self.render_mode == 'human':
            self.clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))
        self.ball.draw(self.screen)
        self.bar.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for brake in self.brake:
            brake.draw(self.screen)

        ### Show score and the speed
        speed_show = self.font.render('Speed' + '{:.2f}'.format(np.sqrt(self.ball.speed[0]**2 + self.ball.speed[1]**2)), True, (255,255,0))
        v_speed_show = self.font.render('Vertical Speed' + str(self.ball.speed[1]), False, (255,255,0))
        self.screen.blit(speed_show, (150,10))

        if self.render_mode == 'human':
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

        for brake in self.brake:
            one_obs_coor = np.array(brake.rect)
            one_obs_coor[2:4] += brake.rect[0:2]
            state.append(one_obs_coor)
        
        state = np.concatenate(state,0).reshape(-1,4)

        #print('state:', state.shape)
        return state.reshape(-1)

    
    def step(self, action):
        self.bar.update(action)
        bounce = self.ball.update(self.bar)
        hit_brake = 0
        for br in self.brake:
            if br.update(self.ball,self.rng):
                new_brake = Rectangle.Brake(self.SCREEN_WIDTH, self.rng)
                while pygame.sprite.spritecollide(new_brake, self.obstacles, False) or pygame.sprite.spritecollide(new_brake, self.brake, False):
                    new_brake = Rectangle.Brake(self.SCREEN_WIDTH, self.rng)
                self.brake.add(new_brake)
                hit_brake += 1

        self.previous_obs_collision = Collision.ball_collide_with_obstacles(self.ball, self.obstacles, self.previous_obs_collision, self.rng)


        terminated = not self.ball.survive
        reward = bounce if not terminated else -10000
        reward += hit_brake * 1000
        if self.previous_obs_collision != -1:
            reward -= 1000
        observation = self.get_state()
        info = self._get_info()

        if self.render_mode == 'human':
            self.render()
        #print(observation.shape)

        return observation, reward, terminated, info


        

    def reset(self, seed=1, options=None):
        super().reset(seed=seed)
        """if self.render_mode == 'human':
            self.render()"""
        # generate screen
        if self.screen == None:
            pygame.init()
            if self.render_mode == 'human':
                pygame.display.init()
                display_flag = pygame.SHOWN if self.render_mode else pygame.HIDDEN
                self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT], flags=display_flag)
            else:
                self.screen = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))


        # Need to further check self. 
        self.ball = Ball.Ball(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.rng)
        self.bar = Rectangle.ControlBar((225, 650), 70, 10, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.obstacles = [Rectangle.Obstacle(self.SCREEN_WIDTH, self.rng) for i in range(self.num_of_obs)]
        self.brake = []
        for i in range(self.num_of_br):
            brake = Rectangle.Brake(self.SCREEN_WIDTH, self.rng)
            while pygame.sprite.spritecollide(brake, self.obstacles, False) or pygame.sprite.spritecollide(brake, self.brake, False):
                brake = Rectangle.Brake(self.SCREEN_WIDTH, self.rng)
            self.brake.append(brake)
        self.brake = pygame.sprite.Group(self.brake)

        state = self.get_state()
        info =self._get_info()

        
        self.render()
              

        return state  #ball, bar and obstaicles cooridnate

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()





######### Test code ########
if __name__ == '__main__':
    #print("HI")
    test = CustomEnv()
    running = True

    test.reset()
    while running: 
        pressed_keys = pygame.key.get_pressed()
        action = 1
        if pressed_keys[K_LEFT]:
            action = 0
        if pressed_keys[K_RIGHT]:
            action = 2

        ob, rew, terminated, info = test.step(action)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    test.close()
                    
        if terminated == True:
            test.close()
            running = False           