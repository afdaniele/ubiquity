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
    ShoeboxIF

from ubiquity import Shoebox
from ubiquity.stubs import QuantumStubBuilder
from ubiquity.types import QuantumStub

from .Shoebox_pb2 import ShoeboxPB

EXCLUDED_METHODS = [
    '__new__',
    '__repr__',
    '__str__',
    '__init__',
    '__getattribute__'
]


def serialize_shoebox(sb: Shoebox) -> ShoeboxPB:
    shoebox_pb = ShoeboxPB()
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
        # add stub to shoebox
        shoebox_pb.quanta.append(stub.serialize())
    # serialize objects
    for object_name, object_id in sb.objects.items():
        shoebox_pb.objects[object_name] = object_id
    # return serialized shoebox
    return shoebox_pb


def deserialize_shoebox(shoebox_pb: ShoeboxPB) -> ShoeboxIF:
    shoebox = Shoebox(shoebox_pb.name)
    # parse quanta
    for quantum in shoebox_pb.quanta:
        quantum_id = quantum.id
        stub = QuantumStubBuilder(quantum_id)
        # parse fields
        for field in quantum.fields:
            stub.add_field(Field(field.name, field.type))
        # parse methods
        for method in quantum.methods:
            args = []
            for arg in method.args:
                args.append(Parameter(
                    arg.name,
                    arg.type,
                    arg.annotation,
                    arg.default_value
                ))
            method = Method(method.name, args)
            stub.add_method(method)
        # add stub to shoebox
        shoebox.register_quantum(stub, quantum_id)
    # parse objects
    for object_name, object_id in shoebox_pb.objects.items():
        shoebox.name_quantum(object_name, object_id)
    # return newly built shoebox
    return shoebox
