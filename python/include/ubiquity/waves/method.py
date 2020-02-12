from typing import Dict, Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF
from ubiquity.serialization.Wave_pb2 import WavePB, MethodCallRequestPB, MethodCallResponsePB

MethodArguments = Dict[str, Any]


class MethodCallRequestWave(Wave):

    def __init__(self, shoebox: Union[ShoeboxIF, None], request_wave: Union[str, None],
                 object_id: int, method_name: str, args: MethodArguments):
        super().__init__(shoebox, request_wave)
        self._object_id = object_id
        self._method_name = method_name
        self._args = args

    @property
    def object_id(self) -> int:
        return self._object_id

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def args(self) -> MethodArguments:
        return self._args

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        pass

    def _serialize(self) -> MethodCallRequestPB:
        wave_pb = MethodCallRequestPB()
        wave_pb.method.shoebox_name = self.shoebox.name
        wave_pb.method.object_id = self.object_id
        wave_pb.method.method_name = self.method_name
        # TODO: args
        wave_pb.arguments = []
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallRequestPB]) -> 'MethodCallRequestWave':
        try:
            if isinstance(wave_pb, MethodCallRequestPB):
                # TODO: args
                return MethodCallRequestWave(
                    None, None, wave_pb.method_call_request.method.object_id,
                    wave_pb.method_call_request.method.method_name,
                    {}
                )
            if isinstance(wave_pb, WavePB):
                return MethodCallRequestWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.request_wave,
                    wave_pb.method_call_request.method.object_id,
                    wave_pb.method_call_request.method.method_name,
                    {}
                )
        except Exception:
            raise WaveParseError()


class MethodCallResponseWave(Wave):

    def __init__(self, shoebox: Union[ShoeboxIF, None], request_wave: Union[str, None],
                 return_value: Any):
        super().__init__(shoebox, request_wave)
        self._return_value = return_value

    @property
    def return_value(self) -> Any:
        return self._return_value

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
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
                    None, None, wave_pb.method_call_response.return_value
                )
            if isinstance(wave_pb, WavePB):
                return MethodCallResponseWave(
                    wave_pb.header.shoebox,
                    wave_pb.header.request_wave,
                    wave_pb.method_call_response.return_value
                )
        except Exception:
            raise WaveParseError()
