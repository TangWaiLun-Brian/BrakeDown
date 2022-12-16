import pygame, random
from pygame.locals import *
import random

class Ball(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):
        super().__init__()

        self.x_cor = 225
        self.y_cor = 420
        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (self.x_cor, self.y_cor), 5)
        self.survive = True
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.speed = [1.5, 8]

    def update(self,  bar):
        """x = self.x_cor + self.speed[0]
        y = self.y_cor + self.speed[1]
        pygame.draw.circle(screen, (255, 255, 255), (x,y), 5)"""
        

        #collision with boundary
        if self.rect.left < 0:
            self.speed[0] *= -1
        elif self.rect.right > self.SCREEN_WIDTH:
            self.speed[0] *= -1
        if self.rect.top <= 0:
            self.speed[1] *= -1
        elif self.rect.bottom >= self.SCREEN_HEIGHT:
            self.survive = False
        
        #collision with bar
        if self.rect.bottom >= bar.rect.top and self.rect.top <= bar.rect.bottom and self.rect.centerx >= bar.rect.left and self.rect.centerx <= bar.rect.right:
            
            #self.speed[0] += random.uniform(-2,2)
            self.speed[1] *= -1




        #print(self.speed)
        self.rect.move_ip(*self.speed)
            

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery), 5)