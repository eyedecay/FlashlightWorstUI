import pygame


class Timer:
    """
    Timer Class for countdown interval 

    Attributes:
        _interval (int): length of countdown in milliseconds
        _last_ticks (int): pygame tick count for last reset
    Methods:
        reset: restarts the timer
    """
    def __init__(self, interval=60000):
        """
        Creates instance

        Args:
            interval (int): countdown length (default 60000 miliseconds)
        """
        self._interval = interval
        self._last_ticks = pygame.time.get_ticks()

    @property
    def interval(self):
        """
        returns the countdown interval in milliseconds

        Returns
            (int): (miliseconds)
        """
        return self._interval

    @property
    def expired(self):
        """
        checks if the countdown has elapsed since last reset

        Returns
            (bool)
        """
        return pygame.time.get_ticks() - self._last_ticks >= self._interval

    @property
    def seconds_left(self):
        """
        returns number of seconds remaining 

        Returns
            (int)
        """
        return max(0, (self._interval - (pygame.time.get_ticks() - self._last_ticks)) // 1000)

    def reset(self):
        """
        restarts the timer by recording current tick count
        """
        self._last_ticks = pygame.time.get_ticks()
