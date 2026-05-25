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
    
    mouse_click = pygame.mouse.get_pressed()
    flashlight_is_on = mouse_click[0]
    
    flashlight.update(WIDTH / 2, is_on=flashlight_is_on)
    flashlight.draw(screen, WIDTH/2, is_on = flashlight_is_on)
    pygame.display.flip()

pygame.quit()

