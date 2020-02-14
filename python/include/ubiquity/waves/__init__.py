import traceback
from abc import ABC
from typing import Union, Any

from ubiquity.types import ShoeboxIF, WaveIF, QuantumID
from ubiquity.serialization.Wave_pb2 import WavePB


class Wave(WaveIF, ABC):

    def __init__(self, shoebox: Union[ShoeboxIF, None], quantum_id: Union[QuantumID, None],
                 request_wave: Union[str, None], wave_id: Union[str, None] = None):
        super().__init__(shoebox, quantum_id, request_wave, wave_id=wave_id)

    def serialize(self) -> WavePB:
        from ubiquity.serialization.wave import serialize_wave
        return serialize_wave(self)

    @staticmethod
    def deserialize(wave_pb: WavePB) -> WaveIF:
        from ubiquity.serialization.wave import deserialize_wave
        try:
            return deserialize_wave(wave_pb)
        except Exception:
            traceback.print_exc()

    def serialize_data(self) -> Any:
        try:
            return self._serialize()
        except Exception:
            traceback.print_exc()
