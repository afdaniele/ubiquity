from ubiquity.types import WaveIF

from ubiquity.waves.shoebox import ShoeboxWave
from ubiquity.waves.field import FieldGetRequestWave, FieldGetResponseWave, FieldSetRequestWave, \
    FieldSetResponseWave
from ubiquity.waves.method import MethodCallRequestWave, MethodCallResponseWave
from ubiquity.waves.error import ErrorWave

from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB
from ubiquity.serialization.Wave_pb2 import \
    WavePB, \
    FieldGetRequestPB, \
    FieldGetResponsePB, \
    FieldSetRequestPB, \
    FieldSetResponsePB, \
    MethodCallRequestPB, \
    MethodCallResponsePB, \
    ErrorPB

wave_type_map = {
    ShoeboxWave: WavePB.Type.SHOEBOX,
    FieldGetRequestWave: WavePB.Type.FIELD_GETTER_REQUEST,
    FieldGetResponseWave: WavePB.Type.FIELD_GETTER_RESPONSE,
    FieldSetRequestWave: WavePB.Type.FIELD_SETTER_REQUEST,
    FieldSetResponseWave: WavePB.Type.FIELD_SETTER_RESPONSE,
    MethodCallRequestWave: WavePB.Type.METHOD_CALL_REQUEST,
    MethodCallResponseWave: WavePB.Type.METHOD_CALL_RESPONSE,
    ErrorWave: WavePB.Type.ERROR
}

wave_parser_map = dict(zip(wave_type_map.values(), wave_type_map.keys()))


def serialize_wave(wave: WaveIF) -> WavePB:
    wave_pb = WavePB()
    wave_pb.type = wave_type_map[type(wave)]
    wave_pb.header.shoebox_name = wave.shoebox.name
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
    parser = wave_parser_map[wave_pb.type]
    return parser.deserialize(wave_pb)