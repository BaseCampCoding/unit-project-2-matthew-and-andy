import pygame

pygame.init()

clock = pygame.time.Clock()


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_t,
    K_f,
    K_g,
    K_h,
    KEYDOWN,
    QUIT,
)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MAX_SPEED = 4
speed = 2
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
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


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)




FRAMERATE = 120

running = True


while running:
    screen.fill((0, 25, 0))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            print(running)
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