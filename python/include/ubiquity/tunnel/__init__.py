import asyncio
import traceback
import threading
from abc import ABC, abstractmethod
from typing import Union

from ubiquity.waves import Wave
from ubiquity.waves.error import ErrorWave
from ubiquity.types import TunnelIF, ShoeboxIF

from ubiquity.serialization.Wave_pb2 import WavePB
from google.protobuf.text_format import MessageToString

DEBUG_MESSAGES = False


class Tunnel(TunnelIF, ABC):

    def __init__(self):
        super().__init__()

    def attach(self, shoebox: ShoeboxIF):
        self._shoebox = shoebox
        self.logger.info('Attached to shoebox "{:s}"'.format(self._shoebox.name))

    def detach(self):
        if self._shoebox:
            self.logger.info('Detaching from shoebox "{:s}"'.format(self._shoebox.name))
        self._shoebox = None

    def wave_in(self, wave_raw: str) -> Union[ErrorWave, None]:
        # parse incoming data
        try:
            wave_pb = WavePB()
            wave_pb.ParseFromString(wave_raw)
            wave = Wave.deserialize(wave_pb)
            self.logger.debug('Received {:s}.'.format(str(wave)))
            if DEBUG_MESSAGES:
                print(MessageToString(wave_pb))
            # we have a valid wave, push it to the shoebox
            return self._shoebox.wave_in(wave)
        except Exception:
            self.logger.error(traceback.format_exc())
            self.logger.debug('Received invalid wave.')

    def wave_out(self, wave: Wave):
        wave_pb = wave.serialize()
        wave_raw = wave_pb.SerializeToString()
        self.logger.debug('Sending out {:s}.'.format(str(wave)))
        if DEBUG_MESSAGES:
            print(MessageToString(wave_pb))
        self._send_wave(wave_raw)


class AsyncTunnel(Tunnel, ABC):

    def __init__(self):
        super().__init__()
        self._event_loop = asyncio.new_event_loop()
        self._event_loop_thread = threading.Thread(target=self._event_loop.run_forever)

    @property
    def event_loop(self):
        return self._event_loop

    def start(self):
        self._event_loop_thread.start()

    def shutdown(self):
        for task in asyncio.Task.all_tasks(loop=self.event_loop):
            task.cancel()
        # self._event_loop.stop()
        super().shutdown()

    async def wave_out(self, wave: Wave):
        wave_pb = wave.serialize()
        wave_raw = wave_pb.SerializeToString()
        self.logger.debug('Sending out {:s}.'.format(str(wave)))
        if DEBUG_MESSAGES:
            print(MessageToString(wave_pb))
        await self._send_wave(wave_raw)

    @abstractmethod
    async def _send_wave(self, wave_raw: str):
        raise NotImplementedError()
