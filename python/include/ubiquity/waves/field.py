from typing import Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF, QuantumID
from ubiquity.serialization.Wave_pb2 import \
    WavePB, \
    FieldGetRequestPB, \
    FieldGetResponsePB, \
    FieldSetRequestPB, \
    FieldSetResponsePB


class FieldGetRequestWave(Wave):

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 field_name: str):
        super().__init__(shoebox, quantum_id, None)
        self._field_name = field_name

    @property
    def field_name(self) -> str:
        return self._field_name

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        print('HIT!')

    def _serialize(self) -> FieldGetRequestPB:
        wave_pb = FieldGetRequestPB()
        wave_pb.field.name = self.field_name
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldGetRequestPB]) -> 'FieldGetRequestWave':
        try:
            if isinstance(wave_pb, FieldGetRequestPB):
                return FieldGetRequestWave(
                    None,
                    None,
                    wave_pb.field_get_request.field.name
                )
            if isinstance(wave_pb, WavePB):
                return FieldGetRequestWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.field_get_request.field.name
                )
        except Exception:
            raise WaveParseError()


class FieldGetResponseWave(Wave):

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 field_value: Any):
        super().__init__(shoebox, quantum_id, request_wave)
        self._field_value = field_value

    @property
    def field_value(self) -> Any:
        return self._field_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        pass

    def _serialize(self) -> FieldGetResponsePB:
        wave_pb = FieldGetResponsePB()
        wave_pb.return_value = self._field_value
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldGetResponsePB]) -> 'FieldGetResponseWave':
        try:
            if isinstance(wave_pb, FieldGetResponsePB):
                return FieldGetResponseWave(
                    None,
                    None,
                    None,
                    wave_pb.field_get_response.return_value
                )
            if isinstance(wave_pb, WavePB):
                return FieldGetResponseWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave,
                    wave_pb.field_get_response.return_value
                )
        except Exception:
            raise WaveParseError()


class FieldSetRequestWave(Wave):

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 field_name: str,
                 field_value: Any):
        super().__init__(shoebox, quantum_id, request_wave)
        self._field_name = field_name
        self._field_value = field_value

    @property
    def field_name(self) -> str:
        return self._field_name

    @property
    def field_value(self) -> Any:
        return self._field_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        pass

    def _serialize(self) -> FieldSetRequestPB:
        wave_pb = FieldSetRequestPB()
        wave_pb.field.name = self.field_name
        wave_pb.field.value = self.field_value
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldSetRequestPB]) -> 'FieldSetRequestWave':
        try:
            if isinstance(wave_pb, FieldSetRequestPB):
                return FieldSetRequestWave(
                    None,
                    None,
                    None,
                    wave_pb.field_set_request.field.name,
                    wave_pb.field_value
                )
            if isinstance(wave_pb, WavePB):
                return FieldSetRequestWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave,
                    wave_pb.field_set_request.field.name,
                    wave_pb.field_set_request.field.value
                )
        except Exception:
            raise WaveParseError()


class FieldSetResponseWave(Wave):

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None]):
        super().__init__(shoebox, quantum_id, request_wave)

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        pass

    def _serialize(self) -> FieldSetResponsePB:
        return FieldSetResponsePB()

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldSetResponsePB]) -> 'FieldSetResponseWave':
        try:
            if isinstance(wave_pb, FieldSetResponsePB):
                return FieldSetResponseWave(None, None, None)
            if isinstance(wave_pb, WavePB):
                return FieldSetResponseWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave
                )
        except Exception:
            raise WaveParseError()
