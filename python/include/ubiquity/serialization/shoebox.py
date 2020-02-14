from ubiquity.types import \
    Quantum, \
    ShoeboxIF

from ubiquity import Shoebox
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
    for quantum_pb in shoebox_pb.quanta:
        quantum = Quantum.deserialize(quantum_pb)
        # add stub to shoebox
        shoebox.register_quantum(quantum, quantum.id)
    # parse objects
    for object_name, object_id in shoebox_pb.objects.items():
        shoebox.name_quantum(object_name, object_id)
    # return newly built shoebox
    return shoebox
