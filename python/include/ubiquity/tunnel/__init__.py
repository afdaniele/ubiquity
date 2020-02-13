import sys
from abc import ABC
from typing import Union

from ubiquity.waves import Wave
from ubiquity.waves.error import ErrorWave
from ubiquity.types import TunnelIF, ShoeboxIF

from ubiquity.serialization.Wave_pb2 import WavePB, _WAVETYPEPB


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
        # noinspection PyPep8
        try:
            wave_pb = WavePB()
            wave_pb.ParseFromString(wave_raw)
            wave = Wave.deserialize(wave_pb)
            self.logger.debug('Received {:s} of type {:s}.'.format(
                str(wave),
                _WAVETYPEPB.values_by_number[wave_pb.header.type].name
            ))
        except:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.logger.error(ex_type)
            self.logger.debug('Received invalid wave.')
            return ErrorWave.from_exception(None, ex_type, ex_value, ex_traceback)
        # we have a valid wave, push it to the shoebox
        self._shoebox.wave_in(wave)

    async def wave_out(self, wave: Wave):
        wave_pb = wave.serialize()
        wave_raw = wave_pb.SerializeToString()
        self.logger.debug('Sending out {:s} of type {:s}.'.format(
            str(wave),
            _WAVETYPEPB.values_by_number[wave_pb.header.type].name
        ))

        from google.protobuf.text_format import MessageToString
        print(MessageToString(wave_pb))

        await self._send_wave(wave_raw)
