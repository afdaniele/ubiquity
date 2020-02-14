# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ubiquity/serialization/WellKnown.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ubiquity/serialization/WellKnown.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n&ubiquity/serialization/WellKnown.proto\x1a\x19google/protobuf/any.proto\"\x16\n\x05IntPB\x12\r\n\x05value\x18\x01 \x01(\x05\"\x18\n\x07\x46loatPB\x12\r\n\x05value\x18\x01 \x01(\x02\"\x19\n\x08StringPB\x12\r\n\x05value\x18\x01 \x01(\t\"\x17\n\x06\x42oolPB\x12\r\n\x05value\x18\x01 \x01(\x08\"2\n\nIterablePB\x12$\n\x06values\x18\x01 \x03(\x0b\x32\x14.google.protobuf.Any\"m\n\x05MapPB\x12 \n\x05items\x18\x01 \x03(\x0b\x32\x11.MapPB.ItemsEntry\x1a\x42\n\nItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01\"\x16\n\x06NonePB\x12\x0c\n\x04none\x18\x01 \x01(\x08\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,])




_INTPB = _descriptor.Descriptor(
  name='IntPB',
  full_name='IntPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='IntPB.value', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=69,
  serialized_end=91,
)


_FLOATPB = _descriptor.Descriptor(
  name='FloatPB',
  full_name='FloatPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='FloatPB.value', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=93,
  serialized_end=117,
)


_STRINGPB = _descriptor.Descriptor(
  name='StringPB',
  full_name='StringPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='StringPB.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=119,
  serialized_end=144,
)


_BOOLPB = _descriptor.Descriptor(
  name='BoolPB',
  full_name='BoolPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='BoolPB.value', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=146,
  serialized_end=169,
)


_ITERABLEPB = _descriptor.Descriptor(
  name='IterablePB',
  full_name='IterablePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='IterablePB.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=171,
  serialized_end=221,
)


_MAPPB_ITEMSENTRY = _descriptor.Descriptor(
  name='ItemsEntry',
  full_name='MapPB.ItemsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='MapPB.ItemsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='MapPB.ItemsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=266,
  serialized_end=332,
)

_MAPPB = _descriptor.Descriptor(
  name='MapPB',
  full_name='MapPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='MapPB.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MAPPB_ITEMSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=332,
)


_NONEPB = _descriptor.Descriptor(
  name='NonePB',
  full_name='NonePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='none', full_name='NonePB.none', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=334,
  serialized_end=356,
)

_ITERABLEPB.fields_by_name['values'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_MAPPB_ITEMSENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_MAPPB_ITEMSENTRY.containing_type = _MAPPB
_MAPPB.fields_by_name['items'].message_type = _MAPPB_ITEMSENTRY
DESCRIPTOR.message_types_by_name['IntPB'] = _INTPB
DESCRIPTOR.message_types_by_name['FloatPB'] = _FLOATPB
DESCRIPTOR.message_types_by_name['StringPB'] = _STRINGPB
DESCRIPTOR.message_types_by_name['BoolPB'] = _BOOLPB
DESCRIPTOR.message_types_by_name['IterablePB'] = _ITERABLEPB
DESCRIPTOR.message_types_by_name['MapPB'] = _MAPPB
DESCRIPTOR.message_types_by_name['NonePB'] = _NONEPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IntPB = _reflection.GeneratedProtocolMessageType('IntPB', (_message.Message,), {
  'DESCRIPTOR' : _INTPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:IntPB)
  })
_sym_db.RegisterMessage(IntPB)

FloatPB = _reflection.GeneratedProtocolMessageType('FloatPB', (_message.Message,), {
  'DESCRIPTOR' : _FLOATPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:FloatPB)
  })
_sym_db.RegisterMessage(FloatPB)

StringPB = _reflection.GeneratedProtocolMessageType('StringPB', (_message.Message,), {
  'DESCRIPTOR' : _STRINGPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:StringPB)
  })
_sym_db.RegisterMessage(StringPB)

BoolPB = _reflection.GeneratedProtocolMessageType('BoolPB', (_message.Message,), {
  'DESCRIPTOR' : _BOOLPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:BoolPB)
  })
_sym_db.RegisterMessage(BoolPB)

IterablePB = _reflection.GeneratedProtocolMessageType('IterablePB', (_message.Message,), {
  'DESCRIPTOR' : _ITERABLEPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:IterablePB)
  })
_sym_db.RegisterMessage(IterablePB)

MapPB = _reflection.GeneratedProtocolMessageType('MapPB', (_message.Message,), {

  'ItemsEntry' : _reflection.GeneratedProtocolMessageType('ItemsEntry', (_message.Message,), {
    'DESCRIPTOR' : _MAPPB_ITEMSENTRY,
    '__module__' : 'ubiquity.serialization.WellKnown_pb2'
    # @@protoc_insertion_point(class_scope:MapPB.ItemsEntry)
    })
  ,
  'DESCRIPTOR' : _MAPPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:MapPB)
  })
_sym_db.RegisterMessage(MapPB)
_sym_db.RegisterMessage(MapPB.ItemsEntry)

NonePB = _reflection.GeneratedProtocolMessageType('NonePB', (_message.Message,), {
  'DESCRIPTOR' : _NONEPB,
  '__module__' : 'ubiquity.serialization.WellKnown_pb2'
  # @@protoc_insertion_point(class_scope:NonePB)
  })
_sym_db.RegisterMessage(NonePB)


_MAPPB_ITEMSENTRY._options = None
# @@protoc_insertion_point(module_scope)
