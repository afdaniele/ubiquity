from typing import Dict, Union, Any

from . import Wave
from ubiquity.exceptions import WaveParseError
from ubiquity.types import ShoeboxIF
from ubiquity import Shoebox
from ubiquity.serialization.Wave_pb2 import WavePB, WaveTypePB
from ubiquity.serialization.Shoebox_pb2 import ShoeboxPB


MethodArguments = Dict[str, Any]


class ShoeboxWave(Wave):

    def __init__(self, shoebox: ShoeboxIF, request_wave: Union[str, None] = None):
        super().__init__(shoebox, request_wave)

    def hit(self, shoebox: Union[None, ShoeboxIF]) -> Union[None, Wave]:
        if shoebox is None:
            return None
        # ---
        shoebox.merge(self.shoebox)

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
            return ShoeboxWave(shoebox, wave_pb.header.request_wave)
        # except Exception:
        #     raise WaveParseError()
