"""_summary_

Returns:
    _type_: _description_
"""

import pygame

from .window_state import WindowState


class WindowStateManager:
    """_summary_"""

    def __init__(self, window_states: list[WindowState] = None):
        self.state_index = 0
        self.window_states: list[WindowState] = window_states

        if window_states is None:
            self.window_states = []

        self._sort_states()

    def _sort_states(self):
        """_summary_"""
        self.window_states.sort(key=lambda x: x.state_id)

    def add_state(self, window_state: WindowState):
        """_summary_

        Args:
            window_state (WindowState): _description_
        """
        self.window_states.append(window_state)

        self._sort_states()

    def remove_state(self, state_id: int):
        """_summary_

        Args:
            state_id (int): _description_
        """
        self.window_states = filter(lambda x: x.state_id != state_id, self.window_states)

    def _get_current_state(self) -> WindowState:
        """_summary_

        Returns:
            WindowState: _description_
        """
        return self.window_states[self.state_index]

    def _set_state(self, index: int):
        """_summary_

        Args:
            index (int): _description_
        """
        old_state = self._get_current_state()

        self.state_index = index

        new_state = self._get_current_state()

        shared_data = old_state.exit_state()

        new_state.enter_state(shared_data)

    def next_state(self):
        """_summary_"""
        self._set_state((self.state_index + 1) % len(self.window_states))

    def previous_state(self):
        """_summary_"""
        index = self.state_index - 1

        if index == -1:
            index = len(self.window_states - 1)

        self._set_state(index)

    def set_state(self, state_id: int):
        """_summary_

        Args:
            state_id (int): _description_
        """
        for i, x in enumerate(self.window_states):
            if x.state_id == state_id:
                self._set_state(i)
                return

    def on_loop(self, events: list[pygame.event.Event]):
        """_summary_

        Args:
            events (list[pygame.event.Event]): _description_
        """
        currnet_state = self._get_current_state()
        currnet_state.on_loop(events)

        if currnet_state.should_switch_state():
            self.next_state()
