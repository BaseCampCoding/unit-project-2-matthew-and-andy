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
    K_g,
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
    def __init__(self, cor: tuple, angle: int):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill(colors["Red"])
        self.rect = self.surf.get_rect(center=cor)
        self.angle = angle
        #0, up
        #1, up and right
        #2, right
        #3, down and right
        #4, down
        #5, down and left
        #6, left
        #7, up and left
    def update(self):
        if self.angle == 0:
            dir = (0, -5)
        elif self.angle == 1:
            dir = (5, -5)
        elif self.angle == 2:
            dir = (5, 0)
        elif self.angle == 3:
            dir = (5, 5)
        elif self.angle == 4:
            dir = (0, 5)
        elif self.angle == 5:
            dir = (-5, 5)
        elif self.angle == 6:
            dir = (-5, 0)
        elif self.angle == 7:
            dir = (-5, -5)
        else:
            dir = (0, 2)
        self.rect.move_ip(dir)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, cor: tuple, variant: int, wave: int):
        super(Zombie, self).__init__()
        speed = 1
        health = (5 + wave) * wave
        if variant == 0:
            self.surf = pygame.Surface((25, 25))
            self.surf.fill(colors["Green"])
        else:
            self.surf = pygame.Surface((20, 20))
            self.surf.fill(colors["Green"])
            health = int(round(health / 2))
            speed = 3
        self.speed = speed
        self.health = health
        self.rect = self.surf.get_rect(center=cor)
    
    def update(self, player, all_sprites):
        p_x = player.rect.right
        p_y = player.rect.top
        z_x = self.rect.right 
        z_y = self.rect.top 
        move_x = 0
        move_y = 0
        if p_x > z_x:
            move_x = 1
            if p_y > z_y:
                move_y = 1
            elif p_y < z_y:
                move_y = -1
            else:
                move_y = 0
        elif p_x < z_x:
            move_x = -1
            if p_y > z_y:
                move_y = 1
            elif p_y < z_y:
                move_y = -1
            else:
                move_y = 0
        else:
            if p_y > z_y:
                move_y = 1
            elif p_y < z_y:
                move_y = -1
            else:
                move_y = 0

        hit = False
        for i in all_sprites:
            if pygame.sprite.collide_rect(self, i) and not i == self:
                hit = True
                temp = i
        if hit == True:
            if temp.rect.right > z_x and temp.rect.top < z_y:
                print("state A")
                move_y = 1
                move_x = 0
            elif temp.rect.left < z_x and temp.rect.bottom < z_y:
                print("state B")
                move_y = -1
                move_x = 0
            elif temp.rect.top > z_y:
                print("state C")
                move_x = 1
                move_y = 0
            elif temp.rect.bottom < z_y:
                print("state D")
                move_x = -1
                move_y = 0
        self.rect.move_ip((move_x * self.speed, move_y * self.speed))

class Wall(pygame.sprite.Sprite):
    def __init__(self, cor: tuple, size: tuple):
        super(Wall, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(colors["Red"])
        self.rect = self.surf.get_rect(center=cor)