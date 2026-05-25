import pygame 

class Flashlight(pygame.sprite.Sprite):
    """
    Flashlight Class

    Attributes:
        screen_width (int): Overall screen width
        screen_height (int): Overall Screen height
        radius (int): radius of light beem
        darkness: (colour)
    """
    def __init__(self, screen_height, screen_width, radius = 100, darkness = 200):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height 
        self.radius = radius 
        self.darkness = darkness

        self.COLOUR = (128, 128, 128)
        self.RIM = (220, 220, 220)

        self.mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        
    def update(self, x_position, is_on):
        
        self.mask.fill((0,0,0, self.darkness))

        if is_on:
            flashlight_pos = (x_position, self.screen_height)
            pygame.draw.circle(self.mask, (0,0,0,0), flashlight_pos, self.radius)
    
    def draw(self, surface, x_position):
        """
        Draws the flashlight onto the bottom of the screen

        Args:
            surface (pygame Surface): surface it's on
            x_position (int): x_position of the flashlight (horizontal)
        """
        surface.blit(self.mask, (0,0))

        handle_width = 40
        handle_height = 80
        handle_x, handle_y = x_position - (handle_width //2), self.screen_height - 50
        pygame.draw.rect(surface, self.COLOUR, (handle_x, handle_y, handle_width, handle_height))

        #wider flashlight point
        wide_part_points = [
            (x_position - 50, self.screen_height - 75), 
            (x_position + 50, self.screen_height - 75), 
            (x_position + 30, self.screen_height - 55), 
            (x_position - 30, self.screen_height - 55), 
        ]

        pygame.draw.polygon(surface, self.COLOUR, wide_part_points)
        pygame.draw.ellipse(surface, self.RIM, (x_position - 50, self.screen_height, 100, 20))




