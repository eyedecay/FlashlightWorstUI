import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
RADIUS = 25

class Ball(pygame.sprite.Sprite):
    """
    Ball Class for creation of balls

    Attributes:
        radius (int): Radius of ball
        vector (list): speed
        image (pygame.Surface): surface to hold the ball image
        rect (image.get_rect): stores x,y coordinates of the ball
    Methods:
        update: moves the ball in random direction and bounces off walls
    """
    def __init__(self, number, x, y):
        """
        Initializes a new ball instance

        Args:
            number (int): numerical value the ball holds
            x (int): initial x-coordinate
            y (int): initial y-coordinate
        """
        super().__init__()

        # Initial Values of the ball
        self.radius = RADIUS
        self.vector = [random.randint(-3,3), random.randint(-3,3)] # Range of speed
    
        # Makes sure balls are moving:
        for i in range(2):
            while abs(self.vector[i]) < 1:
                self.vector[i] = random.randint(-3,3)

        # Creates the balls image
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (139, 0, 0), (self.radius, self.radius), self.radius)

        # Sets the position of the ball
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        # Sets up number on the ball
        numberFont = pygame.font.Font(None, 32)
        text = numberFont.render(str(number), 1, (255, 255, 255))
        self.image.blit(text, (self.radius - text.get_width() // 2, self.radius - text.get_height() // 2))

    def update(self):
        """
        Updates the ball position based on velocity vectors
        """
        # Moves the ball
        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]
        
        # Bounces the ball off the walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH - 0:
            self.vector[0] = -self.vector[0]
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT - 0:
            self.vector[1] = -self.vector[1]
            
