from typing import Any, Tuple, Union

from google.protobuf.any_pb2 import Any as AnyPB
from google.protobuf.message import Message as MessagePB

from ubiquity.types import Quantum, QuantumID, ShoeboxIF, QuantumStub
from ubiquity.serialization.WellKnown_pb2 import \
    IntPB, \
    FloatPB, \
    StringPB, \
    BoolPB, \
    IterablePB, \
    NonePB

from ubiquity.serialization.Quantum_pb2 import QuantumPB

PRIMITIVES = {
    int: lambda v: IntPB(int=True, value=v),
    float: lambda v: FloatPB(float=True, value=v),
    str: lambda v: StringPB(string=True, value=v),
    bool: lambda v: BoolPB(bool=True, value=v),
}


def serialize_any(value: Any, shoebox: ShoeboxIF, primitives_only: bool = False) -> Tuple[Union[QuantumID, None], MessagePB]:
    if isinstance(value, MessagePB):
        raise ValueError('ProtoBuf objects are confined to the tunnel level. '
                         'It should not have made this far up the pipeline. This is a bug.')
    if isinstance(value, Quantum):
        raise ValueError('Quantum objects cannot be re-serialized to form another Quantum. '
                         'This should not have happened. This is a bug.')
    if isinstance(value, QuantumStub):
        raise ValueError('QuantumStub objects are for local use only and cannot be re-serialized '
                         'back to a Quantum. This should not have happened. This is a bug.')
    # ---
    # TODO: recursively serialize dict
    if type(value) in PRIMITIVES:
        # built-in types
        return None, PRIMITIVES[type(value)](value)
    if not primitives_only and isinstance(value, (list, set, tuple)):
        # Iterables
        lst = IterablePB()
        for i, e in enumerate(value):
            a = AnyPB()
            a.Pack(serialize_any(e, shoebox)[1])
            lst.values.append(a)
        return None, lst
    if value is None:
        # None / null
        return None, NonePB(none=True)
    # Quantum object
    quantum_id, quantum = Quantum.from_object(value)
    quantum_pb = quantum.serialize()
    # add quantum to the shoebox
    shoebox.register_quantum(value, quantum_id)
    # ---
    return quantum_id, quantum_pb


def deserialize_any(msg: AnyPB) -> Any:
    if not isinstance(msg, AnyPB):
        raise ValueError('Only objects of type google.protobuf.any_pb2.AnyPB can be '
                         'deserialized. This should not have happened. This is a bug.')
    # ---
    # TODO: recursively deserialize dict
    types = [IntPB, FloatPB, StringPB, BoolPB]
    # built-in types
    for T in types:
        if msg.Is(T.DESCRIPTOR):
            data = T()
            msg.Unpack(data)
            return data.value
    # Iterable
    if msg.Is(IterablePB.DESCRIPTOR):
        data = IterablePB()
        msg.Unpack(data)
        return [deserialize_any(e) for e in data.values]
    # None / null
    if msg.Is(NonePB.DESCRIPTOR):
        return None
    # Quantum object
    if msg.Is(QuantumPB.DESCRIPTOR):
        data = QuantumPB()
        msg.Unpack(data)
        return Quantum.deserialize(data)
    # ---
    return None
