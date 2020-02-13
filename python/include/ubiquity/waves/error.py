from types import TracebackType
from typing import Union

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF, WaveIF, QuantumID
from ubiquity.serialization.Wave_pb2 import WavePB, ErrorPB


class ErrorWave(Wave):

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 etype: str,
                 emessage: str,
                 etrace: str):
        super().__init__(shoebox, quantum_id, request_wave)
        self._error_type = etype
        self._error_message = emessage
        self._error_trace = etrace

    @property
    def error_type(self) -> str:
        return self._error_type

    @property
    def error_message(self) -> str:
        return self._error_message

    @property
    def error_trace(self) -> str:
        return self._error_trace

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, WaveIF]:
        return None

    def _serialize(self) -> ErrorPB:
        return ErrorPB(
            etype=self._error_type,
            emessage=self._error_message,
            etrace=self._error_trace
        )

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, ErrorPB]) -> 'ErrorWave':
        try:
            if isinstance(wave_pb, ErrorPB):
                return ErrorWave(
                    None, None, None, wave_pb.etype, wave_pb.emessage, wave_pb.etrace
                )
            if isinstance(wave_pb, WavePB):
                return ErrorWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave,
                    wave_pb.error.etype,
                    wave_pb.error.emessage,
                    wave_pb.error.etrace
                )
        except:
            raise WaveParseError()

    @staticmethod
    def from_exception(request_wave: Union[str, None], ex_type: BaseException,
                       ex_value: Exception, ex_traceback: TracebackType) -> 'ErrorWave':
        # turn exception into an ErrorRespondeWave
        return ErrorWave(None, None, request_wave, str(ex_type), str(ex_value), str(ex_traceback))
