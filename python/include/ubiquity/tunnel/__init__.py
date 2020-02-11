import sys
import json
from abc import ABC

from ubiquity.logger import logger
from ubiquity.exceptions import WaveParseError
from ubiquity.waves import Wave
from ubiquity.waves.error import ErrorResponseWave
from ubiquity.types import TunnelIF, ShoeboxIF


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
            wave = Wave.from_json(wave_raw)
            logger.debug('Tunnel[{:s}]: Received wave of type {:s}.'.format(
                str(self), wave.utype
            ))
        except (json.JSONDecodeError, WaveParseError):
            ex_type, ex_value, ex_traceback = sys.exc_info()
            logger.debug('Tunnel[{:s}]: Received invalid wave.'.format(str(self)))
            return ErrorResponseWave.from_exception(None, ex_type, ex_value, ex_traceback)
        # we have a valid wave, apply and get result
        return wave.hit(self._shoebox)

    async def wave_out(self, wave: Wave):
        wave_raw = wave.serialize()
        await self._send_wave(wave_raw)
