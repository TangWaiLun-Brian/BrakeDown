import pygame
from pygame.locals import *


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, center, width, height, color=(255,)*3):
        super(Rectangle, self).__init__()
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        #print(self.center[0]-self.length//2, self.center[1]+self.width//2, self.center[0]+self.length//2, self.center[1]-self.width//2)

        self.rect = pygame.Rect(self.center[0]-self.width//2, self.center[1]-self.height//2, self.width, self.height)
        #print(self.color)


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class ControlBar(Rectangle):
    def __init__(self, center, width, height, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(ControlBar, self).__init__(center, width, height)
        self.speed = 5
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

    def update(self, action):
        if action == 0:
            self.rect.move_ip(-self.speed, 0)
        if action == 2:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.SCREEN_WIDTH:
            self.rect.right  = self.SCREEN_WIDTH

class Obstacle(Rectangle):
    def __init__(self, SCREEN_WIDTH, rng):
        width = rng.integers(9, 60)
        height = rng.integers(9, 60)
        centerx = rng.integers(width // 2, SCREEN_WIDTH - width //2)
        centery = rng.integers(height//2, 390 - height // 2)
        super(Obstacle, self).__init__((centerx, centery), width, height)

class Brake(Rectangle):
    def __init__(self, SCREEN_WIDTH, rng):
        width = 15
        height = 15
        centerx = rng.integers(width // 2, SCREEN_WIDTH - width //2)
        centery = rng.integers(height//2, 390 - height // 2)
        super(Brake, self).__init__((centerx, centery), width, height, color=(140,200,70))
    
    def update(self, ball, rng):
        if self.rect.colliderect(ball):    
            ball.speed[0] *= 0.8 
            ball.speed[0] += rng.uniform(-0.2, 0.2)
            ball.speed[1] *= 0.8
            print(ball.speed)
            self.kill()
            return 1
        return 0