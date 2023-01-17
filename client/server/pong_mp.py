import threading
import asyncio
import websockets
import janus
import json
import time


class ServerCommunicator:
    def __init__(self):
        self.tx_queue: janus.Queue = None
        self.rx_queue: janus.Queue = None
        self._address = ""
        self._running = False
        self._thread: threading.Thread = None
        self._loop: asyncio.AbstractEventLoop = None

    def connect(self, address: str):
        self._address = address
        self._thread = threading.Thread(target=self._connection_thread)
        self._thread.start()

        while not self._running:
            time.sleep(0.1)

    def disconnect(self):
        self._loop.call_soon_threadsafe(asyncio.futures.Future, self._disconnect())
        self._thread.join()

    async def _disconnect(self):
        self._running = False
        self._loop.close()

    async def _connection_loop(self):
        self.rx_queue = janus.Queue()
        self.tx_queue = janus.Queue()

        self._running = True

        async with websockets.connect(self._address) as websocket:
            while self._running:
                send = await self.tx_queue.async_q.get()
                await websocket.send(send)
                recv = await websocket.recv()
                await self.rx_queue.async_q.put(recv)

    def _connection_thread(self):
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self._connection_loop())

        if self._running:
            self._loop.close()

    def transcieve(self, data: dict[str, str or int]) -> dict[str, str or int]:
        self.tx_queue.sync_q.put(json.dumps(data))
        recv = self.rx_queue.sync_q.get()

        data = json.loads(recv)
        # print(data)

        return data
