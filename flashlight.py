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
        self.BEAM_COLOUR = (255, 255, 0)

        self.mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        self.beam_width_offset_left = 50
        self.beam_width_offset_right = 50
        self.light_width = self.beam_width_offset_left + self.beam_width_offset_right

        # Create image for flashlight to easily rotate
        self.flashlight_base = pygame.Surface((100, 3 * screen_height), pygame.SRCALPHA)

        # Initial Positions
        self.rotated_flashlight = self.flashlight_base

    def update(self, x_position, is_on, angle):
        self.mask.fill((0,0,0, self.darkness))

        # Beam Surface
        beam_length = 2 * self.screen_height
        self.beam_surface = pygame.Surface((self.light_width, beam_length), pygame.SRCALPHA)
        self.beam_surface.fill((255, 255, 0, 200))

        # Handle
        pygame.draw.rect(self.flashlight_base, self.COLOUR, (35, 1010, 30, 60))
        # Wide part
        pygame.draw.polygon(self.flashlight_base, self.COLOUR, [(0, 960), (100, 960), (65, 1010), (35, 1010)])
        # Rim
        pygame.draw.ellipse(self.flashlight_base, self.RIM, (0, 950, 100, 20))
 
        self.flashlight_base.blit(self.beam_surface, (0, 950 - beam_length))
       
        self.rotated_flashlight = pygame.transform.rotate(self.flashlight_base, -angle)
  
        """
        if is_on:
            beam_x = x_position - (self.light_width // 2)
            pygame.draw.rect(self.mask, (0,0,0,0), (beam_x, 0, self.light_width, self.screen_height - 90))
        """

    def draw(self, surface, x_position, is_on, angle):
        """
        Draws the flashlight onto the bottom of the screen

        Args:
            surface (pygame Surface): surface it's on
            x_position (int): x_position of the flashlight (horizontal)
        """
        rect = self.rotated_flashlight.get_rect()

        # Keeps the center of the flashlight the same when rotating
        rect.center = (x_position, self.screen_height)
        surface.blit(self.rotated_flashlight, rect.topleft)
        surface.blit(self.mask, (0,0))
      
        
