import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, number, window):
        super().__init__()
        starting_pos = [100, 100]
        radius = 20
        ball_speed = [3, -3]

        pygame.draw.circle(window, (255, 0, 0), starting_pos, radius)


        # For Later
        """
        #Initializes Image
        self.image = pygame.imagae.load(f"ball{number}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.center = starting_pos
        """


