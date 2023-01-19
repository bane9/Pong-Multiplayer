from dataclasses import dataclass
import asyncio
from random import randint
from pong_service_server import PongServiceServer
import sys


@dataclass
class AABB:
    x: int
    y: int
    width: int
    height: int

    def is_coliding(self, other: "AABB") -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )


class Ball:
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()

        self.velocity = [randint(4, 8), randint(-8, 8)]

        self.rect = AABB(x, y, width, height)

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


def clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(value, max_val))


class Paddle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = AABB(x, y, width, height)

    def update_position(self, new_y):
        self.rect.y = clamp(new_y, 0, 400)

    def get_position(self) -> tuple[int, int]:
        return self.rect.x, self.rect.y


def are_objects_coliding(obj1: Ball or Paddle, obj2: Ball or Paddle):
    return obj1.rect.is_coliding(obj2.rect)


class PongGameService:
    def __init__(self, server: PongServiceServer, max_score=5):
        self.max_score = max_score

        self.ball = Ball(50, 50, 10, 10)

        self.player1 = Paddle(20, 200, 10, 100)
        self.player2 = Paddle(670, 200, 10, 100)

        self._two_players_joined = False

        self.score1 = 0
        self.score2 = 0

        self.server = server

        server.set_callbacks(self._on_connect, self._on_receive, self._on_disconnect)

    async def _update_ball(self):
        print("Started")

        while True:
            if self._two_players_joined:
                if self.ball.rect.x >= 690:
                    self.score1 += 1
                    self.ball.velocity[0] = -self.ball.velocity[0]
                elif self.ball.rect.x <= 0:
                    self.score2 += 1
                    self.ball.velocity[0] = -self.ball.velocity[0]

                if self.ball.rect.y > 490:
                    self.ball.velocity[1] = -self.ball.velocity[1]
                elif self.ball.rect.y < 0:
                    self.ball.velocity[1] = -self.ball.velocity[1]

                self.ball.update()

                if are_objects_coliding(self.ball, self.player1) or are_objects_coliding(self.ball, self.player2):
                    self.ball.bounce()

                if self.is_game_over():
                    return

            await asyncio.sleep(0.016666)

    def is_game_over(self) -> bool:
        return self.max_score in (self.score1, self.score2)

    def get_async_object(self):
        return self._update_ball()

    async def _on_connect(self, index: int):
        if index == 2:
            self._two_players_joined = True

    async def _on_disconnect(self, _: int):
        if self.server.active_connections() == 0:
            sys.exit(0)

    async def _on_receive(self, ws_idx: int, data: dict[str, str or int]):
        match data["evt"]:
            case "query":
                await self.server.send(ws_idx, {"player": ws_idx})
            case "update":
                if self.is_game_over():
                    await self.server.send(ws_idx, {"status": "end", "score1": self.score1, "score2": self.score2})

                    await self.server.disconnect(ws_idx)

                    if self.server.active_connections() == 0:
                        sys.exit(0)

                    return

                if ws_idx == 1:
                    self.player1.update_position(data["position"])
                elif ws_idx == 2:
                    self.player2.update_position(data["position"])

                await self.server.send(
                    ws_idx,
                    {
                        "status": "run",
                        "event": "update",
                        "ball": list(self.ball.get_position()),
                        "player1": list(self.player1.get_position()),
                        "player2": list(self.player2.get_position()),
                        "score1": self.score1,
                        "score2": self.score2,
                    },
                )
