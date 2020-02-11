from typing import Any, Union, Iterable, Dict
from abc import abstractmethod


QuantumID = int
FieldType = Any
ParameterType = Union[
    '__default__',
    '__positional__',
    '__keyword__',
    '__var_positional__',
    '__var_keyword__'
]
NOTSET = "__NOTSET__"


class ShoeboxContent:
    pass


class QuantumStub:
    pass


class ShoeboxIF:

    def __init__(self, name: str):
        self._name = name
        self._quanta = {}
        self._tunnels = []
        self._objects = {}
        self._content = ShoeboxContent()

    @property
    def name(self):
        return self._name

    @property
    def quanta(self):
        return self._quanta

    @property
    def objects(self):
        return self._objects

    @property
    def content(self):
        return self._content

    @abstractmethod
    def register_quantum(self, obj: Any) -> QuantumID:
        raise NotImplementedError()

    @abstractmethod
    def name_quantum(self, name: str, quantum_id: QuantumID):
        raise NotImplementedError()

    @abstractmethod
    def add(self, name: str, obj: Any):
        raise NotImplementedError()

    @abstractmethod
    def attach(self, tunnel: 'TunnelIF'):
        raise NotImplementedError()

    @abstractmethod
    def detach(self, tunnel: 'TunnelIF'):
        raise NotImplementedError()

    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(shoebox_raw: Union[str, Dict]) -> 'ShoeboxIF':
        raise NotImplementedError()


class TunnelIF:

    def __init__(self):
        self._shoebox = None
        self._is_shutdown = False

    @property
    def shoebox(self):
        return self._shoebox

    @property
    def is_shutdown(self):
        return self._is_shutdown

    def shutdown(self):
        self._is_shutdown = True

    @abstractmethod
    def attach(self, shoebox: ShoeboxIF):
        raise NotImplementedError()

    @abstractmethod
    def detach(self):
        raise NotImplementedError()

    @abstractmethod
    def wave_in(self, wave_raw: str):
        raise NotImplementedError()

    @abstractmethod
    async def wave_out(self, wave: 'WaveIF'):
        raise NotImplementedError()

    @abstractmethod
    async def _send_wave(self, wave_raw: str):
        raise NotImplementedError()


class WaveIF:
    _utype = None

    def __init__(self, shoebox: Union[ShoeboxIF, None]):
        self._shoebox = shoebox

    @property
    def utype(self) -> str:
        return self._utype

    @property
    def shoebox(self) -> ShoeboxIF:
        return self._shoebox

    @abstractmethod
    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, 'WaveIF']:
        raise NotImplementedError()

    @abstractmethod
    def _serialize(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(wave: dict) -> 'WaveIF':
        raise NotImplementedError()

    @abstractmethod
    def serialize(self) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def from_json(wave_raw: str) -> 'WaveIF':
        raise NotImplementedError()

    @staticmethod
    def _is_wave(wave: dict) -> bool:
        if '__ubiquity_object__' not in wave or \
                wave['__ubiquity_object__'] != 1 or \
                '__type__' not in wave:
            return False
        return True


class Field:
    _utype = '__field__'

    def __init__(self, name: str, ftype: FieldType):
        self._name = name
        self._type = ftype

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> FieldType:
        return self._type

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__data__': {
                '__name__': self._name,
                '__type__': str(self._type)
            }
        }


class Parameter:
    _utype = '__parameter__'

    def __init__(self, name: str, ptype: ParameterType, annotation: Any, default: Any):
        self._name = name
        self._type = ptype
        self._annotation = annotation
        self._default = default

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> ParameterType:
        return self._type

    @property
    def annotation(self) -> Any:
        return self._annotation

    @property
    def default(self) -> Any:
        return self._default

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__data__': {
                '__name__': self._name,
                '__type__': str(self._type),
                '__annotation__': str(self._annotation),
                '__default__': self._default
            }
        }


class Method:
    _utype = '__method__'

    def __init__(self, name: str, args: Iterable[Parameter]):
        self._name = name
        self._args = args

    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self) -> Iterable[Parameter]:
        return self._args

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__data__': {
                '__name__': self._name,
                '__args__': list(map(lambda a: a.serialize(), self._args))
            }
        }


class Quantum:
    _utype = '__stub__'

    def __init__(self, sid: int):
        self._id = sid
        self._fields = []
        self._methods = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def fields(self) -> Iterable[Field]:
        return self._fields

    @property
    def methods(self) -> Iterable[Method]:
        return self._methods

    def add_field(self, field: Field):
        self._fields.append(field)

    def add_method(self, method: Method):
        self._methods.append(method)

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__data__': {
                '__id__': self._id,
                '__fields__': list(map(lambda a: a.serialize(), self._fields)),
                '__methods__': list(map(lambda a: a.serialize(), self._methods))
            }
        }
