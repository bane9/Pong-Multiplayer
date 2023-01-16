"""_summary_

Returns:
    _type_: _description_
"""

import asyncio
from pong_server import PongServer


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    server = PongServer()

    asyncio.ensure_future(server.init_server())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == "__main__":
    main()
