from constants import *
from classes import * 
from enemy_spawner import Enemy_Spawner
from random import randint
from database import score, insert_score, PrintOut
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# title and icon
pygame.display.set_caption("Z Shooters")
icon = pygame.image.load(r"zombie (1).png")
pygame.display.set_icon(icon)

enemies_group = pygame.sprite.Group()


# zombie = Zombie((500, 500), 0, 1)
# enemies_group = pygame.sprite.Group()
# all_sprites.add(zombie)

walls = pygame.sprite.Group()
wall_list = [[(450, 300), (50, 300)], [(450, 150), (300, 50)]]
for cor in wall_list:
    wall = Wall(cor[0], cor[1])
    all_sprites.add(wall)
    walls.add(wall)

bullets = pygame.sprite.Group()

spawners = pygame.sprite.Group()
spawn_point_list = [(800, 500), (50, 500)]
for cor in spawn_point_list:
    new = Enemy_Spawner(cor)
    spawners.add(new)
    all_sprites.add(new)

store = Store((100, 100))
all_sprites.add(store)

running = True

bullet_damage = 1
is_auto = False
is_shotgun = False
gun_timer = 0
timer_limit = 20
aimer = Aim(player)
all_sprites.add(aimer)

money = 1000
FONT = pygame.font.SysFont('Consolas', 15)
i_timer = 0

def use_shotgun():
    for m in range(5):
        i = randint(-15, 15)
        j = randint(-15, 15)
        new_bullet = Bullet((player.rect.x + i, player.rect.y + j), player.angle)
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)
wave = 1
kills = 0
sp_timer = 0
while running:
    aimer.update(player)
    pressed_keys = pygame.key.get_pressed()
    screen.fill((0, 25, 0))

    #event management
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
            gun_timer = 0
    elif pressed_keys[K_g] and is_auto == True and is_shotgun == True:
        gun_timer += 1
        if gun_timer > timer_limit:
            use_shotgun()
            gun_timer = 0
    else:
        gun_timer = 0
    
    player.update(pressed_keys, walls)

    #used for drawing the player's stats on screen
    screen.blit(FONT.render("HP: " + str(player.hp), True, (255, 255, 0)), (player.rect.x, player.rect.top-20))
    screen.blit(FONT.render("$" + str(money), True, (255, 255, 0)), (30, 30))
    screen.blit(FONT.render("Wave " + str(wave), True, (255, 255, 0)), (30, 60))
    screen.blit(FONT.render(str(kills) + " Kills", True, (255, 255, 0)), (30, 90))

    #used for making sure the player is in the store before they can buy stuff
    if pygame.sprite.pygame.sprite.collide_rect(player, store):
        redeemed = 0
        redeemed = store.update(pressed_keys, money, is_auto, is_shotgun)
        if redeemed == 1:
            money -= 50
            bullet_damage += 1
        elif redeemed == 2:
            money -= 100
            is_auto = True
        elif redeemed == 3:
            money -= 150
            is_shotgun = True


    for b in bullets:
        b.update()
        for i in walls:
            if pygame.sprite.collide_rect(b, i):
                b.kill()
    for enemy in enemies_group:
        enemy.update(player, all_sprites)
        screen.blit(FONT.render("HP: " + str(enemy.health), True, (255, 255, 0)), (enemy.rect.x, enemy.rect.top-20))
        for bullet in bullets:
            if pygame.sprite.collide_rect(enemy, bullet):
                enemy.health -= bullet_damage
                if enemy.health <= 0:
                    money += 10
                    kills += 1
                    enemy.kill()
                bullet.kill()
        if pygame.sprite.collide_rect(enemy, player) and i_timer == 0:
            player.hp -= 1
            print("OH NO")
            i_timer = 100
    if player.hp <= 0:
        running = False
    if i_timer > 0:
        i_timer -= 1
            
        enemy.update(player, all_sprites)
    sp_timer += 1
    if sp_timer > WAVE_LENGTH:
        wave += 1
        sp_timer = 0 

    for spawn in spawners:
        spawn.update(all_sprites, enemies_group, wave)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()

cur_name = input("What is your name, so that we can put you on the leader board? ")
cur_score = score(cur_name, wave, kills)
insert_score(cur_score)
PrintOut()


# TEMPORARY
# print(f"Kills: {kills}, Wave: {wave}")