from typing import Dict, Union, Any

from . import Wave
from ubiquity.types import ShoeboxIF, QuantumID
from ubiquity.serialization.Wave_pb2 import WavePB, MethodCallRequestPB, MethodCallResponsePB
from ubiquity.serialization.Method_pb2 import ParameterPB
from ubiquity.serialization.any import serialize_any, deserialize_any

MethodArguments = Dict[str, Any]


class MethodCallRequestWave(Wave):
    _type = "MC"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 method_name: str,
                 args: MethodArguments,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, None, wave_id=wave_id)
        self._method_name = method_name
        self._args = args

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def args(self) -> MethodArguments:
        return self._args

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Wave:
        res = getattr(shoebox.quanta[self.quantum_id], self.method_name)(**self.args)
        return MethodCallResponseWave(shoebox, self.quantum_id, self.id, res)

    def _serialize(self) -> MethodCallRequestPB:
        wave_pb = MethodCallRequestPB()
        wave_pb.method.name = self.method_name
        print(self.args)
        for key, value in self.args.items():
            print("> {:s}={:s}".format(key, str(value)))
            p = ParameterPB(name=key)
            qid, q = serialize_any(value)
            if qid is not None:
                self.shoebox.register_quantum(value, qid)
            p.value.Pack(q)
            wave_pb.arguments.append(p)
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallRequestPB]) -> 'MethodCallRequestWave':

        def _get_args(call_request: MethodCallRequestPB) -> MethodArguments:
            args = {}
            for arg_pb in call_request.arguments:
                args[arg_pb.name] = deserialize_any(arg_pb.value)
            return args

        if isinstance(wave_pb, MethodCallRequestPB):
            return MethodCallRequestWave(
                None,
                None,
                wave_pb.method.name,
                _get_args(wave_pb)
            )
        if isinstance(wave_pb, WavePB):
            return MethodCallRequestWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.method_call_request.method.name,
                _get_args(wave_pb.method_call_request),
                wave_id=wave_pb.header.id
            )


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
        if self.return_value:
            qid, q = serialize_any(self.return_value)
            if qid is not None:
                self.shoebox.register_quantum(q, qid)
            wave_pb.return_value.Pack(q)
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallResponsePB]) -> 'MethodCallResponseWave':
        if isinstance(wave_pb, MethodCallResponsePB):
            return MethodCallResponseWave(
                None,
                None,
                None,
                deserialize_any(wave_pb.return_value)
            )
        if isinstance(wave_pb, WavePB):
            return MethodCallResponseWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.header.request_wave,
                deserialize_any(wave_pb.method_call_response.return_value),
                wave_id=wave_pb.header.id
            )
