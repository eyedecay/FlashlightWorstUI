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
        self.flashlight_base = pygame.Surface((100, 120), pygame.SRCALPHA)
        # Handle
        pygame.draw.rect(self.flashlight_base, self.COLOUR, (35, 60, 30, 60))
        # Wide part
        pygame.draw.polygon(self.flashlight_base, self.COLOUR, [(0, 10), (100, 10), (65, 60), (35, 60)])
        # Rim
        pygame.draw.ellipse(self.flashlight_base, self.RIM, (0, 0, 100, 20))
    
    @staticmethod
    def rotate_polygon(points, pivot, angle):
        """Rotates a list of points around a pivot point by an angle in degrees."""
        pivot_vector = pygame.math.Vector2(pivot)
        
        rotated_points = []
        for x, y in points:
            rotated_vector = (pygame.math.Vector2(x, y) - pivot_vector).rotate(angle * 180) + pivot_vector
            rotated_points.append(rotated_vector)
        
        return rotated_points

    def update(self, x_position, is_on):
        
        self.mask.fill((0,0,0, self.darkness))

        
        if is_on:
            beam_x = x_position - (self.light_width // 2)
            pygame.draw.rect(self.mask, (0,0,0,0), (beam_x, 0, self.light_width, self.screen_height - 90))
            
    
    def draw(self, surface, x_position, is_on, angle):
        """
        Draws the flashlight onto the bottom of the screen

        Args:
            surface (pygame Surface): surface it's on
            x_position (int): x_position of the flashlight (horizontal)
        """
        
        if is_on:
            
            # Flashlight Beam
            self.beam_points = [
            (x_position - self.beam_width_offset_left, self.screen_height - 110),
            (x_position + self.beam_width_offset_right, self.screen_height - 110),
            (x_position + self.beam_width_offset_right + 300, -1000), # Widens out at the top
            (x_position - self.beam_width_offset_left - 300, -1000)
            ]
            
            # Rotates beam
            rotated_beam = Flashlight.rotate_polygon(self.beam_points, (x_position, self.screen_height), angle)
        
            beam_x = x_position - (self.light_width // 2)
            beam_surface = pygame.Surface((self.light_width, self.screen_height - 90), pygame.SRCALPHA)
            
            # Draws the rotated beam onto the surface
            pygame.draw.polygon(beam_surface, self.BEAM_COLOUR, rotated_beam)
            
            # Blits beam
            surface.blit(beam_surface, (beam_x, 0))

        surface.blit(self.mask, (0,0))
        rotated_flashlight = pygame.transform.rotate(self.flashlight_base, -angle)
        
        flashlight_center = x_position
        
        rect = rotated_flashlight.get_rect()
        surface.blit(rotated_flashlight, (x_position - 60, self.screen_height -150))
  





