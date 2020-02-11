from typing import Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.logger import get_logger


logger = get_logger()


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
            '__data__': {
                '__object__': self._object_id,
                '__field_name__': self._field_name
            }
        }

    @staticmethod
    def deserialize(wave: dict) -> 'FieldRequestWave':
        if not FieldRequestWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != FieldRequestWave._utype:
                raise WaveParseError('The given object is not a valid FieldRequestWave')
            return FieldRequestWave(None, wave['__object__'], wave['__field_name__'])
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
            '__data__': {
                '__request_wave__': self._request_wave,
                '__data__': self._field_value
            }
        }

    @staticmethod
    def deserialize(wave: dict) -> 'FieldResponseWave':
        if not FieldResponseWave._is_wave(wave):
            raise WaveParseError('The given object is not a __ubiquity_object__')
        # parse wave
        try:
            if wave['__type__'] != FieldResponseWave._utype:
                raise WaveParseError('The given object is not a valid FieldResponseWave')
            return FieldResponseWave(None, wave['__request_wave__'], wave['__data__'])
        except KeyError:
            raise WaveParseError('The given object is not a valid FieldResponseWave')
