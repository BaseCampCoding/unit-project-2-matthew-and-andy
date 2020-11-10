import pygame
from constants import *
from classes import * 
import random 

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
    
    def spawn_enemy(self, all_sprite, enemy_group, wave):
        new_zombie = Zombie((self.rect.x, self.rect.y), 0, wave)
        all_sprite.add(new_zombie)
        enemy_group.add(new_zombie)

    def update(self, all_sprite, enemy_group):
        self.cur_time += 1
        if self.cur_time >= self.spawn_timer:
            self.spawn_enemy(all_sprite, enemy_group)
            self.cur_time = 0
