import sys
import json
from ubiquity import ulogger
from ubiquity.exceptions import WaveParseError
from ubiquity.wave import Wave, ErrorResponseWave
from abc import abstractmethod


class Tunnel:

    def __init__(self):
        self._shoebox = None

    def attach(self, shoebox: 'Shoebox'):
        self._shoebox = shoebox
        ulogger.info('Attached tunnel {:s} to shoebox "{:s}"'.format(
            str(self), self._shoebox.name()
        ))

    def detach(self):
        if self._shoebox:
            ulogger.info('Detaching tunnel {:s} from shoebox "{:s}"'.format(
                str(self), self._shoebox.name()
            ))
        self._shoebox = None

    def wave_in(self, wave_raw: str):
        # parse incoming data
        try:
            wave = Wave.from_json(wave_raw)
            ulogger.debug('Tunnel[{:s}]: Received wave of type {:s}.'.format(
                str(self), wave.utype
            ))
        except (json.JSONDecodeError, WaveParseError):
            ex_type, ex_value, ex_traceback = sys.exc_info()
            ulogger.debug('Tunnel[{:s}]: Received invalid wave.'.format(str(self)))
            return ErrorResponseWave(None, None, ex_type, ex_value, ex_traceback)
        # we have a valid wave, apply and get result
        return wave.apply(self._shoebox)

    async def wave_out(self, wave: Wave):
        wave_raw = wave.serialize()
        await self._send_wave(wave_raw)

    @abstractmethod
    async def _send_wave(self, wave_raw: str):
        raise NotImplementedError('Method "_send_wave" not implemented in Tunnel class')
