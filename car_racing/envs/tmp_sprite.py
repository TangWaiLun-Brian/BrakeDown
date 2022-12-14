import pygame
from pygame.locals import *
class Rectangle(pygame.sprite.Sprite):
    def __init__(self, center, length, width):
        super(Rectangle, self).__init__()
        self.center = center
        self.length = length
        self.width = width
        self.color = (255,) * 3
        #print(self.center[0]-self.length//2, self.center[1]+self.width//2, self.center[0]+self.length//2, self.center[1]-self.width//2)

        self.rect = pygame.Rect(self.center[0]-self.length//2, self.center[1]+self.width//2, self.length, self.width)
        #print(self.color)


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ControlBar(Rectangle):
    def __init__(self, center, length, width):
        super(ControlBar, self).__init__(center, length, width)
        self.speed = 1
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

if __name__ =='__main__':
    screen = pygame.display.set_mode([450, 800])
    bar = ControlBar((225, 650), 40, 2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed_keys = pygame.key.get_pressed()
        bar.update(pressed_keys)
        screen.fill((0,0,0))
        bar.draw(screen)
        pygame.display.flip()

    pygame.quit()