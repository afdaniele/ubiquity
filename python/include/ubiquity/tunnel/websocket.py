import asyncio
import websockets
from abc import ABC
from websockets import WebSocketCommonProtocol
from websockets.exceptions import ConnectionClosedError

from . import AsyncTunnel
from ubiquity.waves.shoebox import ShoeboxWave
from ubiquity.waves import Wave
from ubiquity.serialization.wave import serialize_wave


class WebSocketTunnel(AsyncTunnel, ABC):

    def __init__(self):
        super().__init__()

    async def _handle_connection(self, client: WebSocketCommonProtocol):
        try:
            if self._shoebox:
                # send the current shoebox
                wave = ShoeboxWave(self._shoebox)
                wave_pb = wave.serialize()
                wave_raw = wave_pb.SerializeToString()
                await client.send(wave_raw)
            # process incoming waves
            async for wave_raw in client:
                # nothing to do if this tunnel is not connected to a shoebox
                if self._shoebox is None:
                    self.logger.debug('Received a wave from {:s}.'.format(
                        str(client.remote_address)
                    ) + ' Dropped, tunnel not attached to any shoeboxes.')
                    continue
                # parse incoming data, and push it up the chain
                wave = self.wave_in(wave_raw)
                if isinstance(wave, Wave):
                    wave_pb = serialize_wave(wave)
                    wave_raw = wave_pb.SerializeToString()
                    await client.send(wave_raw)
        except ConnectionClosedError:
            pass


class WebSocketServerTunnel(WebSocketTunnel):

    def __init__(self, bind_host: str = 'localhost', bind_port: int = 5005):
        super().__init__()
        self._bind_host = bind_host
        self._bind_port = bind_port
        self._links = []
        server = websockets.serve(self.handler, self._bind_host, self._bind_port,
                                  loop=self.event_loop)
        asyncio.ensure_future(server, loop=self.event_loop)
        self.start()

    async def handler(self, client: WebSocketCommonProtocol, _: str):
        self._links.append(client)
        try:
            await self._handle_connection(client)
        finally:
            await client.close()
            self._links.remove(client)

    async def _send_wave(self, wave_raw: str):
        if self._links:
            await asyncio.wait([client.send(wave_raw) for client in self._links],
                               loop=self.event_loop)

    def __str__(self):
        return 'WS:{:s}:{:d}'.format(self._bind_host, self._bind_port)


class WebSocketClientTunnel(WebSocketTunnel):

    def __init__(self, server_host: str, server_port: int = 5005):
        super().__init__()
        self._server_host = server_host
        self._server_port = server_port
        self._socket = None
        self._uri = 'ws://{:s}:{:d}'.format(self._server_host, self._server_port)
        asyncio.run_coroutine_threadsafe(self._connect(), self.event_loop)
        self.start()

    async def _connect(self):
        while True:
            try:
                self._socket = await websockets.connect(self._uri)
                self.event_loop.create_task(self._run())
                break
            except ConnectionRefusedError:
                await asyncio.sleep(1.0, loop=self.event_loop)

    async def _run(self):
        await self._handle_connection(self._socket)
        await self._socket.close()

    async def _send_wave(self, wave_raw: str):
        if self._socket:
            await self._socket.send(wave_raw)

    def __str__(self):
        return 'WS:{:s}:{:d}'.format(self._server_host, self._server_port)
