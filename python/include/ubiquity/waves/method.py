from collections import OrderedDict
from typing import Dict, Union, Any, Iterable

from . import Wave
from ubiquity.types import ShoeboxIF, QuantumID, Quantum
from ubiquity.serialization.Wave_pb2 import WavePB, MethodCallRequestPB, MethodCallResponsePB
from ubiquity.serialization.Method_pb2 import ParameterPB
from ubiquity.serialization.any import serialize_any, deserialize_any

MethodArguments = Iterable[Any]
MethodKWArguments = Dict[str, Any]


class MethodCallRequestWave(Wave):
    _type = "MC"

    def __init__(self,
                 shoebox: Union[ShoeboxIF, None],
                 quantum_id: Union[QuantumID, None],
                 method_name: str,
                 args: MethodArguments,
                 kwargs: MethodKWArguments,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, None, wave_id=wave_id)
        self._method_name = method_name
        self._args = args
        self._kwargs = kwargs

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def args(self) -> MethodArguments:
        return self._args

    @property
    def kwargs(self) -> MethodKWArguments:
        return self._kwargs

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Wave:
        res = getattr(shoebox.quanta[self.quantum_id], self.method_name)(*self.args, **self.kwargs)
        return MethodCallResponseWave(shoebox, self.quantum_id, self.id, res)

    def _serialize(self) -> MethodCallRequestPB:
        wave_pb = MethodCallRequestPB()
        wave_pb.method.name = self.method_name
        for value in self.args:
            p = ParameterPB()
            qid, q = serialize_any(value, self.shoebox)
            if qid is not None:
                self.shoebox.register_quantum(value, qid)
            p.value.Pack(q)
            wave_pb.arguments.append(p)
        for key, value in self.kwargs.items():
            p = ParameterPB(name=key)
            qid, q = serialize_any(value, self.shoebox)
            if qid is not None:
                self.shoebox.register_quantum(value, qid)
            p.value.Pack(q)
            wave_pb.kwarguments.append(p)
        return wave_pb

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, MethodCallRequestPB]) -> 'MethodCallRequestWave':
        if isinstance(wave_pb, MethodCallRequestPB):
            return MethodCallRequestWave(
                None,
                None,
                wave_pb.method.name,
                [deserialize_any(a.value) for a in wave_pb.arguments],
                OrderedDict([
                    (a.name, deserialize_any(a.value))
                    for a in wave_pb.kwarguments
                ])
            )
        if isinstance(wave_pb, WavePB):
            return MethodCallRequestWave(
                wave_pb.header.shoebox,
                wave_pb.header.quantum_id,
                wave_pb.method_call_request.method.name,
                [deserialize_any(a.value) for a in wave_pb.method_call_request.arguments],
                OrderedDict([
                    (a.name, deserialize_any(a.value))
                    for a in wave_pb.method_call_request.kwarguments
                ]),
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
        # turn Quantum objects into their corresponding QuantumStub(s)
        self._return_value = Quantum.build_stubs(self.return_value, shoebox)

    def _serialize(self) -> MethodCallResponsePB:
        wave_pb = MethodCallResponsePB()
        _, quantum_pb = serialize_any(self.return_value, self.shoebox)
        wave_pb.return_value.Pack(quantum_pb)
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
