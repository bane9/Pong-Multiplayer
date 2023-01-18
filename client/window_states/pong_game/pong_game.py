"""_summary_

Returns:
    _type_: _description_
"""

import pygame

from global_config import GlobalConfig
from server import ServerCommunicator

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
        self.opponent: Paddle = None

        self.player_idx = 0
        self.opponent_idx = 0

        self.com = ServerCommunicator()

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

        self.com.connect(shared_data["instance_host"])

        window_caption = "Pong"

        if "session_id" in shared_data and shared_data["session_id"]:
            window_caption += f' | Game ID: {shared_data["session_id"]}'

        pygame.display.set_caption(window_caption)

        shared_data["player"] = self.com.transcieve({"evt": "query"})["player"]

        if shared_data["player"] == 1:
            self.player = self.paddleA
            self.opponent = self.paddleB
            self.player_idx = 1
            self.opponent_idx = 2
        else:
            self.player = self.paddleB
            self.opponent = self.paddleA
            self.player_idx = 2
            self.opponent_idx = 1

    def on_loop(self, _: list[pygame.event.Event]):
        """_summary_

        Args:
            _ (list[pygame.event.Event]): _description_
        """
        keys = pygame.key.get_pressed()

        player_pos = list(self.player.get_position())

        if keys[pygame.K_UP]:
            player_pos[1] -= 5
        elif keys[pygame.K_DOWN]:
            player_pos[1] += 5

        recv = self.com.transcieve({"evt": "update", "position": player_pos[1]})

        if recv["status"] == "run":
            self.player.set_position(*recv[f"player{self.player_idx}"])
            self.opponent.set_position(*recv[f"player{self.opponent_idx}"])
            self.ball.set_position(*recv["ball"])

            self.all_sprites_list.update()

            pygame.draw.line(GlobalConfig.screen, self.WHITE, (349, 0), (349, 500), 5)

            font = pygame.font.Font(None, 74)
            text = font.render(str(recv["score1"]), 1, self.WHITE)
            GlobalConfig.screen.blit(text, (250, 10))
            text = font.render(str(recv["score2"]), 1, self.WHITE)
            GlobalConfig.screen.blit(text, (420, 10))

            self.all_sprites_list.draw(GlobalConfig.screen)
        elif recv["status"] == "end":
            self._should_switch_state = True
            if self.shared_data["player"] == 1:
                self.shared_data["player_score"] = recv["score1"]
                self.shared_data["opponent_score"] = recv["score2"]
            else:
                self.shared_data["player_score"] = recv["score2"]
                self.shared_data["opponent_score"] = recv["score1"]
            self.com.disconnect()

    @classmethod
    @property
    def state_id(cls) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return 1
