from typing import Union, Any

from . import Wave
from ubiquity.types import ShoeboxIF, QuantumID
from ubiquity.serialization.Wave_pb2 import \
    WavePB, \
    FieldGetRequestPB, \
    FieldGetResponsePB, \
    FieldSetRequestPB, \
    FieldSetResponsePB
from ubiquity.serialization.any import serialize_any, deserialize_any


class FieldGetRequestWave(Wave):
    _type = "FG"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 field_name: str,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, None, wave_id=wave_id)
        self._field_name = field_name

    @property
    def field_name(self) -> str:
        return self._field_name

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Wave:
        res = shoebox.quanta[self.quantum_id].__getattribute__(self.field_name)
        quantum_id, quantum = serialize_any(res)
        return FieldGetResponseWave(shoebox, quantum_id, self.id, quantum)

    def _serialize(self) -> FieldGetRequestPB:
        wave_pb = FieldGetRequestPB()
        wave_pb.field.name = self.field_name
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldGetRequestPB]) -> 'FieldGetRequestWave':
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
                wave_pb.field_get_request.field.name,
                wave_id=wave_pb.header.id
            )


class FieldGetResponseWave(Wave):
    _type = "FV"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 field_value: Any,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)
        self._field_value = field_value

    @property
    def field_value(self) -> Any:
        return self._field_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> None:
        pass

    def _serialize(self) -> FieldGetResponsePB:
        wave_pb = FieldGetResponsePB()
        wave_pb.return_value.Pack(self._field_value)
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldGetResponsePB]) -> 'FieldGetResponseWave':
        if isinstance(wave_pb, FieldGetResponsePB):
            return FieldGetResponseWave(
                None,
                None,
                None,
                deserialize_any(wave_pb.field_get_response.return_value)
            )
        if isinstance(wave_pb, WavePB):
            return FieldGetResponseWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.header.request_wave,
                deserialize_any(wave_pb.field_get_response.return_value),
                wave_id=wave_pb.header.id
            )


class FieldSetRequestWave(Wave):
    _type = "FS"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 field_name: str,
                 field_value: Any,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, None, wave_id=wave_id)
        self._field_name = field_name
        self._field_value = field_value

    @property
    def field_name(self) -> str:
        return self._field_name

    @property
    def field_value(self) -> Any:
        return self._field_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Wave:
        pass

    def _serialize(self) -> FieldSetRequestPB:
        wave_pb = FieldSetRequestPB()
        wave_pb.field.name = self.field_name
        qid, q = serialize_any(self.field_value)
        if qid is not None:
            self.shoebox.register_quantum(q, qid)
        wave_pb.field.value.Pack(q)
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldSetRequestPB]) -> 'FieldSetRequestWave':
        if isinstance(wave_pb, FieldSetRequestPB):
            return FieldSetRequestWave(
                None,
                None,
                wave_pb.field.name,
                deserialize_any(wave_pb.field.value)
            )
        if isinstance(wave_pb, WavePB):
            return FieldSetRequestWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.field_set_request.field.name,
                deserialize_any(wave_pb.field_set_request.field.value),
                wave_id=wave_pb.header.id
            )


class FieldSetResponseWave(Wave):
    _type = "FD"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> None:
        pass

    def _serialize(self) -> FieldSetResponsePB:
        return FieldSetResponsePB()

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, FieldSetResponsePB]) -> 'FieldSetResponseWave':
        if isinstance(wave_pb, FieldSetResponsePB):
            return FieldSetResponseWave(None, None, None)
        if isinstance(wave_pb, WavePB):
            return FieldSetResponseWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.header.request_wave,
                wave_id=wave_pb.header.id
            )
