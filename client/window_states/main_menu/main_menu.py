"""_summary_
"""
import pygame
import pygame_menu

from global_config import GlobalConfig
from ..window_state import WindowState


class MainMenu(WindowState):
    """_summary_

    Args:
        WindowState (_type_): _description_
    """

    def __init__(self):
        super().__init__()

        self.login_menu = pygame_menu.Menu(
            "Pong | Login",
            GlobalConfig.screen.get_width(),
            GlobalConfig.screen.get_height(),
            theme=pygame_menu.themes.THEME_DARK,
        )

        self.start_game_menu = pygame_menu.Menu(
            "Pong | Start Game",
            GlobalConfig.screen.get_width(),
            GlobalConfig.screen.get_height(),
            theme=pygame_menu.themes.THEME_DARK,
        )

        self.login_menu.add.text_input("Username", textinput_id="username")
        self.login_menu.add.text_input("Password", textinput_id="password")
        self.login_menu.add.button("Login", self.attempt_login)
        self.login_menu.add.button("Quit", pygame_menu.events.EXIT)

        self.start_game_menu.add.button("Start game", self.start_game)
        self.start_game_menu.add.text_input("Game ID", textinput_id="game_id")
        self.start_game_menu.add.button("Join game", self.join_game)

        self.is_logged_in = False

    def attempt_login(self):
        """_summary_"""
        self.is_logged_in = True
        self.login_menu.disable()

    def start_game(self):
        """_summary_"""
        self._should_switch_state = True
        self.shared_data["player"] = 0
        self.start_game_menu.disable()

    def join_game(self):
        """_summary_"""
        self._should_switch_state = True
        self.shared_data["player"] = 1
        self.start_game_menu.disable()

    def enter_state(self, shared_data: dict[str, str or int]):
        """_summary_

        Args:
            shared_data (dict[str, str or int]): _description_
        """
        super().enter_state(shared_data)
        if not self.is_logged_in:
            self.login_menu.enable()
        else:
            self.start_game_menu.enable()

    def on_loop(self, events: list[pygame.event.Event]):
        """_summary_

        Args:
            events (list[pygame.event.Event]): _description_
        """
        if self.login_menu.is_enabled():
            self.login_menu.update(events)
            if self.login_menu.is_enabled():
                self.login_menu.draw(GlobalConfig.screen)
        elif self.start_game_menu.is_enabled():
            self.start_game_menu.update(events)
            if self.start_game_menu.is_enabled():
                self.start_game_menu.draw(GlobalConfig.screen)

    @classmethod
    @property
    def state_id(cls) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return 0
