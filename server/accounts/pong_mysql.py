"""_summary_
"""

import asyncio
import aiomysql
from global_config import GlobalConfig


class PongMySQL:
    PONG_DB = "pong_server"

    def __init__(self):
        self.pool: aiomysql.Pool = None

    async def deinit(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def init(self):
        """_summary_"""
        await self.deinit()

        self.pool = await aiomysql.create_pool(
            host=GlobalConfig.SQL_HOST,
            port=GlobalConfig.SQL_PORT,
            user=GlobalConfig.SQL_USERNAME,
            password=GlobalConfig.SQL_PASSWORD,
            db=self.PONG_DB,
            loop=asyncio.get_event_loop(),
        )

    async def _pserver_execute(self, command: str) -> tuple[bool, str]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(command)
                (result,) = await cur.fetchone()

        ok = True

        if result != "Ok":
            ok = False

        return ok, result

    async def login(self, username: str, password: str) -> tuple[bool, str]:
        return await self._pserver_execute(f'select login_user("{username}", "{password}");')

    async def register(self, username: str, password: str) -> tuple[bool, str]:
        return await self._pserver_execute(f'select register_user("{username}", "{password}");')
