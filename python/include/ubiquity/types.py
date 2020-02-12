from typing import Any, Union, Iterable
from abc import abstractmethod

from ubiquity.serialization.Shoebox_pb2 import QuantumPB
from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB
from ubiquity.serialization.Wave_pb2 import WavePB
from ubiquity.serialization.Field_pb2 import FieldPB
from ubiquity.serialization.Method_pb2 import ParameterPB, ParameterTypePB, MethodPB


QuantumID = int
FieldType = Any
ParameterType = Union[
    '__default__',
    '__positional__',
    '__keyword__',
    '__var_positional__',
    '__var_keyword__'
]

param_type_map = {
    '__default__': ParameterTypePB.DEFAULT,
    '__positional__': ParameterTypePB.POSITIONAL,
    '__keyword__': ParameterTypePB.KEYWORD,
    '__var_positional__': ParameterTypePB.VAR_POSITIONAL,
    '__var_keyword__': ParameterTypePB.VAR_KEYWORD
}


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
    def merge(self, shoebox: 'ShoeboxIF'):
        raise NotImplementedError()

    @abstractmethod
    def serialize(self) -> ShoeboxPB:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(shoebox_pb: ShoeboxPB) -> 'ShoeboxIF':
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

    def __init__(self, shoebox: Union[ShoeboxIF, None], request_wave: Union[str, None]):
        self._shoebox = shoebox
        self._request_wave = request_wave

    @property
    def shoebox(self) -> ShoeboxIF:
        return self._shoebox

    @property
    def request_wave(self) -> Union[str, None]:
        return self._request_wave

    @abstractmethod
    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, 'WaveIF']:
        raise NotImplementedError()

    @abstractmethod
    def _serialize(self) -> Any:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(wave_pb: Any) -> 'WaveIF':
        raise NotImplementedError()

    @abstractmethod
    def serialize(self) -> WavePB:
        raise NotImplementedError()

    @abstractmethod
    def serialize_data(self) -> Any:
        raise NotImplementedError()


class Field:

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
        return FieldPB(
            name=self.name,
            type=str(self.type)
        )


class Parameter:

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
        return ParameterPB(
            name=self.name,
            type=param_type_map[self.type],
            annotation=str(self.annotation),
            default_value=self.default
        )


class Method:

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
        return MethodPB(
            name=self.name,
            args=[p.serialize() for p in self.args]
        )


class Quantum:

    def __init__(self, quantum_id: int):
        self._id = quantum_id
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
        return QuantumPB(
            id=self.id,
            fields=[f.serialize() for f in self.fields],
            methods=[m.serialize() for m in self.methods]
        )
