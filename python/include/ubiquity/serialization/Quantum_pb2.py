# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ubiquity/serialization/Quantum.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ubiquity.serialization import Field_pb2 as ubiquity_dot_serialization_dot_Field__pb2
from ubiquity.serialization import Method_pb2 as ubiquity_dot_serialization_dot_Method__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ubiquity/serialization/Quantum.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n$ubiquity/serialization/Quantum.proto\x1a\"ubiquity/serialization/Field.proto\x1a#ubiquity/serialization/Method.proto\"M\n\tQuantumPB\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x18\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x08.FieldPB\x12\x1a\n\x07methods\x18\x03 \x03(\x0b\x32\t.MethodPBb\x06proto3')
  ,
  dependencies=[ubiquity_dot_serialization_dot_Field__pb2.DESCRIPTOR,ubiquity_dot_serialization_dot_Method__pb2.DESCRIPTOR,])




_QUANTUMPB = _descriptor.Descriptor(
  name='QuantumPB',
  full_name='QuantumPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='QuantumPB.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fields', full_name='QuantumPB.fields', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='methods', full_name='QuantumPB.methods', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=190,
)

_QUANTUMPB.fields_by_name['fields'].message_type = ubiquity_dot_serialization_dot_Field__pb2._FIELDPB
_QUANTUMPB.fields_by_name['methods'].message_type = ubiquity_dot_serialization_dot_Method__pb2._METHODPB
DESCRIPTOR.message_types_by_name['QuantumPB'] = _QUANTUMPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QuantumPB = _reflection.GeneratedProtocolMessageType('QuantumPB', (_message.Message,), {
  'DESCRIPTOR' : _QUANTUMPB,
  '__module__' : 'ubiquity.serialization.Quantum_pb2'
  # @@protoc_insertion_point(class_scope:QuantumPB)
  })
_sym_db.RegisterMessage(QuantumPB)


# @@protoc_insertion_point(module_scope)
