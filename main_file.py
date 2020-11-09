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

FRAMERATE = 120

running = True

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            print(running)
        if event.type == pygame.QUIT:
                running = False
    
    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()