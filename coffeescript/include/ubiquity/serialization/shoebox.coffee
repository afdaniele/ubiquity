require('./Ubiquity_pb')


serialize_shoebox = (sb ###: Shoebox ###) ###: ShoeboxPB ### ->
  shoebox_pb = proto.ShoeboxPB()
  for [quantum_id, quantum] in Object.entries(sb.quanta)
# do not serialize stubs
    if quantum instanceof QuantumStub
      continue
    # create stub object
    [_, stub] = Quantum.from_object(quantum, quantum_id)
    # add stub to shoebox
    shoebox_pb.addQuanta(stub.serialize())
  # serialize objects
  for [object_name, object_id] in Object.entries(sb)
    shoebox_pb.getObjectsMap().set(object_name, object_id)
  # return serialized shoebox
  return shoebox_pb


deserialize_shoebox = (shoebox_pb ###: ShoeboxPB ###) ###: ShoeboxIF ### ->
  shoebox = Shoebox(shoebox_pb.getName())
  # parse quanta
  for quantum_pb in shoebox_pb.getQuantaList()
    quantum = Quantum.deserialize(quantum_pb)
    # add stub to shoebox
    shoebox.register_quantum(quantum, quantum.id)
  # parse objects
  for [object_name, object_id] in shoebox_pb.getObjectsMap().entries()
    shoebox.name_quantum(object_name, object_id)
  # return newly built shoebox
  return shoebox

