from typing import Any, Dict
from inspect import getmembers, signature, _empty
from collections import OrderedDict
from enum import Enum

StubID = int
FieldType = Any
ParameterType = Any
ArgumentType = Any
NOTSET = "__NOTSET__"


class AccessMode(Enum):
    PUBLIC_ONLY = 1
    PERMISSIVE = 2


class Shoebox:

    _utype = '__shoebox__'

    def __init__(self, id: str):
        self._id = id
        self._objects = {}

    def id(self):
        return self._id

    def add(self, obj: Any, access: AccessMode = AccessMode.PUBLIC_ONLY) -> StubID:
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
                arg_type = arg_info.annotation if arg_info.annotation != _empty else NOTSET
                arg_default = arg_info.default if arg_info.default != _empty else NOTSET
                arg = Parameter(arg_name, arg_type, arg_default)
                method_args[arg_name] = arg
            method = Method(method_name, method_args)
            stub.add_method(method)
        # add object to stub
        self._objects[stub_id] = stub
        # return object ID
        return stub_id

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.id__': self._id,
            '__.objects__': {
                id: o.serialize() for id, o in self._objects.items()
            }
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

    def __init__(self, name: str, ptype: ParameterType, default: Any):
        self._name = name
        self._type = ptype
        self._default = default

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> ParameterType:
        return self._type

    def get_default(self) -> Any:
        return self._default

    def serialize(self):
        return {
            '__ubiquity_object__': 1,
            '__type__': self._utype,
            '__.name__': self._name,
            '__.type__': str(self._type),
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
            '__.args__': {
                k: v.serialize() for k, v in self._args.items()
            }
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
            '__.fields__': {
                k: v.serialize() for k, v in self._fields.items()
            },
            '__.methods__': {
                k: v.serialize() for k, v in self._methods.items()
            }
        }



if __name__ == '__main__':
    import json
    from types import SimpleNamespace

    def fcn(a, b: str, c: int, *args, **kwargs) -> int:
        return 1

    a = SimpleNamespace(a=5, b=None, c={}, d={'asd': 74}, e=[], f=[1, 2], g=lambda d: [], h=fcn)

    sbox = Shoebox('general')

    sbox.add(a)



    print(json.dumps(sbox.serialize(), indent=4, sort_keys=True))
