from constants import *
from classes import * 
from enemy_spawner import Enemy_Spawner

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


enemies_group = pygame.sprite.Group()


# zombie = Zombie((500, 500), 0, 1)
# enemies_group = pygame.sprite.Group()
# all_sprites.add(zombie)

wall = Wall((400, 400), (50, 50))
all_sprites.add(wall)
bullets = pygame.sprite.Group()

spawner = Enemy_Spawner((500, 500))
spawners = pygame.sprite.Group()
all_sprites.add(spawner)
spawners.add(spawner)

store = Store((100, 100))
all_sprites.add(store)

running = True

bullet_damage = 1
is_auto = False
is_shotgun = False
gun_timer = 0
timer_limit = 20

money = 0


def use_shotgun():
    for i in range(5):
        new_bullet = Bullet((player.rect.left + 12 - i, player.rect.top + 12 - i), player.angle)
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)
while running:
    pressed_keys = pygame.key.get_pressed()
    screen.fill((0, 25, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g and is_auto == False:
                if is_shotgun == False:
                    new_bullet = Bullet((player.rect.left + 12, player.rect.top + 12), player.angle)
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)
                else:
                    use_shotgun()
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
    if pressed_keys[K_g] and is_auto == True and is_shotgun == False:
        gun_timer += 1
        if gun_timer > timer_limit:
            new_bullet = Bullet((player.rect.left + 12, player.rect.top + 12), player.angle)
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            timer = 0
    elif pressed_keys[K_g] and is_auto == True and is_shotgun == True:
        gun_timer += 1
        if gun_timer > timer_limit:
            use_shotgun()
            gun_timer = 0
    else:
        gun_timer = 0
    
    player.update(pressed_keys)
    if pygame.sprite.pygame.sprite.collide_rect(player, store):
        redeemed = 0
        redeemed = store.update(pressed_keys, money, is_auto, is_shotgun)
        if redeemed == 1:
            bullet_damage += 1
        elif redeemed == 2:
            is_auto = True
        elif redeemed == 3:
            is_shotgun = True


    for b in bullets:
        b.update()
    for enemy in enemies_group:
        for bullet in bullets:
            if pygame.sprite.collide_rect(enemy, bullet):
                enemy.health -= bullet_damage
                if enemy.health <= 0:
                    money += 10
                    enemy.kill()
                bullet.kill()
        enemy.update(player, all_sprites)
    
    for spawn in spawners:
        spawn.update(all_sprites, enemies_group)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()