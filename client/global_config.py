"""_summary_
"""

import pygame


class GlobalConfig:
    """_summary_"""

    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500

    SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

    SCREEN_CLEAR_COLOR = (0, 0, 0)

    FRAMERATE_CAP = 60

    screen: pygame.surface.Surface

    SERVER_PORT = 8080
    SERVER_HOST = "127.0.0.1"
