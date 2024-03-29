import pygame
from pygame.locals import *
import numpy as np

class Rectangle(pygame.sprite.Sprite):
    """
    The base class of Rectangle
    Inherited from pygame Sprite
    """
    def __init__(self, center, width, height, color=(255,)*3):
        super(Rectangle, self).__init__()
        self.center = center
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.center[0]-self.width//2, self.center[1]-self.height//2, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class ControlBar(Rectangle):
    """
    Control Bar Object
    Inherited from Rectangle
    """
    def __init__(self, center, width, height, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(ControlBar, self).__init__(center, width, height)
        self.speed = 5
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

    def update(self, action):
        # update bar position
        if action == 0:
            self.rect.move_ip(-self.speed, 0)
        if action == 2:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.SCREEN_WIDTH:
            self.rect.right  = self.SCREEN_WIDTH

class Obstacle(Rectangle):
    """
    Obstacle Object
    Inherited from Rectangle
    """
    def __init__(self, SCREEN_WIDTH, rng):
        # assign a random width and height for the obstacle
        width = rng.integers(9, 60)
        height = rng.integers(9, 60)

        # assigan a random position for the obstacle
        centerx = rng.integers(width // 2, SCREEN_WIDTH - width //2)
        centery = rng.integers(height//2, 390 - height // 2)

        super(Obstacle, self).__init__((centerx, centery), width, height, color=(240, 231, 129))

class Brake(Rectangle):
    """
    Brake Object
    Inherited from Rectangle
    """
    def __init__(self, SCREEN_WIDTH, rng):
        width = 15
        height = 15

        centerx = rng.integers(width // 2, SCREEN_WIDTH - width //2)
        centery = rng.integers(height//2, 390 - height // 2)

        super(Brake, self).__init__((centerx, centery), width, height, color=(27, 110, 33))

    def update(self, ball, rng, sound_hit_brake):
        # Disappear when collide with ball
        # Regenerate one at a new position
        if self.rect.colliderect(ball):
            if sound_hit_brake is not None:
                sound_hit_brake.play()

            norm = np.sqrt(ball.speed[0]**2 + ball.speed[1]**2)
            ball.speed[0] = ball.speed[0] / norm * ball.initial_speed
            ball.speed[1] = ball.speed[1] / norm * ball.initial_speed

            self.kill()
            return 1
        return 0


class Accelerator(Rectangle):
    """
    Nitrous Accelerator
    Inherited from Rectangle
    """
    def __init__(self, SCREEN_WIDTH, rng):
        width = 15
        height = 15
        self.SCREEN_WIDTH = SCREEN_WIDTH
        # initialize random position
        self.x_cor_float = centerx = rng.integers(width, SCREEN_WIDTH - width)
        self.y_cor_float = centery = rng.integers(30, 900 // 2)

        super(Accelerator, self).__init__((centerx, centery), width, height, color=(255, 0, 0))

        # initialize random direction for speed
        init_speed_x = rng.uniform(-1, 1)
        init_speed_y = np.sqrt(9 - init_speed_x ** 2)
        self.speed = [init_speed_x, init_speed_y]

    def update(self, ball, rng, sound_hit_acc):
        # update coordinate
        self.x_cor_float += self.speed[0]
        self.y_cor_float += self.speed[1]
        self.rect.centerx = int(self.x_cor_float)
        self.rect.centery = int(self.y_cor_float)

        # check bouncing with wall
        if self.rect.left < 0 and self.speed[0] <= 0:
            self.speed[0] *= -1
        elif self.rect.right > self.SCREEN_WIDTH and self.speed[0] >= 0:
            self.speed[0] *= -1
        if self.rect.top <= 0 and self.speed[1] <= 0:
            self.speed[1] *= -1
        elif self.rect.bottom >= 600 and self.speed[1] >= 0:
            self.speed[1] *= -1

        # if collide with ball, accelerates the ball and disappear
        if self.rect.colliderect(ball):
            ball.speed[0] *= 1.5
            ball.speed[1] *= 1.5
            if sound_hit_acc is not None:
                sound_hit_acc.play()
            self.kill()
            return 1
        return 0