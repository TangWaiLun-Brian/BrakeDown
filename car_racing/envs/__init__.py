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


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, center, width, height):
        super(Rectangle, self).__init__()
        self.center = center
        self.width = width
        self.height = height
        self.color = (255,) * 3
        #print(self.center[0]-self.length//2, self.center[1]+self.width//2, self.center[0]+self.length//2, self.center[1]-self.width//2)

        self.rect = pygame.Rect(self.center[0]-self.width//2, self.center[1]+self.height//2, self.width, self.height)
        #print(self.color)


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ControlBar(Rectangle):
    def __init__(self, center, width, height):
        super(ControlBar, self).__init__(center, width, height)
        self.speed = 1
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right  = SCREEN_WIDTH





running = True


ball_coor = [225,400]
ball_speed = [0,1]

ball = Ball(*ball_coor, ball_speed)
bar = ControlBar((225, 650), 40, 2)

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()
    

    pressed_keys = pygame.key.get_pressed()
    bar.update(pressed_keys)
    bar.draw(screen)

    ball.update(ball_speed)
    ball.draw(screen)

    pygame.display.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()