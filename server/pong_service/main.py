"""_summary_
"""
import sys
import json
import asyncio
from random import randint
from websockets import server

MAX_SCORE = 5


class Rect:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def is_coliding(cordinates1: Rect, rect1: Rect, coordinates2: Rect, rect2: Rect) -> bool:
    return (
        cordinates1.x < coordinates2.x + rect2.x
        and cordinates1.x + rect1.x > coordinates2.x
        and cordinates1.y < coordinates2.y + rect2.y
        and cordinates1.y + rect1.y > coordinates2.y
    )


class Ball:
    """_summary_

    Args:
        pygame (_type_): _description_
    """

    def __init__(self, width, height):
        super().__init__()

        self.velocity = [randint(4, 8), randint(-8, 8)]

        self.rect = Rect(width, height)

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


player = 0
player1_socket = None
player2_socket = None
player1_done = False
player2_done = False
ball = Ball(10, 10)
update_data = {
    "event": "update",
    "ball": [50, 50],
    "player1": [20, 200],
    "player2": [670, 200],
    "score1": 0,
    "score2": 0,
}


def is_ball_coliding() -> bool:
    global update_data
    global ball
    ball_rect = Rect(10, 10)
    ball_pos = Rect(*ball.get_position())
    player_rect = Rect(10, 100)
    player1_pos = Rect(*update_data["player1"])
    player2_pos = Rect(*update_data["player2"])

    return is_coliding(ball_pos, ball_rect, player1_pos, player_rect) or is_coliding(
        ball_pos, ball_rect, player2_pos, player_rect
    )


def clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(value, max_val))


async def update_ball():
    global update_data
    global ball
    global player

    print("Started")

    while True:
        if player >= 2:
            if ball.rect.x >= 690:
                update_data["score1"] += 1
                ball.velocity[0] = -ball.velocity[0]
            elif ball.rect.x <= 0:
                update_data["score2"] += 1
                ball.velocity[0] = -ball.velocity[0]

            if ball.rect.y > 490:
                ball.velocity[1] = -ball.velocity[1]
            elif ball.rect.y < 0:
                ball.velocity[1] = -ball.velocity[1]

            ball.update()

            if is_ball_coliding():
                ball.bounce()

            update_data["ball"] = ball.get_position()

            if update_data["score1"] == MAX_SCORE or update_data["score2"] == MAX_SCORE:
                return

        await asyncio.sleep(0.016666)


async def handle_connect(websocket, _: str):
    global player
    global update_data

    player += 1

    cur_player = player
    player_str = f"player{cur_player}"

    while True:
        data = json.loads(await websocket.recv())

        if data["evt"] == "update":
            if update_data["score1"] == MAX_SCORE or update_data["score2"] == MAX_SCORE:
                await websocket.send(
                    json.dumps({"status": "end", "score1": update_data["score1"], "score2": update_data["score2"]})
                )

                player -= 1

                if player <= 0:
                    sys.exit(0)

            y = data["position"]

            update_data[player_str][0] = 20 if cur_player == 1 else 670
            update_data[player_str][1] = clamp(y, 0, 400)

            to_send = {"status": "run", **update_data}

            await websocket.send(json.dumps(to_send))

        elif data["evt"] == "query":
            await websocket.send(f'{{"player": {cur_player}}}')


def main():
    print("Service booted", sys.argv)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    print(f"{hostname=} {port=}")

    start_server = server.serve(handle_connect, hostname, port)

    asyncio.gather(start_server, update_ball())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
