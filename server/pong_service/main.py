"""_summary_
"""
import sys
import asyncio

from game import PongGameService
from pong_service_server import PongServiceServer


def main():
    print("Service booted", sys.argv)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    print(f"{hostname=} {port=}")

    server = PongServiceServer(hostname, port)
    game = PongGameService(server, 5)

    asyncio.gather(server.get_async_object(), game.get_async_object())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
