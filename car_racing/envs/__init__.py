import pygame
from pygame.locals import *

pygame.init()

xdim, ydim = 900, 1600
screen = pygame.display.set_mode([900, 1600]) 


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()

    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()