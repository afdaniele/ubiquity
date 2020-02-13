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


def serialize_shoebox(sb: Shoebox) -> ShoeboxPB:
    shoebox_pb = ShoeboxPB()
    for quantum_id, quantum in sb.quanta.items():
        # do not serialize stubs
        if isinstance(quantum, QuantumStub):
            continue
        # create stub object
        _, stub = Quantum.from_object(quantum, quantum_id)
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
