require('Ubiquity_pb')

PRIMITIVES = {
    number: (v) -> proto.IntPB().setInt(true).setValue(v),
    String: (v) -> proto.StringPB().setString(true).setValue(v),
    boolean: (v) -> proto.BoolPB().setBool(true).setValue(v)
}


serialize_any = (value ###: Any ###, shoebox ###: ShoeboxIF ###, primitives_only ###: bool ###) ###: Tuple[Union[QuantumID, null], MessagePB] ### ->
    if value instanceof proto.MessagePB
        throw 'ProtoBuf objects are confined to the tunnel level.
It should not have made this far up the pipeline.
This is a bug.'
    if value instanceof Quantum
        throw 'Quantum objects cannot be re-serialized to form another Quantum.
This should not have happened.
This is a bug.'
    if value instanceof QuantumStub
        throw 'QuantumStub objects are for local use only and cannot be
re-serialized back to a Quantum. This should not have happened.
This is a bug.'
    # ---
    # TODO: implement this
    return null


deserialize_any = (msg ###: AnyPB ###) ###: Any ### ->
    if msg not instanceof proto.AnyPB
        throw 'Only objects of type google.protobuf.any_pb2.AnyPB can be deserialized.
This should not have happened.
This is a bug.'
    # ---
    # TODO: recursively deserialize dict
    # TODO: implement this
    return null
