import pygame, random
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()

xdim, ydim = 900, 1600

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800

MAX_BALL_SPEED = 10
ACCELERTION = 0.3

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 

class Ball(pygame.sprite.Sprite):

    def __init__(self, x_cor, y_cor):
        super().__init__()

        """self.image = pygame.Surface([x_cor, y_cor])
        self.image.fill((0,0,0))"""
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (x_cor,y_cor), 5)
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.survive = True
        self.collide_with_bar = False
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
            if not self.collide_with_bar:
                speed[0] += random.uniform(-2,2)
                speed[1] *= -1
                self.collide_with_bar = True
        else:
            self.collide_with_bar = False
        
        #print(speed)
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


class Obstacle(Rectangle):
    def __init__(self):
        width = random.randint(9, 60)
        height = random.randint(9, 60)
        centerx = random.randint(-1, SCREEN_WIDTH - width)
        centery = random.randint(-1, 390 - height)
        super(Obstacle, self).__init__((centerx, centery), width, height)


def check_collison(obstacle, ball, ball_speed, previous, current, tolerance=15):
    flag = -1
    # if min(abs(obstacle.rect.left - ball.rect.centerx), abs(obstacle.rect.right - ball.rect.centerx)) <= min(abs(obstacle.rect.top - ball.rect.centery), abs(obstacle.rect.bottom - ball.rect.centery)):
    if obstacle.rect.left <= ball.rect.right and obstacle.rect.right >= ball.rect.left and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current:
            ball_speed[0] *= -1
            ball_speed[1] += random.uniform(-1, 1)
        flag = current
    elif obstacle.rect.right >= ball.rect.left and obstacle.rect.left <= ball.rect.right and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current + 1:
            ball_speed[0] *= -1
            ball_speed[1] += random.uniform(-1, 1)
        flag = current + 1
    # else
    if obstacle.rect.top <= ball.rect.bottom and obstacle.rect.bottom >= ball.rect.top and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current + 2:
            ball_speed[1] *= -1
            ball_speed[0] += random.uniform(-1, 1)
        flag = current + 2
    elif obstacle.rect.bottom >= ball.rect.top and obstacle.rect.top <= ball.rect.bottom and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current + 3:
            ball_speed[1] *= -1
            ball_speed[0] += random.uniform(-1, 1)
        flag = current + 3

    # adopt code method from video
    # flag = -1
    # if obstacle.rect.colliderect(ball.rect):
    #     if abs(obstacle.rect.top - ball.rect.bottom) < tolerance:
    #         ball_speed[1] *= -1
    #         flag = current
    #     elif abs(obstacle.rect.bottom - ball.rect.top) < tolerance:
    #         ball_speed[1] *= -1
    #         flag = current + 1
    #     if abs(obstacle.rect.left - ball.rect.right) < tolerance:
    #         ball_speed[0] *= -1
    #         flag = current + 2
    #     elif abs(obstacle.rect.right - ball.rect.left) < tolerance:
    #         ball_speed[0] *= -1
    #         flag = current + 3
    return flag

running = True


ball_coor = [225,400]
ball_speed = [3,10]

ball = Ball(*ball_coor)
bar = ControlBar((225, 650), 450, 10)
obstacles = [Obstacle() for i in range(10)]
previous_collison = -1
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()
    

    pressed_keys = pygame.key.get_pressed()
    bar.update(pressed_keys)
    bar.draw(screen)
    have_collision = False
    #print(previous_collison)
    tmp_pre = -1
    for i, obstacle in enumerate(obstacles):
        collide = check_collison(obstacle, ball, ball_speed, previous_collison, i * 4)
        if collide >= 0:
            tmp_pre = collide
            break
    previous_collison = tmp_pre
    ball.update(ball_speed, bar, ball)
    ball.draw(screen)

    if ball.survive == False:
        ball.kill()
        running = False
    for obstacle in obstacles:
        obstacle.draw(screen)
    pygame.display.update()

    clock.tick(120)
    pygame.display.flip()

pygame.quit()