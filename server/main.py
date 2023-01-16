"""_summary_

Returns:
    _type_: _description_
"""

import asyncio
from aiohttp import web
from global_config import GlobalConfig


async def handle(request: web.Request):
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def main():
    GlobalConfig.web_server = web.Application()

    GlobalConfig.web_server.add_routes([web.get("/", handle), web.get("/{name}", handle)])

    runner = web.AppRunner(GlobalConfig.web_server)
    await runner.setup()
    site = web.TCPSite(runner, GlobalConfig.SERVER_HOST, GlobalConfig.SERVER_PORT)
    await site.start()


def init_main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    asyncio.ensure_future(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == "__main__":
    init_main()
