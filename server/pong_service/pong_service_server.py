import json
from typing import Callable, Awaitable
from websockets import server, exceptions as ws_exceptions
from websockets.server import WebSocketServerProtocol


class PongServiceServer:
    def __init__(
        self,
        hostname: str,
        port: int,
        on_connect: Callable[[int], Awaitable[None]] = None,
        on_receive: Callable[[int, dict], Awaitable[None]] = None,
        on_disconnect: Callable[[int], Awaitable[None]] = None,
    ):
        self.hostname = hostname
        self.port = port
        self._connection_num = 0
        self._connections: dict[int, WebSocketServerProtocol] = {}

        self.on_connect = on_connect
        self.on_receive = on_receive
        self.on_disconnect = on_disconnect

        self.server = None

    def set_callbacks(
        self,
        on_connect: Callable[[int], Awaitable[None]],
        on_receive: Callable[[int, dict], Awaitable[None]],
        on_disconnect: Callable[[int], Awaitable[None]],
    ):
        self.on_connect = on_connect
        self.on_receive = on_receive
        self.on_disconnect = on_disconnect

    async def _connect_handler(self, websocket: WebSocketServerProtocol, _: str):
        self._connection_num += 1
        self._connections[self._connection_num] = websocket

        connection = self._connection_num
        await self.on_connect(connection)

        while True:
            msg = None
            try:
                msg = json.loads(await websocket.recv())
            except TypeError as e:
                print(e)
            except ws_exceptions.ConnectionClosedError:
                self._connections.pop(connection)
                await self.on_disconnect(connection)

            if msg is not None:
                await self.on_receive(connection, msg)

    def get_async_object(self):
        if self.server is None:
            self.server = server.serve(self._connect_handler, self.hostname, self.port)

        return self.server

    async def send(self, ws_idx: int, data: dict or list):
        data = json.dumps(data)
        await self._connections[ws_idx].send(data)

    async def disconnect(self, ws_idx: int):
        await self._connections[ws_idx].close()
        self._connections.pop(ws_idx)

    def active_connections(self) -> int:
        return len(self._connections)
