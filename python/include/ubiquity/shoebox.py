from typing import Any, Dict, Union

from .types import QuantumID, ShoeboxIF
from .tunnel import Tunnel


class Shoebox(ShoeboxIF):

    def __init__(self, name: str):
        super().__init__(name)

    def register_quantum(self, obj: Any) -> QuantumID:
        if obj is None:
            raise ValueError('None not supported as quantum object')
        # get ID of the object
        quantum_id = id(obj)
        # add quantum
        self._quanta[quantum_id] = obj
        return quantum_id

    def name_quantum(self, name: str, quantum_id: QuantumID):
        if not name.isidentifier():
            raise ValueError('The name "{:s}" is not a valid identifier for the object' % name)
        self._objects[name] = quantum_id
        setattr(self.content, name, self._quanta[quantum_id])

    def add(self, name: str, obj: Any):
        if not name.isidentifier():
            raise ValueError('The name "{:s}" is not a valid identifier for the object' % name)
        quantum_id = self.register_quantum(obj)
        self.name_quantum(name, quantum_id)

    def attach(self, tunnel: 'Tunnel'):
        self._tunnels.append(tunnel)
        tunnel.attach(self)

    def detach(self, tunnel: 'Tunnel'):
        tunnel.detach()
        self._tunnels.remove(tunnel)

    def serialize(self) -> dict:
        from .serialization import serialize_shoebox
        return serialize_shoebox(self)

    @staticmethod
    def deserialize(shoebox_raw: Union[str, Dict]) -> 'Shoebox':
        from .serialization import deserialize_shoebox
        return deserialize_shoebox(shoebox_raw)


# > Entanglement:
# The phenomenon in quantum theory whereby particles that interact with each other become
# permanently dependent on each other’s quantum states and properties, to the extent that
# they lose their individuality and in many ways behave as a single entity. At some level,
# entangled particles appear to “know” each other’s states and properties.


# > Nonlocality:
# The rather spooky ability of objects in quantum theory to apparently instantaneously
# know about each other’s quantum state, even when separated by large distances, in
# apparent contravention of the principle of locality (the idea that distant objects cannot
# have direct influence on one another, and that an object is influenced directly only by
# its immediate surroundings).


# > Superposition:
# The ability in quantum theory of an object, such as an atom or sub-atomic particle,
# to be in more than one quantum state at the same time. For example, an object could
# technically be in more than one place simultaneously as a consequence of the wave-like
# character of microscopic particles.

# > Wave-Particle Duality:
# The idea that light (and indeed all matter and energy) is both a wave and a particle,
# and that sometimes it behaves like a wave and sometimes it behaves like a particle.
# It is a central concept of quantum theory.
