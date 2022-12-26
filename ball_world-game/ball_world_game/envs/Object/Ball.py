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

        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (self.x_cor, self.y_cor), 5)
        self.survive = True
        self.win = False
        self.too_fast = False
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        init_speed_x = rng.uniform(-1,1)
        #init_speed_x = 0.5
        init_speed_y = np.sqrt(initial_speed**2 - init_speed_x**2)
        self.speed = [init_speed_x, init_speed_y]
        self.initial_speed = initial_speed
        self.count = 0
        #for testing
        #self.speed = [0, 0]

        #Sound



    def update(self,  bar, sound_hit_bar):
        """x = self.x_cor + self.speed[0]
        y = self.y_cor + self.speed[1]
        pygame.draw.circle(screen, (255, 255, 255), (x,y), 5)"""
        

        #collision with boundary
        if self.rect.left < 0 and self.speed[0] <= 0:
            self.speed[0] *= -1
        elif self.rect.right > self.SCREEN_WIDTH and self.speed[0] >= 0:
            self.speed[0] *= -1
        if self.rect.top <= 0 and self.speed[1] <= 0:
            self.speed[1] *= -1
        elif self.rect.bottom >= self.SCREEN_HEIGHT:
            self.survive = False

        bounce = 0
        #collision with bar
        if self.rect.bottom >= bar.rect.top and self.rect.top <= bar.rect.bottom and self.rect.centerx >= bar.rect.left and self.rect.centerx <= bar.rect.right:
            """if self.speed[0]**2 + self.speed[1]**2 < 20**2:
                self.speed[1] += 0.01
                sign = 1 if self.speed[0] >= 0 else -1
                self.speed[0] += sign * 0.01

            bounce = 1
            #self.speed[0] += random.uniform(-2,2)
            self.speed[1] *= -1"""
            bounce = 1
            if sound_hit_bar is not None:
                sound_hit_bar.play()
            sign = 1 if self.rect.centerx - bar.rect.centerx > 0 else -1
            self.init_total_speed_squa = self.speed[0]**2 + self.speed[1]**2
            #self.dis_with_center = self.rect.centerx - bar.rect.centerx if abs(self.rect.centerx - bar.rect.centerx) > 3 else (abs(self.rect.centerx - bar.rect.centerx) / (self.rect.centerx - bar.rect.centerx)) * 3
            self.rebounce_angle = ((self.rect.centerx - bar.rect.centerx + (sign * 3)) / (bar.rect.right-bar.rect.left) + (sign * 3))* np.pi /1.5
            self.speed[0] = np.sqrt(self.init_total_speed_squa) * np.sin(self.rebounce_angle)
            self.speed[1] = np.sqrt(self.init_total_speed_squa) * np.cos(self.rebounce_angle) * -1
            
            #print(self.rebounce_angle, self.speed)






        #print(self.speed)
        self.x_cor_float += self.speed[0]
        self.y_cor_float += self.speed[1]
        self.rect.centerx = int(self.x_cor_float)
        self.rect.centery = int(self.y_cor_float)
        self.total_speed = np.sqrt(self.speed[0]**2 + self.speed[1]**2)
        if self.total_speed >= 15:
            self.survive = False
            self.too_fast = True

        if self.total_speed < 1 and self.total_speed > 0:
            self.win = True
        elif self.count >= 5:
            self.win = True
        #self.rect.move_ip(*self.speed)
        # if self.rect.centerx - bar.rect.left < 0:
        #     dist = self.rect.centerx - bar.rect.left
        # elif self.rect.centerx - bar.rect.right > 0:
        #     dist = bar.rect.right - self.rect.centerx
        # else:
        #     dist = int(((bar.rect.right-bar.rect.left) / 2 - abs(bar.rect.centerx - self.rect.centerx))  * 0.25 )
        # vert_dist = self.rect.bottom - bar.rect.top
        # if vert_dist < 0:
        #     dist
        #     dist *= (np.log(abs((1/vert_dist)))+7)
        # #print(dist)
        dist = self.SCREEN_WIDTH - abs(self.rect.centerx - bar.rect.centerx)
        return bounce * 0 + dist    #2000

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery), 5)