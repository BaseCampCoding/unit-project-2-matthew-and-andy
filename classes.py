import pygame
pygame.init()
from constants import *
from random import randint

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_BACKSPACE,
    K_RETURN,
    K_t,
    K_r,
    K_g,
    KEYDOWN,
    QUIT,
    K_1,
    K_2,
    K_3,
    K_4
)

speed = 2

class Aim(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Aim, self).__init__()
        self.surf = pygame.image.load(r"target.png").convert_alpha()
        self.rect = self.surf.get_rect()
    def update(self, player):
        mod_x = 0
        mod_y = 0
        if player.angle == 0:
            mod_y = -80
        elif player.angle == 1:
            mod_x = 80
            mod_y = -80
        elif player.angle == 2:
            mod_x = 80
        elif player.angle == 3:
            mod_x = 80
            mod_y = 80
        elif player.angle == 4:
            mod_y = 80
        elif player.angle == 5:
            mod_x = -80
            mod_y = 80
        elif player.angle == 6:
            mod_x = -80
        else:
            mod_x = -80
            mod_y = -80
        self.rect = self.surf.get_rect(center=(player.rect.x + mod_x + 32, player.rect.y + mod_y + 32))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(r"soldier.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(450, 30))
        self.hp = 15
        self.angle = 0
    def update(self, pressed_keys, walls):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-speed, 0)

        #collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        #indicator
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
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, cor: tuple, variant: int, wave: int):
        super(Zombie, self).__init__()
        speed = 1
        health = 5 + wave
        damage = 1
        sub_variant_chance = randint(1, 15)
        if variant == 0:#common 
            self.surf = pygame.image.load(r"zombie.png").convert_alpha()
            if sub_variant_chance == 15:
                name = 'Electric Boogoola'
                damage = 2
            else:
                name = 'Regular Joe' 

        elif variant == 1:#tank
            self.surf = pygame.image.load(r"zombie (3).png").convert_alpha()
            if sub_variant_chance == 15:
                name = 'Real Steel'
                health = health * 3
            else:
                name = 'The Rock' 
                health = health * 2
        elif variant == 2:#speedy
            self.surf = pygame.image.load(r"zombie (1).png").convert_alpha()
            if sub_variant_chance == 15:
                name = 'Insane Gonzales'
                speed = 3
                health = int(round(health / 2))
            else:
                name = 'Speedy Gonzales'
                health = int(round(health / 2))
                speed = 2
        elif variant == 3: #BOSS
            self.surf = pygame.image.load(r"BOSS.png").convert_alpha()
            name = 'The Imposter'
            health = health * 10 
            speed = 3
        self.speed = speed
        self.health = health
        self.name = name
        self.damage = damage
        self.rect = self.surf.get_rect(center=cor)
        self.pre_x = 0
        self.pre_y = 0
        self.move_x = 0
        self.move_y = 0
        self.timer = 0

    
    def update(self, player, all_sprites, zombies, aim):
        p_x = player.rect.right
        p_y = player.rect.top
        z_x = self.rect.right 
        z_y = self.rect.top 
        z_b = self.rect.bottom
        z_l = self.rect.left
        self.move_x = 0
        self.move_y = 0
        if p_x > z_x:
            self.move_x = 1
            if p_y > z_y:
                self.move_y = 1
            elif p_y < z_y:
                self.move_y = -1
            else:
                self.move_y = 0
        elif p_x < z_x:
            self.move_x = -1
            if p_y > z_y:
                self.move_y = 1
            elif p_y < z_y:
                self.move_y = -1
            else:
                self.move_y = 0
        else:
            if p_y > z_y:
                self.move_y = 1
            elif p_y < z_y:
                self.move_y = -1
            else:
                self.move_y = 0

        hit = False
        
        for i in all_sprites:
            if pygame.sprite.collide_rect(self, i) and not i == self and not i in zombies and not i == aim:
                hit = True
                temp = i
        if hit == True:
            if self.move_x != 0 and self.move_y != 0:
                obj_wid = int(temp.surf.get_size()[0] / 2)
                obj_hi = int(temp.surf.get_size()[1] / 2)
                is_dumb = 0
                if self.rect.left >= temp.rect.left + obj_wid:
                    self.move_x = -1
                    self.move_y = 0
                    is_dumb += 1
                if self.rect.left < temp.rect.left + obj_wid:
                    self.move_x = 1
                    self.move_y = 0
                    is_dumb += 1
                if self.rect.top >= temp.rect.top + obj_hi:
                    self.move_y = -1
                    self.move_x = 0
                    is_dumb += 1
                if self.rect.top < temp.rect.top + obj_hi:
                    self.move_y = 1
                    self.move_x = 0
                    is_dumb += 1
                if is_dumb > 1:
                    self.move_y *= -1
                    self.move_x *= -1
                # else:
                #     self.move_y = random.randint(-10, 10)
                #     self.move_x = random.randint(-10, 10)
            elif self.move_x != 0 and self.move_y == 0:
                # if self_y < p_y:
                #     self.move_y = 1
                # else:
                #     self.move_y = -1
                self.move_y = self.move_x
                self.move_x = 0
            elif self.move_x == 0 and self.move_y != 0:
                # if self_x < p_x:
                #     self.move_x = 1
                # else:
                #     self.move_x = -1
                self.move_x = self.move_y
                self.move_y = 0
        self.rect.move_ip((self.move_x * self.speed, self.move_y * self.speed))
        #animation
        # pygame.transform.flip(, True, False)
        # if move_x != self.pre_x and move_x != 0:
        #     self.surf = pygame.transform.flip(self.surf, True, False)
        # self.pre_x = move_x
        # self.pre_y = move_y

class Wall(pygame.sprite.Sprite):
    def __init__(self, cor: tuple, size: tuple):
        super(Wall, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(colors["Red"])
        self.rect = self.surf.get_rect(center=cor)


class Store(pygame.sprite.Sprite):
    def __init__(self, cor: tuple):
        super(Store, self).__init__()
        self.surf = pygame.image.load(r"gun-shop.png").convert_alpha()
        self.rect = self.surf.get_rect(center=cor)

    def update(self, pressed_keys, Money, is_auto, is_shotgun):
        if pressed_keys[K_1] and Money >= 300:
            return 1
        elif pressed_keys[K_2] and Money >= 100 and is_auto == False:
            return 2 
        elif pressed_keys[K_3] and Money >= 150 and is_shotgun == False:
            return 3
        elif pressed_keys[K_4] and Money >= 200:
            return 4
        else:
            return 0 