// Generated by CoffeeScript 2.5.1
(function() {
  var deserialize_shoebox, serialize_shoebox;

  require('./Ubiquity_pb');

  serialize_shoebox = function(sb/*: Shoebox */)/*: ShoeboxPB */ {
    var _, i, j, len, len1, object_id, object_name, quantum, quantum_id, ref, ref1, shoebox_pb, stub;
    shoebox_pb = proto.ShoeboxPB();
    ref = Object.entries(sb.quanta);
    for (i = 0, len = ref.length; i < len; i++) {
      [quantum_id, quantum] = ref[i];
      // do not serialize stubs
      if (quantum instanceof QuantumStub) {
        continue;
      }
      // create stub object
      [_, stub] = Quantum.from_object(quantum, quantum_id);
      // add stub to shoebox
      shoebox_pb.addQuanta(stub.serialize());
    }
    ref1 = Object.entries(sb);
    // serialize objects
    for (j = 0, len1 = ref1.length; j < len1; j++) {
      [object_name, object_id] = ref1[j];
      shoebox_pb.getObjectsMap().set(object_name, object_id);
    }
    // return serialized shoebox
    return shoebox_pb;
  };

  deserialize_shoebox = function(shoebox_pb/*: ShoeboxPB */)/*: ShoeboxIF */ {
    var i, j, len, len1, object_id, object_name, quantum, quantum_pb, ref, ref1, shoebox;
    shoebox = Shoebox(shoebox_pb.getName());
    ref = shoebox_pb.getQuantaList();
    // parse quanta
    for (i = 0, len = ref.length; i < len; i++) {
      quantum_pb = ref[i];
      quantum = Quantum.deserialize(quantum_pb);
      // add stub to shoebox
      shoebox.register_quantum(quantum, quantum.id);
    }
    ref1 = shoebox_pb.getObjectsMap().entries();
    // parse objects
    for (j = 0, len1 = ref1.length; j < len1; j++) {
      [object_name, object_id] = ref1[j];
      shoebox.name_quantum(object_name, object_id);
    }
    // return newly built shoebox
    return shoebox;
  };

}).call(this);