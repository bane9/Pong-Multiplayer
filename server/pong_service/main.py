"""_summary_
"""

import asyncio
import websockets
from websockets import server
import sys
import json
import random

player = 0
player1_socket = None
player2_socket = None
player1_done = False
player2_done = False

update_data = {"event": "update", "ball": [50, 50], "player1": [20, 200], "player2": [670, 200]}


def clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(value, max_val))


def rnd_clamp(value: int, min_val=-250, max_val=250) -> int:
    return clamp(value + random.randint(-5, 5), min_val, max_val)


async def update_ball():
    global update_data

    while True:
        update_data["ball"][0] = rnd_clamp(update_data["ball"][0])
        update_data["ball"][1] = rnd_clamp(update_data["ball"][1])

        await asyncio.sleep(0.016666)


async def handle_connect(websocket, _: str):
    global player
    global update_data

    player += 1

    cur_player = player
    player_str = f"player{cur_player}"

    while True:
        data = json.loads(await websocket.recv())

        print("got: ", data)

        if data["evt"] == "update":
            x, y = data["position"]

            update_data[player_str][0] = x
            update_data[player_str][1] = y

            await websocket.send(json.dumps(update_data))

        elif data["evt"] == "query":
            await websocket.send(f'{{"player": {cur_player}}}')


def main():
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    start_server = server.serve(handle_connect, hostname, port)

    asyncio.gather(start_server, update_ball())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
