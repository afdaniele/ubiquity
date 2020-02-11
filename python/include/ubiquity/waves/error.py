from types import TracebackType
from typing import Union

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF, WaveIF


class ErrorResponseWave(Wave):
    _utype = '__error_response_wave__'

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 request_wave: Union[str, None],
                 etype: str,
                 emessage: str,
                 etrace: str):
        super().__init__(shoebox)
        self._request_wave = request_wave
        self._error_type = etype
        self._error_message = emessage
        self._error_trace = etrace

    @property
    def request_wave(self) -> Union[str, None]:
        return self._request_wave

    @property
    def error_type(self) -> str:
        return self._error_type

    @property
    def error_message(self) -> str:
        return self._error_message

    @property
    def error_trace(self) -> str:
        return self._error_trace

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, WaveIF]:
        return None

    def _serialize(self) -> dict:
        # TODO: self._error_trace needs extra serialization
        return {
            '__ubiquity_object__': 1,
            '__type__': '__method_return__',
            '__data__': {
                '__request_wave__': self._request_wave,
                '__type__': self._error_type,
                '__message__': self._error_message,
                '__trace__': self._error_trace
            }
        }

    @staticmethod
    def deserialize(wave: dict) -> 'ErrorResponseWave':
        if not ErrorResponseWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != ErrorResponseWave._utype:
                raise WaveParseError('The given object is not a valid ErrorResponseWave')
            return ErrorResponseWave(
                None, wave['__request_wave__'], wave['__type__'], wave['__message__'], wave['__trace__']
            )
        except KeyError:
            raise WaveParseError('The given object is not a valid ErrorResponseWave')

    @staticmethod
    def from_exception(request_wave: str, ex_type: BaseException,
                       ex_value: Exception, ex_traceback: TracebackType) -> 'ErrorResponseWave':
        # turn exception into an ErrorRespondeWave
        return ErrorResponseWave(None, request_wave, str(ex_type), str(ex_value), str(ex_traceback))
