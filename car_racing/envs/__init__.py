import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

xdim, ydim = 900, 1600
screen = pygame.display.set_mode([450, 800]) 

class Ball(pygame.sprite.Sprite):

    def __init__(self, x_cor, y_cor):
        super().__init__()

        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (225,400), 3)

        

running = True
ball_coor = [100,300]
ball_speed = [0,0]
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()


    
    ball = Ball(*ball_coor)

    pygame.display.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()