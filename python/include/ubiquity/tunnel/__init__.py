import sys
import json
from abc import abstractmethod

from ubiquity.logger import get_logger
from ubiquity.exceptions import WaveParseError
from ubiquity.waves import Wave
from ubiquity.waves.error import ErrorResponseWave


logger = get_logger()


class Tunnel:

    def __init__(self):
        self._shoebox = None
        self._is_shutdown = False

    @property
    def is_shutdown(self):
        return self._is_shutdown

    def shutdown(self):
        self._is_shutdown = True

    def attach(self, shoebox: 'Shoebox'):
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
        pass
    #     # parse incoming data
    #     try:
    #         wave = Wave.from_json(wave_raw)
    #         logger.debug('Tunnel[{:s}]: Received wave of type {:s}.'.format(
    #             str(self), wave.utype
    #         ))
    #     except (json.JSONDecodeError, WaveParseError):
    #         ex_type, ex_value, ex_traceback = sys.exc_info()
    #         logger.debug('Tunnel[{:s}]: Received invalid wave.'.format(str(self)))
    #         return ErrorResponseWave(None, None, ex_type, ex_value, ex_traceback)
    #     # we have a valid wave, apply and get result
    #     return wave.apply(self._shoebox)

    async def wave_out(self, wave: Wave):
        wave_raw = wave.serialize()
        await self._send_wave(wave_raw)

    @abstractmethod
    async def _send_wave(self, wave_raw: str):
        raise NotImplementedError('Method "_send_wave" not implemented in Tunnel class')
