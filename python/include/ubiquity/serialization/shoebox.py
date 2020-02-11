import json
from typing import Union, Dict
from collections import OrderedDict

from inspect import \
    getmembers, \
    signature, \
    _empty, \
    _ParameterKind

from ubiquity.types import \
    Field, \
    Parameter, \
    Method, \
    Quantum, \
    NOTSET

from ubiquity import Shoebox
from ubiquity.exceptions import JSONParseError
from ubiquity.stubs import QuantumStub, QuantumStubBuilder


def serialize_shoebox(sb: Shoebox) -> dict:
    _quanta = {}
    for quantum_id, quantum in sb.quanta.items():
        # do not serialize stubs
        if isinstance(quantum, QuantumStub):
            continue
        # create stub for the object
        stub = Quantum(quantum_id)
        # add fields to stub
        for field_name, field_value in getmembers(quantum, lambda m: not callable(m)):
            field_type = type(field_value)
            field = Field(field_name, field_type)
            stub.add_field(field)
        # add methods to stub
        for method_name, method_callable in getmembers(quantum, callable):
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
                arg_annotation = arg_info.annotation if arg_info.annotation != _empty else NOTSET
                arg_default = arg_info.default if arg_info.default != _empty else NOTSET
                arg = Parameter(arg_name, arg_type, arg_annotation, arg_default)
                method_args.append(arg)
            method = Method(method_name, method_args)
            stub.add_method(method)
        # add stub to shoebox
        _quanta[quantum_id] = stub
    # return serialized shoebox
    return {
        '__ubiquity_object__': 1,
        '__type__': '__shoebox__',
        '__data__': {
            '__name__': sb.name,
            '__quanta__': {
                i: o.serialize() for i, o in _quanta.items()
            },
            '__objects__': sb.objects
        }
    }


def deserialize_shoebox(shoebox_raw: Union[str, Dict]) -> Shoebox:
    if isinstance(shoebox_raw, str):
        shoebox_raw = json.loads(shoebox_raw, object_pairs_hook=OrderedDict)
    if '__ubiquity_object__' not in shoebox_raw or \
            shoebox_raw['__ubiquity_object__'] != 1 or \
            '__type__' not in shoebox_raw or \
            shoebox_raw['__type__'] != '__shoebox__':
        raise JSONParseError('The given JSON string does not contain a valid Shoebox description')
    # ---
    shoebox_raw = shoebox_raw['__data__']
    shoebox = Shoebox(shoebox_raw['__name__'])
    # parse quanta
    for quantum_id, quantum in shoebox_raw['__quanta__']:
        quantum = quantum['__data__']
        stub = QuantumStubBuilder(shoebox, quantum_id)
        # parse fields
        # TODO: validate quantum['__fields__']
        for field_name, field_data in quantum['__fields__']['__data__']:
            field = Field(field_name, field_data['__type__'])
            stub.add_field(field)
        # parse methods
        # TODO: validate quantum['__methods__']
        for method_name, method_data in quantum['__methods__']['__data__']:
            args = []
            _args = method_data['__args__']
            for arg_name, arg_data in _args:
                args.append(Parameter(
                    arg_name,
                    arg_data['__type__'],
                    arg_data['__annotation__'],
                    arg_data['__default__']
                ))
            method = Method(method_name, args)
            stub.add_method(method)
        # add stub to shoebox
        shoebox.register_quantum(stub.compile())
    # parse objects
    for object_name, object_id in shoebox_raw['__objects__']:
        shoebox.name_quantum(object_name, object_id)
    # return newly built shoebox
    return shoebox



