"""_summary_
"""

from aiohttp import web
from global_config import GlobalConfig
from pong_mysql import PongMySQL


class PongServer:
    def __init__(self):
        self.sql: PongMySQL = PongMySQL()

    async def init_server(self):
        GlobalConfig.web_server = web.Application()

        GlobalConfig.web_server.add_routes(
            (
                web.post("/login", self.handle_login),
                web.post("/register", self.handle_register),
                web.get("/new_session", self.handle_new_session),
            )
        )

        await self.sql.init()

        runner = web.AppRunner(GlobalConfig.web_server)
        await runner.setup()
        site = web.TCPSite(runner, GlobalConfig.SERVER_HOST, GlobalConfig.SERVER_PORT)
        await site.start()

    async def handle_login(self, request: web.Request):
        data: dict[str, str] = await request.json()

        ok, res = await self.sql.login(data["username"], data["password"])

        return web.Response(text=res, status=200 if ok else 401)

    async def handle_register(self, request: web.Request):
        data: dict[str, str] = await request.json()

        ok, res = await self.sql.register(data["username"], data["password"])

        return web.Response(text=res, status=200 if ok else 401)

    async def handle_new_session(self, request: web.Request):
        pass
