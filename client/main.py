"""_summary_
"""

import pygame

from global_config import GlobalConfig
import window_states as ws


def game_loop():
    """_summary_"""
    GlobalConfig.screen = pygame.display.set_mode(GlobalConfig.SCREEN_DIMENSIONS)

    clock = pygame.time.Clock()

    state_manager = ws.WindowStateManager()

    state_manager.add_state(ws.MainMenu())
    state_manager.add_state(ws.PongGame())
    state_manager.add_state(ws.ScoreMenu())

    state_manager.set_state(ws.PongGame.state_id)

    while True:
        GlobalConfig.screen.fill(GlobalConfig.SCREEN_CLEAR_COLOR)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return

        state_manager.on_loop(events)

        pygame.display.flip()

        clock.tick(GlobalConfig.FRAMERATE_CAP)


def main():
    """_summary_"""
    pygame.init()

    pygame.display.set_caption("Pong")

    game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()
