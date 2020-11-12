import pygame
from constants import *
from classes import * 
import random 

#enemy spawner
class Enemy_Spawner(pygame.sprite.Sprite):
    def __init__(self, cor: tuple):
        super(Enemy_Spawner, self).__init__()
        self.special_name = "Spawner"
        self.surf = pygame.image.load(r"z_spawner.png").convert_alpha()
        self.rect = self.surf.get_rect(center=cor)
        self.spawn_timer = random.randrange(440, 1040)
        self.cur_time = 0
    
    def spawn_enemy(self, all_sprite, enemy_group, wave):
        variant = 0 
        if wave <= 3:
            variant = 0 
        elif wave < 8:
            variant = random.randint(0,1) 
        elif wave < 16:
            variant = random.randint(0,2)
        else:
            variant = random.randint(1, 3)
        new_zombie = Zombie((self.rect.x, self.rect.y - 60), variant, wave)
        all_sprite.add(new_zombie)
        enemy_group.add(new_zombie)

    def update(self, all_sprite, enemy_group, wave):
        self.cur_time += 1
        if self.cur_time >= self.spawn_timer:
            self.spawn_enemy(all_sprite, enemy_group, wave)
            self.cur_time = 0
