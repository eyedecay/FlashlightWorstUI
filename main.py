import pygame
from src.flashlight import Flashlight
from src.ball import Ball
from src.timer import Timer
from src.lock import Lock
import random
import math

WIDTH, HEIGHT = 1200, 700
BALL_MAX = 20

BEAM_HALF_ANGLE = 15
BEAM_MAX_DIST = 700
COLLECT_TIME = 5000


def ball_digit_checker(present_digits):
    """
    Checks if a number 0-9 is missing from the screen
    Args
        present_digits(list)
    Returns
        Boolean
    """
    for i in range(10):
        if i not in present_digits:
            return True
    return False


def is_in_beam(ball, origin_x, origin_y, beam_angle):
    """
    Checks if a ball is within the flashlight beam 

    Args:
        ball (object): ball object 
        origin_x (float): flashlight origin x
        origin_y (float): flashlight origin y
        beam_angle (float): direction of beam center (degrees))
    Returns
        bool (Whether ball is within beam)
    """
    dx = ball.rect.centerx - origin_x
    dy = ball.rect.centery - origin_y
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0 or dist > BEAM_MAX_DIST:
        return False
    ball_angle = math.degrees(math.atan2(dy, dx)) + 90
    difference = abs((ball_angle - beam_angle + 180) % 360 - 180)
    return difference < BEAM_HALF_ANGLE


pygame.init()


FONT = pygame.font.SysFont('Arial', 32)
VERIFICATION_FONT = pygame.font.Font(None, 120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# initialize Flashlight
flashlight = Flashlight(screen_width=WIDTH, screen_height=HEIGHT, darkness=100)

# Initialize game clock
clock = pygame.time.Clock()
create_ball_event = pygame.USEREVENT + 1

# Timer for the balls
pygame.time.set_timer(create_ball_event, 1000)

# Sprite containing all the balls
ball_group = []
ball_counter = 0
present_digits = []


verification_code = random.randint(100000, 999999)
lock = Lock(x=WIDTH - 150)
lock.reset([int(d) for d in str(verification_code)])
verification_on_screen = FONT.render(str(verification_code), True, (255, 255, 255))

timer = Timer()
ball_beam_times = {}
game_state = "playing"

# Game Loop
while running:
    # Sets up timer
    current_time = pygame.time.get_ticks()

    # Changes verification code, if timer runs out
    if timer.expired:
        verification_code = random.randint(100000, 999999)
        lock.reset([int(d) for d in str(verification_code)])
        verification_on_screen = FONT.render(str(verification_code), True, (255, 255, 255)) #font
        timer.reset()
        ball_beam_times = {}

    # Game Evenets
    for event in pygame.event.get():
        # Close window event
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and game_state == "playing":
            #shortcut
            lock.skip(5)
        # Create ball event
        elif (event.type == create_ball_event
        and (ball_counter < BALL_MAX or ball_digit_checker(present_digits))):
            ball_counter += 1 # Increases counter
            ball_number = random.randint(0,9) # Assigns random number to ball
            present_digits.append(ball_number) # Adds digit to list of digits on screen
            ball = Ball(ball_number, random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), screen_width=WIDTH, screen_height=HEIGHT)
            ball_group.append(ball)

    screen.fill((0, 0, 0))

    # Displays balls
    for ball in ball_group:
        ball.update()
        screen.blit(ball.image, ball.rect)

    # Records if the user is pressing the mouse or not
    mouse_click = pygame.mouse.get_pressed()
    flashlight_is_on = mouse_click[0]

    # Text display verificatoin code    
    text_surface = FONT.render("CODE:", True, (255, 255, 255))
    screen.blit(text_surface, (100, 500))
    screen.blit(verification_on_screen, (100, 600))

    # Text display for timer
    timer_text = FONT.render(str(timer.seconds_left), True, (255, 255, 255))
    screen.blit(timer_text, (300, 500))

    # Records position of users mouse
    mouse_pos = pygame.mouse.get_pos()
    
    dx = mouse_pos[0] - (WIDTH / 2)
    dy = mouse_pos[1] - HEIGHT

    # Calculates angle of flashlight based on user's mouse position
    light_angle = math.degrees(math.atan2(dy, dx)) + 90

    if game_state == "playing":
        if flashlight_is_on:
            for ball in ball_group:
                if is_in_beam(ball, WIDTH / 2, HEIGHT, light_angle):
                    if ball not in ball_beam_times:
                        ball_beam_times[ball] = current_time
                    elif current_time - ball_beam_times[ball] >= COLLECT_TIME:
                        if lock.try_collect(ball.number):
                            del ball_beam_times[ball]
                            #check if all digits done
                            if lock.is_full:
                                game_state = "verified"
                else:
                    ball_beam_times.pop(ball, None)
        else:
            ball_beam_times.clear()

        lock.draw(screen)

        # Updates flashlight
        flashlight.update(is_on=flashlight_is_on, angle=light_angle)

        # Draws flashlight
        flashlight.draw(screen, WIDTH / 2)

    # game ends
    elif game_state == "verified":
        verification_text = VERIFICATION_FONT.render("VERIFIED", True, (0, 255, 0))
        screen.blit(verification_text, (WIDTH // 2 - verification_text.get_width() // 2,
                            HEIGHT // 2 - verification_text.get_height() // 2))

    pygame.display.flip()
    
    clock.tick(60)
pygame.quit()
