import pygame
from flashlight import Flashlight
from ball import Ball
import random
from pygame.locals import USEREVENT

WIDTH, HEIGHT = 1200, 700
BALL_MAX = 20 # Max amount of balls on the screen at a time

def ballCondition(num_list):
    """
    Checks if a number 0-9 is missing from the screen
    Args
        num_list(list)
    Returns
        Boolean
    """
    for i in range(10):
        if i not in num_list:
            return True
    return False
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# initialize Flashlight
flashlight = Flashlight(screen_width = WIDTH, screen_height = HEIGHT, radius = 180, darkness = 200)

# Initialize game clock
clock = pygame.time.Clock()
create_ball_event = USEREVENT + 1

# Timer for the balls
pygame.time.set_timer(create_ball_event, 1000)

# Sprite containing all the balls
ball_group = []
ball_counter = 0
num_list = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    


            # Create ball event
        elif (event.type == create_ball_event 
        and (ball_counter < BALL_MAX or ballCondition(num_list))):
            ball_counter += 1 # Increases counter
            ball_number = random.randint(0,9) # Assigns random number to ball
            num_list.append(ball_number) # Adds number to list of number on the screen
            ball = Ball(ball_number, random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) # Creates a ball
            ball_group.append(ball)

    screen.fill((0, 0, 0))

    # Displays balls
    for ball in ball_group:
        ball.update()
        screen.blit(ball.image, ball.rect)
        
    mouse_click = pygame.mouse.get_pressed()
    flashlight_is_on = mouse_click[0]
    
    flashlight.update(WIDTH / 2, is_on=flashlight_is_on)
    flashlight.draw(screen, WIDTH/2, is_on = flashlight_is_on)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

