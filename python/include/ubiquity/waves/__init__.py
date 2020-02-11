import json
import uuid
import logging
from typing import Dict, Union, Any
from abc import abstractmethod


MethodArguments = Dict[str, Any]

logging.basicConfig()
logger = logging.getLogger('wave')
logger.setLevel(logging.DEBUG)


class Wave:
    _utype = None

    def __init__(self, shoebox: Union['Shoebox', None]):
        self._shoebox = shoebox

    @property
    def utype(self) -> str:
        return self._utype

    @property
    def shoebox(self) -> 'Shoebox':
        return self._shoebox

    @abstractmethod
    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        raise NotImplementedError('This is an absrtact method in the Wave class')

    @abstractmethod
    def _serialize(self) -> dict:
        raise NotImplementedError('This is an absrtact method in the Wave class')

    @staticmethod
    @abstractmethod
    def deserialize(wave: dict) -> 'Wave':
        raise NotImplementedError('This is an absrtact method in the Wave class')

    def serialize(self) -> str:
        return json.dumps({
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__shoebox__': self._shoebox.name() if self._shoebox else None,
            '__wave__': str(uuid.uuid4()),
            '__data__': self._serialize()
        })

    @staticmethod
    def _is_wave(wave: dict) -> bool:
        if '__ubiquity_object__' not in wave or \
                wave['__ubiquity_object__'] != 1 or \
                '__type__' not in wave:
            return False
        return True

    # @staticmethod
    # def from_json(wave_raw: str) -> 'Wave':
    #     wave = json.loads(wave_raw, object_pairs_hook=OrderedDict)
    #     if not Wave._is_wave(wave):
    #         raise WaveParseError('The given object is not a __ubiquity_object__')
    #     parser = {
    #         '__shoebox_wave__': ShoeboxWave.deserialize,
    #         '__field_request_wave__': FieldRequestWave.deserialize,
    #         '__field_response_wave__': FieldResponseWave.deserialize,
    #         '__method_call_request_wave__': MethodCallRequestWave.deserialize,
    #         '__method_call_response_wave__': MethodCallResponseWave.deserialize
    #     }
    #     try:
    #         return parser[wave['__type__']](wave)
    #     except KeyError:
    #         raise WaveParseError('Wave of type "{:s}" not supported'.format(wave['__type__']))
