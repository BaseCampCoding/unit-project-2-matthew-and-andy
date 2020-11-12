from constants import *
from classes import * 
from enemy_spawner import Enemy_Spawner
from random import randint
from database import score, insert_score, PrintOut, close
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#background
background = pygame.image.load(r"darkfloor.jpg")


# title and icon
pygame.display.set_caption("Z Shooters")
icon = pygame.image.load(r"zombie (1).png")
pygame.display.set_icon(icon)

enemies_group = pygame.sprite.Group()


# zombie = Zombie((500, 500), 0, 1)
# enemies_group = pygame.sprite.Group()
# all_sprites.add(zombie)

walls = pygame.sprite.Group()
wall_list = [[(450, 300), (100, 100)]]
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

store = Store((750, 100))
all_sprites.add(store)
store_timer = 0

bullet_damage = 1
is_auto = False
is_shotgun = False
gun_timer = 0
timer_limit = 5
aimer = Aim(player)
all_sprites.add(aimer)

money = 0
FONT = pygame.font.SysFont('Consolas', 15)
i_timer = 0

def use_shotgun():
    for m in range(5):
        i = randint(20, 40)
        j = randint(20, 40)
        new_bullet = Bullet((player.rect.x + i, player.rect.y + j), player.angle)
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)

def takeSecond(elem):
    return (elem[1] * 5) + elem[2]

#game running initialization
wave = 1
kills = 0
sp_timer = 0

running = True

while running:
    aimer.update(player)
    pressed_keys = pygame.key.get_pressed()
    #background image 
    screen.blit(background,(0,0))
    #event management
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g and is_auto == False:
                if is_shotgun == False:
                    new_bullet = Bullet((player.rect.left + 32, player.rect.top + 32), player.angle)
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
            new_bullet = Bullet((player.rect.left + 32, player.rect.top + 32), player.angle)
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            gun_timer = 0
    elif pressed_keys[K_g] and is_auto == True and is_shotgun == True:
        gun_timer += 1
        if gun_timer > timer_limit + 5:
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
        store_timer += 1
        if store_timer > 300:
            player.rect.top += 200
        screen.blit(FONT.render("1. Bullet Damage ($300)", True, (255, 255, 0)), (300, 30))
        screen.blit(FONT.render("2. Fully-Automatic ($100)", True, (255, 255, 0)), (300, 50))
        screen.blit(FONT.render("3. Shotgun ($150)", True, (255, 255, 0)), (300, 70))
        screen.blit(FONT.render("4. +1 HP ($200)", True, (255, 255, 0)), (300, 90))
        redeemed = 0
        redeemed = store.update(pressed_keys, money, is_auto, is_shotgun)
        if redeemed == 1:
            money -= 300
            bullet_damage += 1
        elif redeemed == 2:
            money -= 100
            is_auto = True
        elif redeemed == 3:
            money -= 150
            is_shotgun = True
        elif redeemed == 4:
            money -= 200
            player.hp += 1
    else:
        store_timer = 0


    for b in bullets:
        b.update()
        for i in walls:
            if pygame.sprite.collide_rect(b, i):
                b.kill()
    for enemy in enemies_group:
        enemy.update(player, all_sprites, enemies_group, aimer)
        screen.blit(FONT.render(str(enemy.name) + ": " + str(enemy.health), True, (255, 255, 0)), (enemy.rect.x, enemy.rect.top-20))
        for bullet in bullets:
            if pygame.sprite.collide_rect(enemy, bullet):
                enemy.health -= bullet_damage
                if enemy.health <= 0:
                    money += enemy.price
                    kills += 1
                    enemy.kill()
                bullet.kill()
        if pygame.sprite.collide_rect(enemy, player) and i_timer == 0:
            player.hp -= enemy.damage
            i_timer = 100
    if player.hp <= 0:
        running = False
    if i_timer > 0:
        i_timer -= 1
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

in_leader_board = False
text = ''
running = True
while running:
    screen.fill((0, 25, 0))
    #background image 
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and in_leader_board == False:
                cur_score = score(text, wave, kills)
                insert_score(cur_score)
                in_leader_board = True
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
    if in_leader_board == False:
        screen.blit(FONT.render("Please enter your name", True, (255, 255, 0)), (50, 300))
        screen.blit(FONT.render(text, True, (255, 255, 0)), (50, 350))
    else:
        score_board = PrintOut()
        score_board.sort(key=takeSecond, reverse=True)
        z = 30
        for row in score_board:
            screen.blit(FONT.render(f"Name: {row[0]}, Waves: {row[1]}, Kills: {row[2]}", True, (255, 255, 0)), (50, z))
            z += 30
            if z > 300:
                break
    pygame.display.flip()
    clock.tick(FRAMERATE)
close()
pygame.quit()