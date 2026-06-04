import pygame 

class Flashlight(pygame.sprite.Sprite):
    """
    Rotatable flashlight that projects a beam from the bottom centre of the screen.

    Uses pixel-perfect masks for beam-ball intersection and a darkness overlay
    so only beam-lit balls are visible.

    Draw in order: draw_mask → draw_beam → draw_flashlight.

    Attributes:
        screen_width (int): Overall screen width
        screen_height (int): Overall screen height
        darkness (int): (colour)
        is_on (bool): whether the beam is currently active
        colour (tuple): RGB for flashlight handle/head
        rim (tuple): RGB for the rim ellipse
        mask (pygame.Surface): full-screen darkness overlay (SRCALPHA)
        beam_width_offset_left (int): beam left half-width
        beam_width_offset_right (int): beam right half-width
        light_width (int): total beam width
        flashlight_base (pygame.Surface): unrotated handle + head
        rotated_flashlight (pygame.Surface): rotated handle + head
        beam_only_base (pygame.Surface): unrotated beam 
        beam_visual_base (pygame.Surface): unrotated translucent beam
        rotated_beam (pygame.Surface): rotated hit-detection beam
        rotated_beam_visual (pygame.Surface): rotated visual beam
        beam_length (int): length 
        beam_alpha (int): alpha 
        beam_colour (tuple): RGBA 
        beam_shape_surface (pygame.Surface): white fill for mask generation
        beam_surface (pygame.Surface): yellow fill for visual beam
        beam_pixel_mask (pygame.Mask): pixel mask for collision

    Methods:
        update(is_on, angle): rebuilds visuals
        ball_under_beam(ball, x_position): beam-ball check
        draw_mask(surface, x_position, balls): draw darkness 
        draw_beam(surface, x_position): draw translucent beam 
        draw_flashlight(surface, x_position): draw handle + head
        _beam_rect(x_position): helper for rotated beam rect
    """
    def __init__(self, screen_height, screen_width, darkness=255):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height 
        self.darkness = darkness
        self.is_on = False

        # Colours for flashlight base
        self.colour = (128, 128, 128)
        self.rim = (220, 220, 220)


        self.mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        # Initializes beam values
        self.beam_width_offset_left = 50
        self.beam_width_offset_right = 50
        self.light_width = self.beam_width_offset_left + self.beam_width_offset_right

        # Create image for flashlight to easily rotate
        self.flashlight_base = pygame.Surface((100, 3 * screen_height), pygame.SRCALPHA)
        self.rotated_flashlight = self.flashlight_base

        # Create beam surfaces
        self.beam_only_base = pygame.Surface((100, 3 * screen_height), pygame.SRCALPHA)
        self.beam_visual_base = pygame.Surface((100, 3 * screen_height), pygame.SRCALPHA)
        self.rotated_beam = self.beam_only_base
        self.rotated_beam_visual = None

        # Beam values
        self.beam_length = self.screen_height * 2
        self.beam_alpha = 90
        self.beam_colour = (255, 255, 0, self.beam_alpha)

        # Shape used for hit detection 
        self.beam_shape_surface = pygame.Surface((self.light_width, self.beam_length), pygame.SRCALPHA)
        self.beam_shape_surface.fill((255, 255, 255, 255))
        self.beam_surface = pygame.Surface((self.light_width, self.beam_length), pygame.SRCALPHA)
        self.beam_surface.fill(self.beam_colour)


    def update(self, is_on, angle):
        """
        Args:
            is_on (bool): whether the beam is active
            angle (float): beam direction in degrees (0 = up)
        """
        self.is_on = is_on
        self.flashlight_base.fill((0,0,0,0))
        self.beam_only_base.fill((0,0,0,0))
        self.beam_visual_base.fill((0, 0, 0, 0))
        self.rotated_beam_visual = None

        self.mask.fill((0, 0, 0, self.darkness))
        if is_on:
            beam_y = self.screen_height + 250 - self.beam_length
            # For hit detection, blits transparent shape 
            self.beam_only_base.blit(self.beam_shape_surface, (0, beam_y))

            # Blits beam (coloured) onto visual base if flashlight is on
            self.beam_visual_base.blit(self.beam_surface, (0, beam_y))

        # Handle
        pygame.draw.rect(self.flashlight_base, self.colour, (35, self.screen_height + 310, 30, 60))
        # Wide part
        pygame.draw.polygon(self.flashlight_base, self.colour, [(0, self.screen_height + 260), (100, self.screen_height + 260), (65, self.screen_height + 310), (35, self.screen_height + 310)])
        # Rim
        pygame.draw.ellipse(self.flashlight_base, self.rim, (0, self.screen_height + 250, 100, 20))
 
        # Rotates flashlight and beam
        self.rotated_flashlight = pygame.transform.rotate(self.flashlight_base, -angle)
        self.rotated_beam = pygame.transform.rotate(self.beam_only_base, -angle)

        # Flashlight is turned on
        if is_on:
            self.rotated_beam_visual = pygame.transform.rotate(self.beam_visual_base, -angle)
            # Mask to check collisions with balls
            self.beam_pixel_mask = pygame.mask.from_surface(self.rotated_beam, threshold=1)
        else:
            # No collisions with balls whne beam is not on
            self.beam_pixel_mask = None

    def _beam_rect(self, x_position):
        """
        Gets the rectangle of the rotated beam for blitting and collision detection
        Args
            x_position (int): x position of flashlight
        Returns:
            (rect)
        """
        rect = self.rotated_beam.get_rect()
        rect.center = (x_position, self.screen_height)
        return rect

    def ball_under_beam(self, ball, x_position):
        """
        Checks intersection between ball and beam

        Args
            ball (Sprite): ball to check
            x_position (int): x position of flashlight
        Returns
            self.beam_pixe_mask.overlap(tuple) if intersection or none if no intersection
        """
        if not self.is_on or self.beam_pixel_mask is None:
            return False
        beam_rect = self._beam_rect(x_position)
        ball_mask = pygame.mask.from_surface(ball.image, threshold=1)
        offset = (ball.rect.x - beam_rect.x, ball.rect.y - beam_rect.y)
        return self.beam_pixel_mask.overlap(ball_mask, offset) is not None

    def draw_mask(self, surface, x_position, balls=None):
        """
        Draws the darkness mask over balls. When on, redraws balls overlapping the beam shape 
        Args
            surface (Surface): surface to draw on
            x_position (int): x position of flashlight
            balls (list(sprite)): group of balls to check for overlap with beam
        """
        surface.blit(self.mask, (0, 0))
        if self.is_on and balls:
            for ball in balls:
                # Checks if there is intersection point
                if self.ball_under_beam(ball, x_position):
                    # Blits ball over, so ball is sen over mask
                    surface.blit(ball.image, ball.rect)

    def draw_beam(self, surface, x_position):
        """
        Draws translucent yellow beam over visible balls.
        Args
            surface (Surface): surface to draw on
            x_position (int): x position of flashlight
        Returns
            Returns None if flashlight off, otherwise draws beam (no return value)
        """
        # If beam not on, return None
        if not self.is_on:
            return None
        rect = self._beam_rect(x_position)
        surface.blit(self.rotated_beam_visual, rect.topleft)

    def draw_flashlight(self, surface, x_position):
        """
        Draws the flashlight body (handle and head)
        Args
            surface (Surface): surface to draw on
            x_position (int): x position of flashlight
        """
        rect = self.rotated_flashlight.get_rect()
        rect.center = (x_position, self.screen_height)
        surface.blit(self.rotated_flashlight, rect.topleft)
