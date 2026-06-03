import pygame


class Lock:
    """
    Lock Class for 6-digit verification code collection

    Attributes:
        _x (int): x-coordinate of the lock display
        _y (int): y-coordinate of the first box
        _code_digits (list): 6-digit target code 
        _collected (list): digits collected so far
        _font (pygame.Font): font used 
    Methods:
        try_collect: attempts to collect a digit in order
        reset: sets a new code 
        skip: fills first n slots with correct digits (Manual skip button for random testing)
        draw: renders the lock
    """
    BOX_SIZE = 60
    BOX_GAP = 15

    def __init__(self, x=1050, y=80):
        """
        initializes a new lock

        Args:
            x (int): x-coordinate of the lock display (default 1050)
            y (int): y-coordinate of the first box (default 80)
        """
        self._x = x
        self._y = y
        self._code_digits = []
        self._collected = []
        self._font = pygame.font.SysFont('Arial', 32)

    @property
    def code_digits(self):
        """
        returns the target verification code digits

        Returns
            (list)
        """
        return self._code_digits

    @property
    def collected(self):
        """
        Returns digits collected 

        Returns
            (list)
        """
        return list(self._collected)

    @property
    def is_full(self):
        """
        Checks if all 6 digits have been collected

        Returns
            (bool)
        """
        return len(self._collected) == 6

    def try_collect(self, digit):
        """
        Sees if a digit matches the next required digit

        Args:
            digit (int): the digit 
        Returns
            (bool): if it matches
        """
        if len(self._collected) < 6 and digit == self._code_digits[len(self._collected)]:
            self._collected.append(digit)
            return True
        return False

    def reset(self, new_code_digits):
        """
        sets a new verification code 

        Args:
            new_code_digits (list): 6-digit code as list of ints
        """
        self._code_digits = new_code_digits
        self._collected = []

    def skip(self, n):
        """
        fills the first n slots with the correct code digits (shortcut)

        Args:
            n (int): number of slots to fill
        """
        self._collected = self._code_digits[:n]

    def draw(self, screen):
        """
        Draws the lock display 

        Args:
            screen (pygame.Surface): surface pygame
        """
        lock_text = self._font.render("LOCK", True, (200, 200, 200))
        screen.blit(lock_text, (self._x, self._y - 25))
        for i in range(len(self._code_digits)):
            box_x = self._x
            box_y = self._y + i * (self.BOX_SIZE + self.BOX_GAP)
            if i < len(self._collected):
                pygame.draw.rect(screen, (0, 200, 0), (box_x, box_y, self.BOX_SIZE, self.BOX_SIZE))
                digit_text = self._font.render(str(self._collected[i]), True, (255, 255, 255))
                screen.blit(digit_text, (box_x + self.BOX_SIZE // 2 - digit_text.get_width() // 2,
                                         box_y + self.BOX_SIZE // 2 - digit_text.get_height() // 2))
            else:
                pygame.draw.rect(screen, (60, 60, 60), (box_x, box_y, self.BOX_SIZE, self.BOX_SIZE), 3)
