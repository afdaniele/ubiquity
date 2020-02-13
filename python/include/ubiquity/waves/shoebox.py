from typing import Dict, Union, Any

from . import Wave
from ubiquity.types import ShoeboxIF
from ubiquity import Shoebox
from ubiquity.serialization.Wave_pb2 import WavePB, WaveTypePB
from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB

MethodArguments = Dict[str, Any]


class ShoeboxWave(Wave):
    _type = "SB"

    def __init__(self,
                 shoebox: ShoeboxIF,
                 request_wave: Union[str, None] = None,
                 wave_id: Union[str, None] = None):
        super().__init__(shoebox, None, request_wave, wave_id=wave_id)

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> None:
        # merge quanta
        for _, quantum_builder in self.shoebox.quanta.items():
            quantum_id = quantum_builder.get_quantum_id()
            quantum = quantum_builder.build(shoebox)
            # add stub to shoebox
            shoebox.register_quantum(quantum, quantum_id)
        # parse objects
        for object_name, object_id in self.shoebox.objects.items():
            shoebox.name_quantum(object_name, object_id)

    def _serialize(self) -> ShoeboxPB:
        return self._shoebox.serialize()

    @staticmethod
    def deserialize(wave_pb: Union[WavePB, ShoeboxPB]) -> 'ShoeboxWave':
        # try:
        if isinstance(wave_pb, ShoeboxPB):
            shoebox = Shoebox.deserialize(wave_pb)
            return ShoeboxWave(shoebox, None)
        if isinstance(wave_pb, WavePB) and wave_pb.header.type == WaveTypePB.SHOEBOX:
            shoebox = Shoebox.deserialize(wave_pb.shoebox)
            return ShoeboxWave(shoebox, wave_pb.header.request_wave, wave_id=wave_pb.header.id)
        # except Exception:
        #     raise WaveParseError()
