# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ubiquity/serialization/Wave.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ubiquity.serialization import Shoebox_pb2 as ubiquity_dot_serialization_dot_Shoebox__pb2
from ubiquity.serialization import Field_pb2 as ubiquity_dot_serialization_dot_Field__pb2
from ubiquity.serialization import Method_pb2 as ubiquity_dot_serialization_dot_Method__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ubiquity/serialization/Wave.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n!ubiquity/serialization/Wave.proto\x1a\x19google/protobuf/any.proto\x1a$ubiquity/serialization/Shoebox.proto\x1a\"ubiquity/serialization/Field.proto\x1a#ubiquity/serialization/Method.proto\"\x9d\x03\n\x06WavePB\x12\x1d\n\x06header\x18\x01 \x01(\x0b\x32\r.WaveHeaderPB\x12\x1d\n\x07shoebox\x18\n \x01(\x0b\x32\n.ShoeboxPBH\x00\x12/\n\x11\x66ield_get_request\x18\x0b \x01(\x0b\x32\x12.FieldGetRequestPBH\x00\x12\x31\n\x12\x66ield_get_response\x18\x0c \x01(\x0b\x32\x13.FieldGetResponsePBH\x00\x12/\n\x11\x66ield_set_request\x18\r \x01(\x0b\x32\x12.FieldSetRequestPBH\x00\x12\x31\n\x12\x66ield_set_response\x18\x0e \x01(\x0b\x32\x13.FieldSetResponsePBH\x00\x12\x33\n\x13method_call_request\x18\x0f \x01(\x0b\x32\x14.MethodCallRequestPBH\x00\x12\x35\n\x14method_call_response\x18\x10 \x01(\x0b\x32\x15.MethodCallResponsePBH\x00\x12\x19\n\x05\x65rror\x18\x11 \x01(\x0b\x32\x08.ErrorPBH\x00\x42\x06\n\x04\x64\x61ta\"p\n\x0cWaveHeaderPB\x12\n\n\x02id\x18\x01 \x01(\t\x12\x19\n\x04type\x18\x02 \x01(\x0e\x32\x0b.WaveTypePB\x12\x0f\n\x07shoebox\x18\x03 \x01(\t\x12\x12\n\nquantum_id\x18\x04 \x01(\x03\x12\x14\n\x0crequest_wave\x18\x05 \x01(\t\",\n\x11\x46ieldGetRequestPB\x12\x17\n\x05\x66ield\x18\x01 \x01(\x0b\x32\x08.FieldPB\"@\n\x12\x46ieldGetResponsePB\x12*\n\x0creturn_value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\",\n\x11\x46ieldSetRequestPB\x12\x17\n\x05\x66ield\x18\x01 \x01(\x0b\x32\x08.FieldPB\"\x14\n\x12\x46ieldSetResponsePB\"Q\n\x13MethodCallRequestPB\x12\x19\n\x06method\x18\x01 \x01(\x0b\x32\t.MethodPB\x12\x1f\n\targuments\x18\x02 \x03(\x0b\x32\x0c.ParameterPB\"B\n\x14MethodCallResponsePB\x12*\n\x0creturn_value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\"\x18\n\x07\x45rrorPB\x12\r\n\x05\x65rror\x18\x01 \x01(\t*\xcb\x01\n\nWaveTypePB\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07SHOEBOX\x10\x01\x12\x18\n\x14\x46IELD_GETTER_REQUEST\x10\x02\x12\x19\n\x15\x46IELD_GETTER_RESPONSE\x10\x03\x12\x18\n\x14\x46IELD_SETTER_REQUEST\x10\x04\x12\x19\n\x15\x46IELD_SETTER_RESPONSE\x10\x05\x12\x17\n\x13METHOD_CALL_REQUEST\x10\x06\x12\x18\n\x14METHOD_CALL_RESPONSE\x10\x07\x12\t\n\x05\x45RROR\x10\x14\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,ubiquity_dot_serialization_dot_Shoebox__pb2.DESCRIPTOR,ubiquity_dot_serialization_dot_Field__pb2.DESCRIPTOR,ubiquity_dot_serialization_dot_Method__pb2.DESCRIPTOR,])

_WAVETYPEPB = _descriptor.EnumDescriptor(
  name='WaveTypePB',
  full_name='WaveTypePB',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHOEBOX', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_GETTER_REQUEST', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_GETTER_RESPONSE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_SETTER_REQUEST', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_SETTER_RESPONSE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='METHOD_CALL_REQUEST', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='METHOD_CALL_RESPONSE', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=8, number=20,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1063,
  serialized_end=1266,
)
_sym_db.RegisterEnumDescriptor(_WAVETYPEPB)

