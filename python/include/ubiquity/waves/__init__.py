from typing import Union, Any
from abc import ABC

from ubiquity.types import ShoeboxIF, WaveIF
from ubiquity.serialization.Wave_pb2 import WavePB


class Wave(WaveIF, ABC):

    def __init__(self, shoebox: Union[ShoeboxIF, None], request_wave: Union[str, None]):
        super().__init__(shoebox, request_wave)

    def serialize(self) -> WavePB:
        from ubiquity.serialization.wave import serialize_wave
        return serialize_wave(self)

    @staticmethod
    def deserialize(wave_pb: WavePB) -> WaveIF:
        from ubiquity.serialization.wave import deserialize_wave
        return deserialize_wave(wave_pb)

    def serialize_data(self) -> Any:
        return self._serialize()
