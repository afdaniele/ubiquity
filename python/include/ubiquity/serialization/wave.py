from ubiquity.types import WaveIF

from ubiquity.waves.shoebox import ShoeboxWave
from ubiquity.waves.field import \
    FieldGetRequestWave, \
    FieldGetResponseWave, \
    FieldSetRequestWave, \
    FieldSetResponseWave
from ubiquity.waves.method import MethodCallRequestWave, MethodCallResponseWave
from ubiquity.waves.error import ErrorWave

from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB
from ubiquity.serialization.Wave_pb2 import \
    WavePB, \
    WaveTypePB, \
    FieldGetRequestPB, \
    FieldGetResponsePB, \
    FieldSetRequestPB, \
    FieldSetResponsePB, \
    MethodCallRequestPB, \
    MethodCallResponsePB, \
    ErrorPB

wave_type_map = {
    ShoeboxWave: WaveTypePB.SHOEBOX,
    FieldGetRequestWave: WaveTypePB.FIELD_GETTER_REQUEST,
    FieldGetResponseWave: WaveTypePB.FIELD_GETTER_RESPONSE,
    FieldSetRequestWave: WaveTypePB.FIELD_SETTER_REQUEST,
    FieldSetResponseWave: WaveTypePB.FIELD_SETTER_RESPONSE,
    MethodCallRequestWave: WaveTypePB.METHOD_CALL_REQUEST,
    MethodCallResponseWave: WaveTypePB.METHOD_CALL_RESPONSE,
    ErrorWave: WaveTypePB.ERROR
}

wave_parser_map = dict(zip(wave_type_map.values(), wave_type_map.keys()))


def serialize_wave(wave: WaveIF) -> WavePB:
    wave_pb = WavePB()
    wave_pb.header.type = wave_type_map[type(wave)]
    wave_pb.header.shoebox = wave.shoebox.name if wave.shoebox else ''
    wave_pb.header.quantum_id = wave.quantum_id if wave.quantum_id else 0
    wave_pb.header.request_wave = wave.request_wave or ''
    # serialize data
    wave_data = wave.serialize_data()
    # store data
    if isinstance(wave_data, ShoeboxPB):
        wave_pb.shoebox.MergeFrom(wave_data)
    elif isinstance(wave_data, FieldGetRequestPB):
        wave_pb.field_get_request.MergeFrom(wave_data)
    elif isinstance(wave_data, FieldGetResponsePB):
        wave_pb.field_get_response.MergeFrom(wave_data)
    elif isinstance(wave_data, FieldSetRequestPB):
        wave_pb.field_set_request.MergeFrom(wave_data)
    elif isinstance(wave_data, FieldSetResponsePB):
        wave_pb.field_set_response.MergeFrom(wave_data)
    elif isinstance(wave_data, MethodCallRequestPB):
        wave_pb.method_call_request.MergeFrom(wave_data)
    elif isinstance(wave_data, MethodCallResponsePB):
        wave_pb.method_call_response.MergeFrom(wave_data)
    elif isinstance(wave_data, ErrorPB):
        wave_pb.error.MergeFrom(wave_data)
    # ---
    return wave_pb


def deserialize_wave(wave_pb: WavePB) -> WaveIF:
    parser = wave_parser_map[wave_pb.header.type]
    return parser.deserialize(wave_pb)
