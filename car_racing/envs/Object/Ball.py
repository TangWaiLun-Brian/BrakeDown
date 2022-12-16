import pygame, random
from pygame.locals import *
import random

class Ball(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):
        super().__init__()

        self.x_cor = 225
        self.y_cor = 400
        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (self.x_cor, self.y_cor), 5)
        self.survive = True
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

    def update(self, speed, bar, ball):
        """x = self.x_cor + speed[0]
        y = self.y_cor + speed[1]
        pygame.draw.circle(screen, (255, 255, 255), (x,y), 5)"""
        

        #collision with boundary
        if self.rect.left < 0:
            speed[0] *= -1
        elif self.rect.right > self.SCREEN_WIDTH:
            speed[0] *= -1
        if self.rect.top <= 0:
            speed[1] *= -1
        elif self.rect.bottom >= self.SCREEN_HEIGHT:
            self.survive = False
        
        #collision with bar
        if self.rect.bottom >= bar.rect.top and self.rect.top <= bar.rect.bottom and self.rect.centerx >= bar.rect.left and self.rect.centerx <= bar.rect.right:
            
            speed[0] += random.uniform(-2,2)
            speed[1] *= -1
        
        #print(speed)
        self.rect.move_ip(*speed)
            

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery), 5)