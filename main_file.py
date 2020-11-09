from constants import *
from classes import * 

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    screen.fill((0, 25, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()