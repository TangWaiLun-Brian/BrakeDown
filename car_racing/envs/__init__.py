import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

xdim, ydim = 900, 1600

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 

class Ball(pygame.sprite.Sprite):

    def __init__(self, x_cor, y_cor, speed):
        super().__init__()

        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (x_cor,y_cor), 5)
        self.x_cor = x_cor
        self.y_cor = y_cor

    def update(self, speed):
        """x = self.x_cor + speed[0]
        y = self.y_cor + speed[1]
        pygame.draw.circle(screen, (255, 255, 255), (x,y), 5)"""
        self.rect.move_ip(*speed)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery), 5)


running = True


ball_coor = [225,400]
ball_speed = [0,1]

ball = Ball(*ball_coor, ball_speed)


while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()
    ball.update(ball_speed)
    ball.draw(screen)

    pygame.display.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()