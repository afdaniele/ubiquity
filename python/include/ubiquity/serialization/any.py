from typing import Any, Tuple, Union

from google.protobuf.any_pb2 import Any as AnyPB

from ubiquity.types import Quantum, QuantumID
from ubiquity.serialization.WellKnown_pb2 import Int, Float, String, Bool
from ubiquity.serialization.Quantum_pb2 import QuantumPB

WELL_KNOWN_TYPE_MAP = {
    int: Int,
    float: Float,
    str: String,
    bool: Bool
}


def serialize_any(value: Any) -> Tuple[Union[QuantumID, None], Any]:
    if type(value) in WELL_KNOWN_TYPE_MAP:
        # built-in types
        quantum_id, quantum = None, WELL_KNOWN_TYPE_MAP[type(value)](value=value)
    else:
        # Quantum object
        quantum_id, quantum = Quantum.from_object(value)
        quantum = quantum.serialize()
    # ---
    # TODO: serialize NULL
    # TODO: recursively serialize dict, list, and tuples
    return quantum_id, quantum


def deserialize_any(msg: AnyPB) -> Any:
    types = [Int, Float, String, Bool]
    # built-in types
    for T in types:
        if msg.Is(T.DESCRIPTOR):
            data = T()
            msg.Unpack(data)
            return data.value
    # Quantum object
    if msg.Is(QuantumPB.DESCRIPTOR):
        data = QuantumPB()
        msg.Unpack(data)
        return Quantum.deserialize(data)
    # ---
    return None
