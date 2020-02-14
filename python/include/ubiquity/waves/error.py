import traceback
from typing import Union
from types import TracebackType

from . import Wave
from ubiquity.types import ShoeboxIF, WaveIF, QuantumID
from ubiquity.serialization.Wave_pb2 import WavePB, ErrorPB


class ErrorWave(Wave):
    _type = "EE"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 error: str,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)
        self._error = error

    @property
    def error(self) -> str:
        return self._error

    def hit(self, shoebox: Union[None, ShoeboxIF]):
        pass

    def _serialize(self) -> ErrorPB:
        return ErrorPB(error=self.error)

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, ErrorPB]) -> 'ErrorWave':
        if isinstance(wave_pb, ErrorPB):
            return ErrorWave(
                None,
                None,
                None,
                wave_pb.error
            )
        if isinstance(wave_pb, WavePB):
            return ErrorWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.header.request_wave,
                wave_pb.error.error,
                wave_id=wave_pb.header.id
            )

    @staticmethod
    def from_exception(request_wave: Union[str, None], ex_type: BaseException,
                       ex_value: Exception, ex_traceback: TracebackType) -> 'ErrorWave':
        # turn exception into an ErrorWave
        return ErrorWave(
            None,
            None,
            request_wave,
            str(traceback.format_exception(ex_type, ex_value, ex_traceback))
        )
