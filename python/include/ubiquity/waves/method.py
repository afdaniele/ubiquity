from typing import Dict, Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF, QuantumID
from ubiquity.serialization.Wave_pb2 import WavePB, MethodCallRequestPB, MethodCallResponsePB

MethodArguments = Dict[str, Any]


class MethodCallRequestWave(Wave):
    _type = "MC"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 method_name: str,
                 args: MethodArguments,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)
        self._method_name = method_name
        self._args = args

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def args(self) -> MethodArguments:
        return self._args

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Wave:
        pass

    def _serialize(self) -> MethodCallRequestPB:
        wave_pb = MethodCallRequestPB()
        wave_pb.method.name = self.method_name
        # TODO: args
        wave_pb.arguments = []
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallRequestPB]) -> 'MethodCallRequestWave':
        try:
            if isinstance(wave_pb, MethodCallRequestPB):
                # TODO: args
                return MethodCallRequestWave(
                    None,
                    None,
                    None,
                    wave_pb.method_call_request.method.name,
                    {}
                )
            if isinstance(wave_pb, WavePB):
                # TODO: args
                return MethodCallRequestWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave,
                    wave_pb.method_call_request.method.name,
                    {},
                    wave_id=wave_pb.header.id
                )
        except Exception:
            raise WaveParseError()


class MethodCallResponseWave(Wave):
    _type = "MR"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None],
                 return_value: Any,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)
        self._return_value = return_value

    @property
    def return_value(self) -> Any:
        return self._return_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> None:
        pass

    def _serialize(self) -> MethodCallResponsePB:
        wave_pb = MethodCallResponsePB()
        wave_pb.return_value = self.return_value
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallResponsePB]) -> 'MethodCallResponseWave':
        try:
            if isinstance(wave_pb, MethodCallResponsePB):
                return MethodCallResponseWave(
                    None,
                    None,
                    None,
                    wave_pb.method_call_response.return_value
                )
            if isinstance(wave_pb, WavePB):
                return MethodCallResponseWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.quantum_id,
                    wave_pb.header.request_wave,
                    wave_pb.method_call_response.return_value,
                    wave_id=wave_pb.header.id
                )
        except Exception:
            raise WaveParseError()
