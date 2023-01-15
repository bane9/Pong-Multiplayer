"""_summary_

Returns:
    _type_: _description_
"""

import pygame

from global_config import GlobalConfig

from .ball import Ball
from .paddle import Paddle
from ..window_state import WindowState


class PongGame(WindowState):
    """_summary_

    Args:
        WindowState (_type_): _description_

    Returns:
        _type_: _description_
    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    LEVEL_CAP = 3

    def __init__(self):
        super().__init__()

        self.paddleA = Paddle(self.WHITE, 10, 100)

        self.paddleB = Paddle(self.WHITE, 10, 100)

        self.ball = Ball(self.WHITE, 10, 10)

        self.all_sprites_list = pygame.sprite.Group()

        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

        self.scoreA = 0
        self.scoreB = 0

        self.player: Paddle = None

    def _reset(self):
        """_summary_"""
        self.ball.set_position(345, 195)

        self.paddleA.set_position(20, 200)

        self.paddleB.set_position(670, 200)

        self.scoreA = 0
        self.scoreB = 0

    def enter_state(self, shared_data: dict[str, str or int]):
        """_summary_

        Args:
            shared_data (dict[str, str or int]): _description_
        """
        self.set_shared_data(shared_data)
        self._reset()

        if shared_data["player"] == 0:
            self.player = self.paddleA
        else:
            self.player = self.paddleB

    def on_loop(self, _: list[pygame.event.Event]):
        """_summary_

        Args:
            _ (list[pygame.event.Event]): _description_
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move_up(5)
        elif keys[pygame.K_DOWN]:
            self.player.move_down(5)

        self.all_sprites_list.update()

        if self.ball.rect.x >= 690:
            self.scoreA += 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x <= 0:
            self.scoreB += 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y > 490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
            self.ball.bounce()

        pygame.draw.line(GlobalConfig.screen, self.WHITE, (349, 0), (349, 500), 5)

        self.all_sprites_list.draw(GlobalConfig.screen)

        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, self.WHITE)
        GlobalConfig.screen.blit(text, (250, 10))
        text = font.render(str(self.scoreB), 1, self.WHITE)
        GlobalConfig.screen.blit(text, (420, 10))

        if self.scoreA >= self.LEVEL_CAP or self.scoreB >= self.LEVEL_CAP:
            self.shared_data["player1_score"] = self.scoreA
            self.shared_data["player2_score"] = self.scoreB
            self._should_switch_state = True

    @classmethod
    @property
    def state_id(cls) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return 1
