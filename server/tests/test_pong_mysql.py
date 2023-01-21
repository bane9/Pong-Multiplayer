from pong_mysql import PongMySQL
import pytest
import types


@pytest.mark.asyncio
async def test_login_and_register():
    server = PongMySQL()

    out_str = ""

    username = "username"
    password = "password"

    async def _pserver_execute(self, command: str):
        nonlocal out_str

        out_str = command

    server._pserver_execute = types.MethodType(_pserver_execute, server)

    await server.register(username, password)

    assert out_str == f'select register_user("{username}", "{password}");'

    await server.login(username, password)

    assert out_str == f'select login_user("{username}", "{password}");'
