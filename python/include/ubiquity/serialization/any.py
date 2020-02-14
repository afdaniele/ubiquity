from typing import Any, Tuple, Union

from google.protobuf.any_pb2 import Any as AnyPB

from ubiquity.types import Quantum, QuantumID, ShoeboxIF
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


def serialize_any(value: Any, shoebox: ShoeboxIF, primitives_only: bool = False) -> Tuple[Union[QuantumID, None], Any]:
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
    quantum = quantum.serialize()
    # add quantum to the shoebox
    shoebox.register_quantum(quantum, quantum_id)
    # ---
    return quantum_id, quantum


def deserialize_any(msg: AnyPB) -> Any:
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
