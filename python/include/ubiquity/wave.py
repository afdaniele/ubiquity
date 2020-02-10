import json
import uuid
from types import TracebackType
from typing import Dict, Union, Any
from abc import abstractmethod
from .exceptions import WaveParseError
from .shoebox import Shoebox
import logging

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
            '__.data__': self._serialize()
        })

    @staticmethod
    def _is_wave(wave: dict) -> bool:
        if '__ubiquity_object__' not in wave or \
                wave['__ubiquity_object__'] != 1 or \
                '__type__' not in wave:
            return False
        return True

    @staticmethod
    def from_json(wave_raw: str) -> 'Wave':
        wave = json.loads(wave_raw)
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
        return ShoeboxWave(Shoebox.from_json(
            json.dumps(wave['__.data__'])
        ))


class FieldRequestWave(Wave):
    _utype = '__field_request_wave__'

    def __init__(self, shoebox: Union['Shoebox', None], object_id: int, field_name: str):
        super().__init__(shoebox)
        self._object_id = object_id
        self._field_name = field_name

    @property
    def object_id(self) -> int:
        return self._object_id

    @property
    def field_name(self) -> str:
        return self._field_name

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        pass

    def _serialize(self) -> dict:
        return {
            '__ubiquity_object__': 1,
            '__type__': '__field_access__',
            '__.object__': self._object_id,
            '__.field_name__': self._field_name
        }

    @staticmethod
    def deserialize(wave: dict) -> 'FieldRequestWave':
        if not FieldRequestWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != FieldRequestWave._utype:
                raise WaveParseError('The given object is not a valid FieldRequestWave')
            return FieldRequestWave(None, wave['__.object__'], wave['__.field_name__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid FieldRequestWave')


class FieldResponseWave(Wave):
    _utype = '__field_response_wave__'

    def __init__(self, shoebox: Union['Shoebox', None], request_wave: str, field_value: Any):
        super().__init__(shoebox)
        self._request_wave = request_wave
        self._field_value = field_value

    @property
    def request_wave(self) -> str:
        return self._request_wave

    @property
    def field_value(self) -> Any:
        return self._field_value

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        pass

    def _serialize(self) -> dict:
        # TODO: self._field_value needs extra serialization (it might contain objects to reference)
        return {
            '__ubiquity_object__': 1,
            '__type__': '__field_value__',
            '__.request_wave__': self._request_wave,
            '__.data__': self._field_value
        }

    @staticmethod
    def deserialize(wave: dict) -> 'FieldResponseWave':
        if not FieldResponseWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != FieldResponseWave._utype:
                raise WaveParseError('The given object is not a valid FieldResponseWave')
            return FieldResponseWave(None, wave['__.request_wave__'], wave['__.data__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid FieldResponseWave')


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
            '__.object__': self._object_id,
            '__.method_name__': self._method_name,
            '__.args__': self._args
        }

    @staticmethod
    def deserialize(wave: dict) -> 'MethodCallRequestWave':
        if not MethodCallRequestWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != MethodCallRequestWave._utype:
                raise WaveParseError('The given object is not a valid MethodCallRequestWave')
            return MethodCallRequestWave(None, wave['__.object__'], wave['__.method_name__'], wave['__.args__'])
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
            '__.request_wave__': self._request_wave,
            '__.data__': self._return_value
        }

    @staticmethod
    def deserialize(wave: dict) -> 'MethodCallResponseWave':
        if not MethodCallResponseWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != MethodCallResponseWave._utype:
                raise WaveParseError('The given object is not a valid MethodCallResponseWave')
            return MethodCallResponseWave(None, wave['__.request_wave__'], wave['__.data__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid MethodCallResponseWave')


class ErrorResponseWave(Wave):

    _utype = '__error_response_wave__'

    def __init__(self, shoebox: Union['Shoebox', None], request_wave: Union[str, None], etype: str, emessage: str, etrace: str):
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

    def apply(self, shoebox: Union[None, 'Shoebox']) -> Union[None, 'Wave']:
        return None

    def _serialize(self) -> dict:
        # TODO: self._error_trace needs extra serialization
        return {
            '__ubiquity_object__': 1,
            '__type__': '__method_return__',
            '__.request_wave__': self._request_wave,
            '__.type__': self._error_type,
            '__.message__': self._error_message,
            '__.trace__': self._error_trace
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
                None, wave['__.request_wave__'], wave['__.type__'], wave['__.message__'], wave['__.trace__']
            )
        except KeyError:
            raise WaveParseError('The given object is not a valid ErrorResponseWave')

    @staticmethod
    def from_exception(request_wave: str, ex_type: BaseException,
                       ex_value: Exception, ex_traceback: TracebackType) -> 'ErrorResponseWave':
        # turn exception into an ErrorRespondeWave
        return ErrorResponseWave(None, request_wave, str(ex_type), str(ex_value), str(ex_traceback))
