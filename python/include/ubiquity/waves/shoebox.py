import json
from typing import Dict, Union, Any

from . import Wave
from ubiquity.shoebox import Shoebox
from ubiquity.exceptions import WaveParseError
from ubiquity.logger import get_logger


MethodArguments = Dict[str, Any]

logger = get_logger()


class ShoeboxWave(Wave):
    _utype = '__shoebox_wave__'

    def __init__(self, shoebox: 'Shoebox'):
        super().__init__(shoebox)

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        pass

    def _serialize(self) -> dict:
        return self._shoebox.serialize()

    @staticmethod
    def deserialize(wave: dict) -> 'ShoeboxWave':
        if not ShoeboxWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # TODO: here we need to turn wave into a ShoeboxWave containing a new Shoebox object
        return ShoeboxWave(Shoebox.deserialize(
            json.dumps(wave['__data__'])
        ))
