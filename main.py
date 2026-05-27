import pygame
from flashlight import Flashlight
from ball import Ball
import random
from pygame.locals import USEREVENT
import time
import math

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


FONT = pygame.font.SysFont('Arial', 32)
INTERVAL = 60000 #(miliseconds)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# initialize Flashlight
flashlight = Flashlight(screen_width = WIDTH, screen_height = HEIGHT, radius = 180, darkness = 100)

# Initialize game clock
clock = pygame.time.Clock()
create_ball_event = USEREVENT + 1

# Timer for the balls
pygame.time.set_timer(create_ball_event, 1000)

# Sprite containing all the balls
ball_group = []
ball_counter = 0
num_list = []


#generate random 6-digit code
verification_code = random.randint(100000, 999999)
verification_on_screen = FONT.render(f"{str(verification_code)}", True, (255, 255, 255))
last_time_change = pygame.time.get_ticks()


while running:
    current_time = pygame.time.get_ticks()

    #reset code every 60 seconds
    if current_time - last_time_change >= INTERVAL:
        verification_code = random.randint(100000, 999999)

        verification_on_screen = FONT.render(f"{str(verification_code)}", True, (255, 255, 255))
        last_time_change = pygame.time.get_ticks() #set to current_time
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Create ball event
        elif (event.type == create_ball_event and (ball_counter < BALL_MAX or ballCondition(num_list))):
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
    
    text_surface = FONT.render("CODE:", True, (255, 255, 255))
    screen.blit(text_surface, (100, 500))


    screen.blit(verification_on_screen, (100, 600))


    #timer 
    elapsed_time = (current_time - last_time_change) // 1000
    time_until_change = 60 - elapsed_time
    timer_text = FONT.render(f"{str(time_until_change)}", True, (255, 255, 255))
    screen.blit(timer_text, (300, 500))
    

    mouse_click = pygame.mouse.get_pressed()
    flashlight_is_on = mouse_click[0]
    
    mousePos = pygame.mouse.get_pos()
    
    dx = mousePos[0] - (WIDTH / 2)
    dy = mousePos[1] - HEIGHT
    
    lightAngle = math.degrees(math.atan2(dy, dx)) + 90
 

    flashlight.update(WIDTH / 2, is_on=flashlight_is_on)
    flashlight.draw(screen, WIDTH/2, is_on = flashlight_is_on, angle = lightAngle)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

