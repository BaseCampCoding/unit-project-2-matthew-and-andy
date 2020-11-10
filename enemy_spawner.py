import pygame
from constants import *
from classes import * 
import random 

#enemy spawning
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.image = pygame.image.load(r"zombie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.vel_x = 0 
        self.vel_y = random.randrange(3,8)

    def update(self):
        self.rect.x +=  self.vel_x
        self.rect.y += self.vel_y

#enemy spawner
class Enemy_Spawner(pygame.sprite.Sprite):
    def __init__(self, cor: tuple):
        super(Enemy_Spawner, self).__init__()
        self.image = pygame.image.load(r"zombie.png").convert_alpha()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=cor)
        self.spawn_timer = random.randrange(220, 420)
        self.cur_time = 0
    
    def spawn_enemy(self, all_sprite, enemy_group):
        new_zombie = Zombie((self.rect.x, self.rect.y), 0, 1)
        all_sprite.add(new_zombie)
        enemy_group.add(new_zombie)

    def update(self, all_sprite, enemy_group):
        self.cur_time += 1
        if self.cur_time >= self.spawn_timer:
            self.spawn_enemy(all_sprite, enemy_group)
            self.cur_time = 0
