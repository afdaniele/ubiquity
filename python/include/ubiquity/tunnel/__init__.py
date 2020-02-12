import sys
from abc import ABC

from ubiquity.logger import logger
from ubiquity.waves import Wave
from ubiquity.waves.error import ErrorWave
from ubiquity.types import TunnelIF, ShoeboxIF

from ubiquity.serialization.Wave_pb2 import WavePB, _WAVETYPEPB


class Tunnel(TunnelIF, ABC):

    def __init__(self):
        super().__init__()

    def attach(self, shoebox: ShoeboxIF):
        self._shoebox = shoebox
        logger.info('Attached tunnel {:s} to shoebox "{:s}"'.format(
            str(self), self._shoebox.name
        ))

    def detach(self):
        if self._shoebox:
            logger.info('Detaching tunnel {:s} from shoebox "{:s}"'.format(
                str(self), self._shoebox.name
            ))
        self._shoebox = None

    def wave_in(self, wave_raw: str):
        # parse incoming data
        try:
            wave_pb = WavePB()
            wave_pb.ParseFromString(wave_raw)
            wave = Wave.deserialize(wave_pb)
            logger.debug('Tunnel[{:s}]: Received wave of type {:s}.'.format(
                str(self), _WAVETYPEPB.values_by_number[wave_pb.header.type].name
            ))
        except:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            logger.debug('Tunnel[{:s}]: Received invalid wave.'.format(str(self)))
            return ErrorWave.from_exception(None, ex_type, ex_value, ex_traceback)
        # we have a valid wave, apply and get result
        return wave.hit(self._shoebox)

    async def wave_out(self, wave: Wave):
        wave_pb = wave.serialize()
        wave_raw = wave_pb.SerializeToString()
        await self._send_wave(wave_raw)
