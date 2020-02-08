from typing import Any, Dict, Union
from inspect import \
    getmembers,\
    signature,\
    _empty,\
    _ParameterKind
from collections import OrderedDict
from enum import Enum

StubID = int
FieldType = Any
ParameterType = Union[
    '__default__',
    '__positional__',
    '__keyword__',
    '__var_positional__',
    '__var_keyword__'
]
ArgumentType = Any
NOTSET = "__NOTSET__"


class AccessMode(Enum):
    PUBLIC_ONLY = 1
    PERMISSIVE = 2


class ShoeboxContent:
    pass


class Shoebox:

    _utype = '__shoebox__'

    def __init__(self, name: str):
        self._name = name
        self._quanta = {}
        self._objects = {}
        self.content = ShoeboxContent()

    def name(self):
        return self._name

    def add(self, name: str, obj: Any, access: AccessMode = AccessMode.PUBLIC_ONLY) -> StubID:
        if not name.isidentifier():
            raise ValueError('The name "{:s}" is not a valid identifier for the object' % name)
        stub_id = id(obj)
        # create stub for the object
        stub = Stub(stub_id)
        # add fields to stub
        for field_name, field_value in getmembers(obj, lambda m: not callable(m)):
            if access == AccessMode.PUBLIC_ONLY and field_name.startswith('_'):
                continue
            field_type = type(field_value)
            field = Field(field_name, field_type)
            stub.add_field(field)
        # add methods to stub
        for method_name, method_callable in getmembers(obj, callable):
            if access == AccessMode.PUBLIC_ONLY and method_name.startswith('_'):
                continue
            try:
                method_signature = signature(method_callable)
            except ValueError:
                continue
            method_args = OrderedDict()
            for arg_name, arg_info in method_signature.parameters.items():
                arg_type = {
                    _ParameterKind.POSITIONAL_OR_KEYWORD: '__default__',
                    _ParameterKind.POSITIONAL_ONLY: '__positional__',
                    _ParameterKind.VAR_POSITIONAL: '__var_positional__',
                    _ParameterKind.KEYWORD_ONLY: '__keyword__',
                    _ParameterKind.VAR_KEYWORD: '__var_keyword__',
                }[arg_info.kind]
                arg_annotation = arg_info.annotation if arg_info.annotation != _empty else NOTSET
                arg_default = arg_info.default if arg_info.default != _empty else NOTSET
                arg = Parameter(arg_name, arg_type, arg_annotation, arg_default)
                method_args[arg_name] = arg
            method = Method(method_name, method_args)
            stub.add_method(method)
        # add object to stub
        self._quanta[stub_id] = stub
        self._objects[name] = stub_id
        setattr(self.content, name, stub)
        # return object ID
        return stub_id

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.name__': self._name,
            '__.quanta__': {
                id: o.serialize() for id, o in self._quanta.items()
            },
            '__.objects__': self._objects
        }


class Field:

    _utype = '__field__'

    def __init__(self, name: str, ftype: FieldType):
        self._name = name
        self._type = ftype

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> FieldType:
        return self._type

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.name__': self._name,
            '__.type__': str(self._type)
        }


class Parameter:

    _utype = '__parameter__'

    def __init__(self, name: str, ptype: ParameterType, annotation: Any, default: Any):
        self._name = name
        self._type = ptype
        self._annotation = annotation
        self._default = default

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> ParameterType:
        return self._type

    def get_annotation(self) -> Any:
        return self._annotation

    def get_default(self) -> Any:
        return self._default

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.name__': self._name,
            '__.type__': str(self._type),
            '__.annotation__': str(self._annotation),
            '__.default__': self._default
        }


class Method:

    _utype = '__method__'

    def __init__(self, name: str, args: Dict[str, Parameter]):
        self._name = name
        self._args = args

    def get_name(self) -> str:
        return self._name

    def get_args(self) -> Dict[str, Parameter]:
        return self._args

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.name__': self._name,
            '__.args__': OrderedDict([
                (k, v.serialize()) for k, v in self._args.items()
            ])
        }


class Stub:

    _utype = '__stub__'

    def __init__(self, sid: int):
        self._id = sid
        self._fields = {}
        self._methods = {}

    def get_id(self) -> int:
        return self._id

    def get_fields(self) -> Dict[str, Field]:
        return self._fields

    def get_methods(self) -> Dict[str, Method]:
        return self._methods

    def add_field(self, field: Field):
        self._fields[field.get_name()] = field

    def add_method(self, method: Method):
        self._methods[method.get_name()] = method

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.id__': self._id,
            '__.fields__': OrderedDict([
                (k, v.serialize()) for k, v in self._fields.items()
            ]),
            '__.methods__': OrderedDict([
                (k, v.serialize()) for k, v in self._methods.items()
            ])
        }



if __name__ == '__main__':
    import json
    from goprocam import GoProCamera
    from types import SimpleNamespace

    goproCamera = GoProCamera.GoPro()

    def fcn(a, b: str, c: int, *args, **kwargs) -> int:
        return 1

    a = SimpleNamespace(a=5, b=None, c={}, d={'asd': 74}, e=[], f=[1, 2], g=lambda d: [], h=fcn)

    sbox = Shoebox('general')

    sbox.add('sn', a)
    sbox.add('gopro', goproCamera)



    print(json.dumps(sbox.serialize(), indent=4, sort_keys=False))




# > Entanglement:
# The phenomenon in quantum theory whereby particles that interact with each other become
# permanently dependent on each other’s quantum states and properties, to the extent that
# they lose their individuality and in many ways behave as a single entity. At some level,
# entangled particles appear to “know” each other’s states and properties.


# > Nonlocality:
# The rather spooky ability of objects in quantum theory to apparently instantaneously
# know about each other’s quantum state, even when separated by large distances, in
# apparent contravention of the principle of locality (the idea that distant objects cannot
# have direct influence on one another, and that an object is influenced directly only by
# its immediate surroundings).


# > Superposition:
# The ability in quantum theory of an object, such as an atom or sub-atomic particle,
# to be in more than one quantum state at the same time. For example, an object could
# technically be in more than one place simultaneously as a consequence of the wave-like
# character of microscopic particles.

# > Wave-Particle Duality:
# The idea that light (and indeed all matter and energy) is both a wave and a particle,
# and that sometimes it behaves like a wave and sometimes it behaves like a particle.
# It is a central concept of quantum theory.
