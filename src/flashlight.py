import pygame


class Flashlight(pygame.sprite.Sprite):
    """
    Flashlight that projects a rotatable beam 

    Attributes:
        screen_width (int): Overall screen width
        screen_height (int): Overall screen height
        beam_width (int): pixel number (width)
        handle_length (int): pixel number (length)
        darkness (int): colour
    """
    HANDLE_WIDTH = 30
    HEAD_HEIGHT = 60
    HANDLE_COLOUR = (128, 128, 128)
    RIM_COLOUR = (220, 220, 220)

    def __init__(self, screen_width, screen_height, beam_width=100, handle_length=60, darkness=200):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.beam_width = beam_width
        self.handle_length = handle_length
        self.darkness = darkness

        self.mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        base_height = 3 * screen_height
        self.flashlight_base = pygame.Surface((beam_width, base_height), pygame.SRCALPHA)
        self.rotated_flashlight = None

        self.beam_length = screen_height * 2
        self.beam_surface = pygame.Surface((beam_width, self.beam_length), pygame.SRCALPHA)
        self.beam_surface.fill((255, 255, 0, 200))

        centre_y = base_height // 2
        outlet_y = centre_y - 100
        handle_x = (beam_width - self.HANDLE_WIDTH) // 2

        self._outlet_y = outlet_y
        self._handle_x = handle_x
        self._wide_bottom = outlet_y + self.HEAD_HEIGHT

    def update(self, is_on, angle):
        """
        Rebuilds the flashlight visual for the current frame.

        Args:
            is_on (bool): whether the beam is active
            angle (float): beam direction in degrees (0 = up)
        """
        base = self.flashlight_base
        base.fill((0, 0, 0, 0))
        self.mask.fill((0, 0, 0, 0))

        outlet = self._outlet_y
        handle_x = self._handle_x
        wide_bottom = self._wide_bottom
        beam_width = self.beam_width

        if is_on:
            base.blit(self.beam_surface, (0, outlet - self.beam_length))
        else:
            self.mask.fill((0, 0, 0, self.darkness))

        # Rim
        pygame.draw.ellipse(base, self.RIM_COLOUR, (0, outlet, beam_width, 20))
        # Wide part — trapezoid narrowing from beam_width to HANDLE_WIDTH
        pygame.draw.polygon(base, self.HANDLE_COLOUR, [(0, outlet + 10), (beam_width, outlet + 10), (handle_x + self.HANDLE_WIDTH, wide_bottom), (handle_x, wide_bottom)])
        # Handle
        pygame.draw.rect(base, self.HANDLE_COLOUR, (handle_x, wide_bottom, self.HANDLE_WIDTH, self.handle_length))

        self.rotated_flashlight = pygame.transform.rotate(base, -angle)

    def draw(self, surface, x_position):
        """
        Draws the flashlight onto the bottom 

        Args:
            surface (pygame Surface): surface it's on
            x_position (int): x_position of the flashlight (horizontal)
        """
        rect = self.rotated_flashlight.get_rect()

        # Keeps the center of the flashlight the same when rotating
        rect.center = (x_position, self.screen_height)
        surface.blit(self.rotated_flashlight, rect.topleft)
        surface.blit(self.mask, (0, 0))
