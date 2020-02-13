import os
import uuid
import logging
from typing import Any, Union, Iterable, Tuple
from abc import abstractmethod

from inspect import \
    getmembers, \
    signature, \
    _empty, \
    _ParameterKind

from ubiquity.serialization.Quantum_pb2 import QuantumPB
from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB
from ubiquity.serialization.Wave_pb2 import WavePB
from ubiquity.serialization.Field_pb2 import FieldPB
from ubiquity.serialization.Method_pb2 import ParameterPB, ParameterTypePB, MethodPB

from threading import Semaphore

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

EXCLUDED_METHODS = [
    '__new__',
    '__repr__',
    '__str__',
    '__init__',
    '__getattribute__'
]

logging.basicConfig()
verbose_logging = 'UBIQUITY_VERBOSE' in os.environ and bool(os.environ['UBIQUITY_VERBOSE'])


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
        self._waves_in = {}
        self.__logger__ = logging.getLogger(str(self))
        self.__logger__.setLevel(logging.DEBUG if verbose_logging else logging.INFO)
        self._waves_in_lock = Semaphore(1)
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

    @property
    def logger(self):
        return self.__logger__

    @abstractmethod
    def register_quantum(self, obj: Any, quantum_id: QuantumID = None) -> QuantumID:
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
    def wave_in(self, wave: 'WaveIF'):
        raise NotImplementedError()

    @abstractmethod
    def wave_out(self, wave: 'WaveIF'):
        raise NotImplementedError()

    @abstractmethod
    def wait_on(self, request_wave: Union[str, 'WaveIF'], timeout: int = -1):
        raise NotImplementedError()

    @abstractmethod
    def serialize(self) -> ShoeboxPB:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(shoebox_pb: ShoeboxPB) -> 'ShoeboxIF':
        raise NotImplementedError()

    def __str__(self):
        return 'SB[{:s}]'.format(self.name)


class TunnelIF:

    def __init__(self):
        self._shoebox = None
        self._is_shutdown = False
        self.__logger__ = None

    @property
    def shoebox(self):
        return self._shoebox

    @property
    def is_shutdown(self):
        return self._is_shutdown

    @property
    def logger(self):
        if not self.__logger__:
            self.__logger__ = logging.getLogger('TN\\{:s}/'.format(str(self)))
            self.__logger__.setLevel(logging.DEBUG if verbose_logging else logging.INFO)
        return self.__logger__

    def shutdown(self):
        self._is_shutdown = True

    @abstractmethod
    def attach(self, shoebox: ShoeboxIF):
        raise NotImplementedError()

    @abstractmethod
    def detach(self):
        raise NotImplementedError()

    @abstractmethod
    def wave_in(self, wave_raw: str) -> Union['WaveIF', None]:
        raise NotImplementedError()

    @abstractmethod
    async def wave_out(self, wave: 'WaveIF'):
        raise NotImplementedError()

    @abstractmethod
    async def _send_wave(self, wave_raw: str):
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()


class WaveIF:

    def __init__(self, shoebox: Union[ShoeboxIF, None], quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None]):
        self._id = str(uuid.uuid4())
        self._shoebox = shoebox
        self._quantum_id = quantum_id
        self._request_wave = request_wave
        self.__logger__ = logging.getLogger(str(self))
        self.__logger__.setLevel(logging.DEBUG if verbose_logging else logging.INFO)

    @property
    def id(self) -> str:
        return self._id

    @property
    def shoebox(self) -> Union[ShoeboxIF, None]:
        return self._shoebox

    @property
    def quantum_id(self) -> Union[QuantumID, None]:
        return self._quantum_id

    @property
    def request_wave(self) -> Union[str, None]:
        return self._request_wave

    @property
    def logger(self):
        return self.__logger__

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

    def __str__(self):
        return 'WV{{{:s}}}'.format(self.id[:8])


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
        self.__logger__ = logging.getLogger(str(self))
        self.__logger__.setLevel(logging.DEBUG if verbose_logging else logging.INFO)

    @property
    def id(self) -> int:
        return self._id

    @property
    def fields(self) -> Iterable[Field]:
        return self._fields

    @property
    def methods(self) -> Iterable[Method]:
        return self._methods

    @property
    def logger(self):
        return self.__logger__

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

    def __str__(self):
        return 'QT+{:d}'.format(self.id)

    @staticmethod
    def from_object(obj: Any, quantum_id: QuantumID = None) -> Tuple[QuantumID, 'Quantum']:
        if quantum_id is None:
            quantum_id = id(obj)
        # create stub for the object
        stub = Quantum(quantum_id)
        # add fields to stub
        for field_name, field_value in getmembers(obj, lambda m: not callable(m)):
            field_type = type(field_value)
            field = Field(field_name, field_type)
            stub.add_field(field)
        # add methods to stub
        for method_name, method_callable in getmembers(obj, callable):
            if method_name in EXCLUDED_METHODS:
                continue
            try:
                method_signature = signature(method_callable)
            except ValueError:
                continue
            method_args = []
            for arg_name, arg_info in method_signature.parameters.items():
                arg_type = {
                    _ParameterKind.POSITIONAL_OR_KEYWORD: '__default__',
                    _ParameterKind.POSITIONAL_ONLY: '__positional__',
                    _ParameterKind.VAR_POSITIONAL: '__var_positional__',
                    _ParameterKind.KEYWORD_ONLY: '__keyword__',
                    _ParameterKind.VAR_KEYWORD: '__var_keyword__',
                }[arg_info.kind]
                arg_annotation = arg_info.annotation if arg_info.annotation != _empty else ''
                arg_default = arg_info.default if arg_info.default != _empty else None
                arg = Parameter(arg_name, arg_type, arg_annotation, arg_default)
                method_args.append(arg)
            method = Method(method_name, method_args)
            stub.add_method(method)
        # ---
        return quantum_id, stub
