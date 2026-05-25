import pygame 

class Flashlight(pygame.sprite.Sprite):
    """
    Flashlight Class

    Attributes:
        screen_width (int): Overall screen width
        screen_height (int): Overall Screen height
        radius (int): radius of light beem
        darkness: (colour)
        COLOUR (tuple): Background colour
        RIM_COLOUR (tuple): RIM colour RGB
        BEAM_COLOUR (tuple): RGB for yellow
        mask (pygame.surface):
        beam_width_offset_left (int): half width of beam
        beam_width_offset_right (int): half width of beam
        light_width (int): beam pixel width
    """
    def __init__(self, screen_height, screen_width, radius = 100, darkness = 200):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height 
        self.radius = radius 
        self.darkness = darkness

        self.COLOUR = (128, 128, 128)
        self.RIM_COLOUR = (220, 220, 220)
        self.BEAM_COLOUR = (255, 255, 0, 100)

        self.mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        self.beam_width_offset_left = 50
        self.beam_width_offset_right = 50
        self.light_width = self.beam_width_offset_left + self.beam_width_offset_right

    def update(self, x_position, is_on):
        
        self.mask.fill((0,0,0, self.darkness))

        
        if is_on:
            beam_x = x_position - (self.light_width // 2)
            pygame.draw.rect(self.mask, (0,0,0,0), (beam_x, 0, self.light_width, self.screen_height - 90))
            
    
    def draw(self, surface, x_position, is_on):
        """
        Draws the flashlight onto the bottom of the screen

        Args:
            surface (pygame Surface): surface it's on
            x_position (int): x_position of the flashlight (horizontal)
        """


        if is_on:
            beam_x = x_position - (self.light_width // 2)
            beam_surface = pygame.Surface((self.light_width, self.screen_height - 90), pygame.SRCALPHA)
            beam_surface.fill(self.BEAM_COLOUR)
            surface.blit(beam_surface, (beam_x, 0))

        surface.blit(self.mask, (0,0))

        handle_width = 40
        handle_height = 80
        handle_x, handle_y = x_position - (handle_width //2), self.screen_height - 50
        pygame.draw.rect(surface, self.COLOUR, (handle_x, handle_y, handle_width, handle_height))

        #wider flashlight point
        wide_part_points = [
            (x_position - self.beam_width_offset_left, self.screen_height - 90), 
            (x_position + self.beam_width_offset_right, self.screen_height - 90), 
            (x_position + 30, self.screen_height - 55), 
            (x_position - 30, self.screen_height - 55), 
        ]

        pygame.draw.polygon(surface, self.COLOUR, wide_part_points)
        pygame.draw.ellipse(surface, self.RIM_COLOUR, (x_position - 50, self.screen_height, 100, 20))




