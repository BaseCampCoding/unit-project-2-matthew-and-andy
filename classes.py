import pygame
pygame.init()
from constants import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_t,
    K_r,
    KEYDOWN,
    QUIT,
)

speed = 2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(colors["White"])
        self.rect = self.surf.get_rect()
        self.angle = 0
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
            # if pygame.sprite.spritecollideany(player, walls):
            #     self.rect.move_ip(0, speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
            # if pygame.sprite.spritecollideany(player, walls):
            #     self.rect.move_ip(0, -speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
            # if pygame.sprite.spritecollideany(player, walls):
            #     self.rect.move_ip(speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)
            # if pygame.sprite.spritecollideany(player, walls):
            #     self.rect.move_ip(-speed, 0)
        #collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle):
        self.surf = pygame.Surface((5, 5))
        self.surf.fill(colors["Red"])