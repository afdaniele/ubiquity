import json
import uuid
from typing import Union
from abc import ABC
from collections import OrderedDict

from ubiquity.types import ShoeboxIF, WaveIF
from ubiquity.exceptions import WaveParseError


class Wave(WaveIF, ABC):

    def __init__(self, shoebox: Union[ShoeboxIF, None]):
        super().__init__(shoebox)

    def serialize(self) -> str:
        return json.dumps({
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__shoebox__': self._shoebox.name if self._shoebox else None,
            '__wave__': str(uuid.uuid4()),
            '__data__': self._serialize()
        })

    @staticmethod
    def from_json(wave_raw: str) -> 'Wave':
        from .shoebox import ShoeboxWave
        from .method import MethodCallRequestWave, MethodCallResponseWave
        from .field import FieldRequestWave, FieldResponseWave
        # ---
        wave = json.loads(wave_raw, object_pairs_hook=OrderedDict)
        if not Wave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        parser = {
            '__shoebox_wave__': ShoeboxWave.deserialize,
            '__field_request_wave__': FieldRequestWave.deserialize,
            '__field_response_wave__': FieldResponseWave.deserialize,
            '__method_call_request_wave__': MethodCallRequestWave.deserialize,
            '__method_call_response_wave__': MethodCallResponseWave.deserialize
        }
        try:
            return parser[wave['__type__']](wave)
        except KeyError:
            raise WaveParseError('Wave of type "{:s}" not supported'.format(wave['__type__']))
