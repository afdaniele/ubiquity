import json
import uuid
from typing import Union, Any
from abc import ABC
from collections import OrderedDict

from ubiquity.types import ShoeboxIF, WaveIF
from ubiquity.exceptions import WaveParseError
from ubiquity.serialization.Wave_pb2 import WavePB


class Wave(WaveIF, ABC):

    def __init__(self, shoebox: Union[ShoeboxIF, None], request_wave: Union[str, None]):
        super().__init__(shoebox, request_wave)

    def serialize(self) -> WavePB:
        from ubiquity.serialization.wave import serialize_wave
        return serialize_wave(self)

    def serialize_data(self) -> Any:
        return self._serialize()

        # return json.dumps({
        #     '__ubiquity_object__': 1,
        #     '__type__': self._utype,
        #     '__shoebox__': self._shoebox.name if self._shoebox else None,
        #     '__wave__': str(uuid.uuid4()),
        #     '__data__': self._serialize()
        # })

    @staticmethod
    def from_json(wave_raw: str) -> 'Wave':
        from .shoebox import ShoeboxWave
        from .method import MethodCallRequestWave, MethodCallResponseWave
        from .field import FieldRequestWave, FieldResponseWave
        from .error import ErrorWave
        # ---
        wave = json.loads(wave_raw, object_pairs_hook=OrderedDict)
        if not Wave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        parser = {
            '__shoebox_wave__': ShoeboxWave.deserialize,
            '__field_request_wave__': FieldRequestWave.deserialize,
            '__field_response_wave__': FieldResponseWave.deserialize,
            '__method_call_request_wave__': MethodCallRequestWave.deserialize,
            '__method_call_response_wave__': MethodCallResponseWave.deserialize,
            '__error_response_wave__': ErrorWave.deserialize
        }
        try:
            return parser[wave['__type__']](wave)
        except KeyError:
            raise WaveParseError('Wave of type "{:s}" not supported'.format(wave['__type__']))
