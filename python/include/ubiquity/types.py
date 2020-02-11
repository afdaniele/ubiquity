from typing import Any, Union, Iterable


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
