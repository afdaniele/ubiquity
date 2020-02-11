import json
from typing import Dict, Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF


MethodArguments = Dict[str, Any]


class ShoeboxWave(Wave):
    _utype = '__shoebox_wave__'

    def __init__(self, shoebox: ShoeboxIF):
        super().__init__(shoebox)

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        pass

    def _serialize(self) -> dict:
        return self._shoebox.serialize()

    @staticmethod
    def deserialize(wave: dict) -> 'ShoeboxWave':
        from ubiquity.shoebox import Shoebox
        if not ShoeboxWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # TODO: here we need to turn wave into a ShoeboxWave containing a new Shoebox object
        return ShoeboxWave(Shoebox.deserialize(
            json.dumps(wave['__data__'])
        ))
