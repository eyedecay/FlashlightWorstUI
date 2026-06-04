import pygame
import random


class Ball(pygame.sprite.Sprite):
    """
    Ball Class for creation of balls

    Attributes:
        number (int): digit displayed 
        radius (int): Radius of ball
        vector (list): speed
        screen_width (int): right boundary 
        screen_height (int): bottom boundary
        image (pygame.Surface): surface to hold the ball image
        rect (image.get_rect): stores x,y coordinates of the ball
    
    Methods:
        update(self): updates the ball position to bounce off walls using velocity vectors
    """
    def __init__(self, number, x, y, screen_width=1200, screen_height=700, radius=25):
        """
        Initializes a new ball instance

        Args:
            number (int): numerical value the ball holds
            x (int): initial x-coordinate
            y (int): initial y-coordinate
            screen_width (int): right boundary 
            screen_height (int): bottom boundary 
            radius (int): ball radius 
        """
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = radius
        self.number = number
        self.vector = [random.randint(-3, 3), random.randint(-3, 3)]

        for i in range(2):
            while abs(self.vector[i]) < 1:
                self.vector[i] = random.randint(-3, 3)

        # Creates the ball image
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (139, 0, 0), (radius, radius), radius)

        # Sets the position of the ball
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        # Sets up number on the ball/ Creates the font once on first Ball() constructor instead of every ball
        if not hasattr(Ball, '_font'):
            Ball._font = pygame.font.Font(None, 32)
        text = Ball._font.render(str(number), True, (255, 255, 255))
        self.image.blit(text, (radius - text.get_width() // 2, radius - text.get_height() // 2))

    def update(self):
        """
        Updates the ball position based on velocity vectors
        """
        # Moves the ball
        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]

        # Bounces the ball off the walls
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.vector[0] = -self.vector[0]
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.vector[1] = -self.vector[1]
