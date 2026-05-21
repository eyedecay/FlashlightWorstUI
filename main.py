import pygame
from flashlight import Flashlight


WIDTH, HEIGHT = 1200, 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# initialize Flashlight
flashlight = Flashlight(screen_width = WIDTH, screen_height = HEIGHT, radius = 180, darkness = 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    flashlight.update(WIDTH / 2, is_on=True)
    flashlight.draw(screen, WIDTH/2)
    pygame.display.flip()

pygame.quit()

