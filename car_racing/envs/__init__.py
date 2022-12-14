import pygame, random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

xdim, ydim = 900, 1600

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800

MAX_BALL_SPEED = 20
ACCELERTION = 0.3

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 

class Ball(pygame.sprite.Sprite):

    def __init__(self, x_cor, y_cor):
        super().__init__()

        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (x_cor,y_cor), 3)
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.survive = True

    def update(self, speed, bar, ball):
        """x = self.x_cor + speed[0]
        y = self.y_cor + speed[1]
        pygame.draw.circle(screen, (255, 255, 255), (x,y), 5)"""
        

        #collision with boundary
        if self.rect.left < 0:
            speed[0] *= -1
        elif self.rect.right > SCREEN_WIDTH:
            speed[0] *= -1
        if self.rect.top <= 0:
            speed[1] *= -1
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.survive = False
        
        #collision with bar
        if self.rect.bottom >= bar.rect.top and self.rect.top <= bar.rect.bottom and self.rect.centerx >= bar.rect.left and self.rect.centerx <= bar.rect.right:
            
            speed[0] += random.randint(-1,1) 
            speed[1] *= -1
        
        print(speed)
        self.rect.move_ip(*speed)
            

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
        self.speed = 10
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
init_x = random.randint(-3, 3)
ball_speed = [3,5]

ball = Ball(*ball_coor)
bar = ControlBar((225, 650), 100, 20)

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()
    

    pressed_keys = pygame.key.get_pressed()
    bar.update(pressed_keys)
    bar.draw(screen)

    ball.update(ball_speed, bar, ball)
    ball.draw(screen)

    if ball.survive == False:
        ball.kill()
        running = False

    pygame.display.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()