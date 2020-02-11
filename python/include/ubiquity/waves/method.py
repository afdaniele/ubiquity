from typing import Dict, Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.logger import get_logger


MethodArguments = Dict[str, Any]

logger = get_logger()


class MethodCallRequestWave(Wave):
    _utype = '__method_call_request_wave__'

    def __init__(self, shoebox: Union['Shoebox', None], object_id: int, method_name: str, args: MethodArguments):
        super().__init__(shoebox)
        self._object_id = object_id
        self._method_name = method_name
        self._args = args

    @property
    def object_id(self) -> int:
        return self._object_id

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def args(self) -> MethodArguments:
        return self._args

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        pass

    def _serialize(self) -> dict:
        # TODO: self._args needs extra serialization (it might contain referenced objects)
        return {
            '__ubiquity_object__': 1,
            '__type__': '__method_call__',
            '__data__': {
                '__object__': self._object_id,
                '__method_name__': self._method_name,
                '__args__': self._args
            }
        }

    @staticmethod
    def deserialize(wave: dict) -> 'MethodCallRequestWave':
        if not MethodCallRequestWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != MethodCallRequestWave._utype:
                raise WaveParseError('The given object is not a valid MethodCallRequestWave')
            return MethodCallRequestWave(None, wave['__object__'], wave['__method_name__'], wave['__args__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid MethodCallRequestWave')


class MethodCallResponseWave(Wave):

    _utype = '__method_call_response_wave__'

    def __init__(self, shoebox: Union['Shoebox', None], request_wave: str, return_value: Any):
        super().__init__(shoebox)
        self._request_wave = request_wave
        self._return_value = return_value

    @property
    def request_wave(self) -> str:
        return self._request_wave

    @property
    def return_value(self) -> Any:
        return self._return_value

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        pass

    def _serialize(self) -> dict:
        # TODO: self._return_value needs extra serialization (it might contain objects to reference)
        return {
            '__ubiquity_object__': 1,
            '__type__': '__method_return__',
            '__data__': {
                '__request_wave__': self._request_wave,
                '__data__': self._return_value
            }
        }

    @staticmethod
    def deserialize(wave: dict) -> 'MethodCallResponseWave':
        if not MethodCallResponseWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != MethodCallResponseWave._utype:
                raise WaveParseError('The given object is not a valid MethodCallResponseWave')
            return MethodCallResponseWave(None, wave['__request_wave__'], wave['__data__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid MethodCallResponseWave')