WaveTypePB = enum_type_wrapper.EnumTypeWrapper(_WAVETYPEPB)
NONE = 0
SHOEBOX = 1
FIELD_GETTER_REQUEST = 2
FIELD_GETTER_RESPONSE = 3
FIELD_SETTER_REQUEST = 4
FIELD_SETTER_RESPONSE = 5
METHOD_CALL_REQUEST = 6
METHOD_CALL_RESPONSE = 7
ERROR = 20



_WAVEPB = _descriptor.Descriptor(
  name='WavePB',
  full_name='WavePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='WavePB.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shoebox', full_name='WavePB.shoebox', index=1,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_get_request', full_name='WavePB.field_get_request', index=2,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_get_response', full_name='WavePB.field_get_response', index=3,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_set_request', full_name='WavePB.field_set_request', index=4,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_set_response', full_name='WavePB.field_set_response', index=5,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method_call_request', full_name='WavePB.method_call_request', index=6,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method_call_response', full_name='WavePB.method_call_response', index=7,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='WavePB.error', index=8,
      number=17, type=11, cpp_type=10, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='WavePB.data',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=176,
  serialized_end=589,
)


_WAVEHEADERPB = _descriptor.Descriptor(
  name='WaveHeaderPB',
  full_name='WaveHeaderPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='WaveHeaderPB.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='WaveHeaderPB.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shoebox', full_name='WaveHeaderPB.shoebox', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quantum_id', full_name='WaveHeaderPB.quantum_id', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request_wave', full_name='WaveHeaderPB.request_wave', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=591,
  serialized_end=703,
)


_FIELDGETREQUESTPB = _descriptor.Descriptor(
  name='FieldGetRequestPB',
  full_name='FieldGetRequestPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field', full_name='FieldGetRequestPB.field', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=705,
  serialized_end=749,
)


_FIELDGETRESPONSEPB = _descriptor.Descriptor(
  name='FieldGetResponsePB',
  full_name='FieldGetResponsePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='return_value', full_name='FieldGetResponsePB.return_value', index=0,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=751,
  serialized_end=815,
)


_FIELDSETREQUESTPB = _descriptor.Descriptor(
  name='FieldSetRequestPB',
  full_name='FieldSetRequestPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field', full_name='FieldSetRequestPB.field', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=817,
  serialized_end=861,
)


_FIELDSETRESPONSEPB = _descriptor.Descriptor(
  name='FieldSetResponsePB',
  full_name='FieldSetResponsePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=863,
  serialized_end=883,
)


_METHODCALLREQUESTPB = _descriptor.Descriptor(
  name='MethodCallRequestPB',
  full_name='MethodCallRequestPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='MethodCallRequestPB.method', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='MethodCallRequestPB.arguments', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=885,
  serialized_end=966,
)


_METHODCALLRESPONSEPB = _descriptor.Descriptor(
  name='MethodCallResponsePB',
  full_name='MethodCallResponsePB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='return_value', full_name='MethodCallResponsePB.return_value', index=0,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=968,
  serialized_end=1034,
)


_ERRORPB = _descriptor.Descriptor(
  name='ErrorPB',
  full_name='ErrorPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='ErrorPB.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=1036,
  serialized_end=1060,
)

