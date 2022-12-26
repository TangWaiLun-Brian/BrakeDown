import pygame, random
from pygame.locals import *
import random
import numpy as np

class Ball(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen, rng, initial_speed):
        super().__init__()
        self.x_cor = 225
        self.y_cor = 420
        self.x_cor_float = self.x_cor
        self.y_cor_float = self.y_cor


        self.img = pygame.image.load('ball_world-game/ball_world_game/envs/Image/cannon_ball_10_green.png')
        self.image = self.img.convert()
        self.rect = self.img.get_rect()
        screen.blit(self.img, (self.x_cor, self.y_cor))

        self.survive = True
        self.win = False
        self.too_fast = False
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        # initialize the speed x
        init_speed_x = rng.uniform(-1,1)
        # Calculate speed y with respect to speed x
        init_speed_y = np.sqrt(initial_speed**2 - init_speed_x**2)
        self.speed = [init_speed_x, init_speed_y]
        self.initial_speed = initial_speed
        self.count = 0
        #for testing
        #self.speed = [0, 0]




    def update(self,  bar, sound_hit_bar):

        # collision with boundary
        if self.rect.left < 0 and self.speed[0] <= 0:
            self.speed[0] *= -1
        elif self.rect.right > self.SCREEN_WIDTH and self.speed[0] >= 0:
            self.speed[0] *= -1
        if self.rect.top <= 0 and self.speed[1] <= 0:
            self.speed[1] *= -1
        elif self.rect.bottom >= self.SCREEN_HEIGHT:
            self.survive = False
        # bounce is used to record if the ball collides with bar (for reward part)
        bounce = 0
        # collision with bar
        if self.rect.bottom >= bar.rect.top and self.rect.top <= bar.rect.bottom and self.rect.centerx >= bar.rect.left and self.rect.centerx <= bar.rect.right:
            bounce = 1
            if sound_hit_bar is not None:
                sound_hit_bar.play()
            sign = 1 if self.rect.centerx - bar.rect.centerx > 0 else -1
            self.init_total_speed_squa = self.speed[0]**2 + self.speed[1]**2
            #self.dis_with_center = self.rect.centerx - bar.rect.centerx if abs(self.rect.centerx - bar.rect.centerx) > 3 else (abs(self.rect.centerx - bar.rect.centerx) / (self.rect.centerx - bar.rect.centerx)) * 3
            # Calculate the rebound angle according to the contact point
            self.rebounce_angle = ((self.rect.centerx - bar.rect.centerx + (sign * 3)) / (bar.rect.right-bar.rect.left) + (sign * 3))* np.pi /1.5
            self.speed[0] = np.sqrt(self.init_total_speed_squa) * np.sin(self.rebounce_angle)
            self.speed[1] = np.sqrt(self.init_total_speed_squa) * np.cos(self.rebounce_angle) * -1

        # adjust the position of ball
        # use float to record the actual position but display with a discrete one
        self.x_cor_float += self.speed[0]
        self.y_cor_float += self.speed[1]
        self.rect.centerx = int(self.x_cor_float)
        self.rect.centery = int(self.y_cor_float)

        # calculate ball speed and see if it exceeds the upper bound
        self.total_speed = np.sqrt(self.speed[0]**2 + self.speed[1]**2)
        if self.total_speed >= 15:
            self.survive = False
            self.too_fast = True
        # player wins if speed is lower than lower bound
        if self.total_speed < 1 and self.total_speed > 0:
            self.win = True
        # player also wins if the ball hits brake 5 times
        elif self.count >= 5:
            self.win = True
        # gives the agent reward if bar's x cor is close to ball's x cor
        dist = self.SCREEN_WIDTH - abs(self.rect.centerx - bar.rect.centerx)
        # setting 0 as the coefficient means we don't use bounce reward for now
        return bounce * 0 + dist

    def draw(self, screen):
        screen.blit(self.img, (self.rect.centerx, self.rect.centery))