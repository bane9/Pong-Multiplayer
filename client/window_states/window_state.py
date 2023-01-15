"""_summary_
"""

from abc import ABC, abstractmethod
import pygame


class WindowState(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """

    def __init__(self):
        self.shared_data: dict[str, str or int] = {}
        self._should_switch_state = False

    def get_shared_data(self) -> dict[str, str or int]:
        """_summary_

        Returns:
            dict[str, str or int]: _description_
        """
        return self.shared_data

    def set_shared_data(self, shared_data: dict[str, str or int]):
        """_summary_

        Args:
            shared_data (dict[str, str or int]): _description_
        """
        self.shared_data = shared_data

    def enter_state(self, shared_data: dict[str, str or int]):
        """_summary_

        Args:
            shared_data (dict[str, str or int]): _description_
        """
        self.set_shared_data(shared_data)

    def exit_state(self) -> dict[str, str or int]:
        """_summary_

        Returns:
            dict[str, str or int]: _description_
        """
        self._should_switch_state = False
        return self.get_shared_data()

    @abstractmethod
    def on_loop(self, events: list[pygame.event.Event]):
        """_summary_

        Args:
            events (list[pygame.event.Event]): _description_
        """

    def should_switch_state(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self._should_switch_state

    @classmethod
    def state_id(cls) -> int:
        """_summary_

        Raises:
            NotImplementedError: _description_

        Returns:
            int: _description_
        """

        raise NotImplementedError()
