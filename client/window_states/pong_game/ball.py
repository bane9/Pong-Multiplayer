"""_summary_

Returns:
    _type_: _description_
"""

from random import randint
import pygame


class Ball(pygame.sprite.Sprite):
    """_summary_

    Args:
        pygame (_type_): _description_
    """

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]

        self.rect = self.image.get_rect()

    def update(self):
        """_summary_"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        """_summary_"""
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

    def set_position(self, x: int, y: int):
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_
        """
        self.rect.x = x
        self.rect.y = y

    def get_position(self) -> tuple[int, int]:
        """_summary_

        Returns:
            tuple[int, int]: _description_
        """
        return self.rect.x, self.rect.y
