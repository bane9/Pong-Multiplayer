"""_summary_

Returns:
    _type_: _description_
"""

import pygame
import pygame_menu
from global_config import GlobalConfig
from ..window_state import WindowState


class ScoreMenu(WindowState):
    """_summary_

    Args:
        WindowState (_type_): _description_
    """

    def __init__(self):
        super().__init__()

        self.score_menu = pygame_menu.Menu(
            "Pong | Score",
            GlobalConfig.screen.get_width(),
            GlobalConfig.screen.get_height(),
            theme=pygame_menu.themes.THEME_DARK,
        )

        self.score_menu.add.label("Your score", label_id="your_score")
        self.score_menu.add.label("Opponent score", label_id="opponent_score")
        self.score_menu.add.label("winner", label_id="winner")
        self.score_menu.add.button("Back to main menu", self.exit_menu)

    def exit_menu(self):
        """_summary_"""
        self._should_switch_state = True
        self.score_menu.disable()

    def enter_state(self, shared_data: dict[str, str or int]):
        """_summary_

        Args:
            shared_data (dict[str, str or int]): _description_
        """
        super().enter_state(shared_data)

        self.score_menu.enable()

        your_score_label = self.score_menu.get_widget("your_score")
        opponent_score_label = self.score_menu.get_widget("opponent_score")
        winner_label = self.score_menu.get_widget("winner")

        if self.shared_data["player"] == 0:
            your_score = self.shared_data["player1_score"]
            opponent_score = self.shared_data["player2_score"]
        else:
            your_score = self.shared_data["player2_score"]
            opponent_score = self.shared_data["player1_score"]

        your_score_label.set_title(f"Your score: {your_score}")
        opponent_score_label.set_title(f"Opponent's score: {opponent_score}")

        winner_label.set_title("You won!" if your_score > opponent_score else "You lost")

    def on_loop(self, events: list[pygame.event.Event]):
        """_summary_

        Args:
            events (list[pygame.event.Event]): _description_
        """
        if self.score_menu.is_enabled():
            self.score_menu.update(events)
            if self.score_menu.is_enabled():
                self.score_menu.draw(GlobalConfig.screen)

    @classmethod
    @property
    def state_id(cls) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return 2
