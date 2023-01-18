"""_summary_
"""

from aiohttp import web
from global_config import GlobalConfig
from pong_mysql import PongMySQL
import subprocess
from pong_service import main as pong_main
import sys
import asyncio


class PongServer:
    def __init__(self):
        self.sql: PongMySQL = PongMySQL()
        self.portn = 8765
        self.game_sessions = {}

    async def init_server(self):
        GlobalConfig.web_server = web.Application()

        GlobalConfig.web_server.add_routes(
            (
                web.post("/login", self.handle_login),
                web.post("/register", self.handle_register),
                web.get("/new_session", self.handle_new_session),
                web.get("/get_session", self.handle_get_session),
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

    async def handle_new_session(self, _: web.Request):
        p = subprocess.Popen(
            f'"{sys.executable}" "{pong_main.__file__}" 127.0.0.1 {self.portn}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )

        while True:
            line = p.stdout.readline()
            print(f"{self.portn}:", line.strip())
            if "Started" in line:
                break

        # await asyncio.sleep(1)

        host = f"ws://127.0.0.1:{self.portn}"

        self.game_sessions[self.portn] = host

        self.portn += 1

        return web.json_response({"host": host, "session": self.portn - 1})

    async def handle_get_session(self, request: web.Request):
        request_json = await request.json()
        session = self.game_sessions.get(int(request_json["session"]))

        if session is None:
            return web.Response(text="", status=400)

        return web.Response(text=session)