_WAVEPB.fields_by_name['header'].message_type = _WAVEHEADERPB
_WAVEPB.fields_by_name['shoebox'].message_type = ubiquity_dot_serialization_dot_Shoebox__pb2._SHOEBOXPB
_WAVEPB.fields_by_name['field_get_request'].message_type = _FIELDGETREQUESTPB
_WAVEPB.fields_by_name['field_get_response'].message_type = _FIELDGETRESPONSEPB
_WAVEPB.fields_by_name['field_set_request'].message_type = _FIELDSETREQUESTPB
_WAVEPB.fields_by_name['field_set_response'].message_type = _FIELDSETRESPONSEPB
_WAVEPB.fields_by_name['method_call_request'].message_type = _METHODCALLREQUESTPB
_WAVEPB.fields_by_name['method_call_response'].message_type = _METHODCALLRESPONSEPB
_WAVEPB.fields_by_name['error'].message_type = _ERRORPB
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['shoebox'])
_WAVEPB.fields_by_name['shoebox'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['field_get_request'])
_WAVEPB.fields_by_name['field_get_request'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['field_get_response'])
_WAVEPB.fields_by_name['field_get_response'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['field_set_request'])
_WAVEPB.fields_by_name['field_set_request'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['field_set_response'])
_WAVEPB.fields_by_name['field_set_response'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['method_call_request'])
_WAVEPB.fields_by_name['method_call_request'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['method_call_response'])
_WAVEPB.fields_by_name['method_call_response'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEPB.oneofs_by_name['data'].fields.append(
  _WAVEPB.fields_by_name['error'])
_WAVEPB.fields_by_name['error'].containing_oneof = _WAVEPB.oneofs_by_name['data']
_WAVEHEADERPB.fields_by_name['type'].enum_type = _WAVETYPEPB
_FIELDGETREQUESTPB.fields_by_name['field'].message_type = ubiquity_dot_serialization_dot_Field__pb2._FIELDPB
_FIELDGETRESPONSEPB.fields_by_name['return_value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_FIELDSETREQUESTPB.fields_by_name['field'].message_type = ubiquity_dot_serialization_dot_Field__pb2._FIELDPB
_METHODCALLREQUESTPB.fields_by_name['method'].message_type = ubiquity_dot_serialization_dot_Method__pb2._METHODPB
_METHODCALLREQUESTPB.fields_by_name['arguments'].message_type = ubiquity_dot_serialization_dot_Method__pb2._PARAMETERPB
_METHODCALLRESPONSEPB.fields_by_name['return_value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['WavePB'] = _WAVEPB
DESCRIPTOR.message_types_by_name['WaveHeaderPB'] = _WAVEHEADERPB
DESCRIPTOR.message_types_by_name['FieldGetRequestPB'] = _FIELDGETREQUESTPB
DESCRIPTOR.message_types_by_name['FieldGetResponsePB'] = _FIELDGETRESPONSEPB
DESCRIPTOR.message_types_by_name['FieldSetRequestPB'] = _FIELDSETREQUESTPB
DESCRIPTOR.message_types_by_name['FieldSetResponsePB'] = _FIELDSETRESPONSEPB
DESCRIPTOR.message_types_by_name['MethodCallRequestPB'] = _METHODCALLREQUESTPB
DESCRIPTOR.message_types_by_name['MethodCallResponsePB'] = _METHODCALLRESPONSEPB
DESCRIPTOR.message_types_by_name['ErrorPB'] = _ERRORPB
DESCRIPTOR.enum_types_by_name['WaveTypePB'] = _WAVETYPEPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WavePB = _reflection.GeneratedProtocolMessageType('WavePB', (_message.Message,), {
  'DESCRIPTOR' : _WAVEPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:WavePB)
  })
_sym_db.RegisterMessage(WavePB)

WaveHeaderPB = _reflection.GeneratedProtocolMessageType('WaveHeaderPB', (_message.Message,), {
  'DESCRIPTOR' : _WAVEHEADERPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:WaveHeaderPB)
  })
_sym_db.RegisterMessage(WaveHeaderPB)

FieldGetRequestPB = _reflection.GeneratedProtocolMessageType('FieldGetRequestPB', (_message.Message,), {
  'DESCRIPTOR' : _FIELDGETREQUESTPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:FieldGetRequestPB)
  })
_sym_db.RegisterMessage(FieldGetRequestPB)

FieldGetResponsePB = _reflection.GeneratedProtocolMessageType('FieldGetResponsePB', (_message.Message,), {
  'DESCRIPTOR' : _FIELDGETRESPONSEPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:FieldGetResponsePB)
  })
_sym_db.RegisterMessage(FieldGetResponsePB)

FieldSetRequestPB = _reflection.GeneratedProtocolMessageType('FieldSetRequestPB', (_message.Message,), {
  'DESCRIPTOR' : _FIELDSETREQUESTPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:FieldSetRequestPB)
  })
_sym_db.RegisterMessage(FieldSetRequestPB)

FieldSetResponsePB = _reflection.GeneratedProtocolMessageType('FieldSetResponsePB', (_message.Message,), {
  'DESCRIPTOR' : _FIELDSETRESPONSEPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:FieldSetResponsePB)
  })
_sym_db.RegisterMessage(FieldSetResponsePB)

MethodCallRequestPB = _reflection.GeneratedProtocolMessageType('MethodCallRequestPB', (_message.Message,), {
  'DESCRIPTOR' : _METHODCALLREQUESTPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:MethodCallRequestPB)
  })
_sym_db.RegisterMessage(MethodCallRequestPB)

MethodCallResponsePB = _reflection.GeneratedProtocolMessageType('MethodCallResponsePB', (_message.Message,), {
  'DESCRIPTOR' : _METHODCALLRESPONSEPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:MethodCallResponsePB)
  })
_sym_db.RegisterMessage(MethodCallResponsePB)

ErrorPB = _reflection.GeneratedProtocolMessageType('ErrorPB', (_message.Message,), {
  'DESCRIPTOR' : _ERRORPB,
  '__module__' : 'ubiquity.serialization.Wave_pb2'
  # @@protoc_insertion_point(class_scope:ErrorPB)
  })
_sym_db.RegisterMessage(ErrorPB)


# @@protoc_insertion_point(module_scope)
