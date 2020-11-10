from constants import *
from classes import * 
from enemy_spawner import Enemy_Spawner

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


enemies_group = pygame.sprite.Group()

zombie = Zombie((500, 500), 0, 1)
all_sprites.add(zombie)

wall = Wall((400, 400), (50, 50))
all_sprites.add(wall)
bullets = pygame.sprite.Group()

spawner = Enemy_Spawner((300, 300))

running = True

while running:
    # zombie.update(player, all_sprites)
    screen.fill((0, 25, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                new_bullet = Bullet((player.rect.left + 12, player.rect.top + 12), player.angle)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            elif event.key == pygame.K_r:
                player.angle -= 1
            elif event.key == pygame.K_t:
                player.angle += 1
            
            if player.angle >= 8:
                player.angle = 0
            elif player.angle <= -1:
                player.angle = 7
        if event.type == pygame.QUIT:
            running = False
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    for entity in all_sprites:
        try:
            entity.update()
        except:
            pass
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()