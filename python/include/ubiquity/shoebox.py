import time
import asyncio
from typing import Any, Union

from .types import QuantumID, ShoeboxIF, WaveIF
from .tunnel import Tunnel, AsyncTunnel
from .serialization.Shoebox_pb2 import ShoeboxPB


class Shoebox(ShoeboxIF):

    def __init__(self, name: str):
        super().__init__(name)

    def register_quantum(self, obj: Any, quantum_id: QuantumID = None) -> QuantumID:
        if obj is None:
            raise ValueError('None not supported as quantum object')
        if quantum_id is None:
            # get ID of the object (if not given)
            quantum_id = id(obj)
        # add quantum
        self._quanta[quantum_id] = obj
        self.logger.debug('New quantum QT-{:d} registered!'.format(quantum_id))
        return quantum_id

    def name_quantum(self, name: str, quantum_id: QuantumID):
        if not name.isidentifier():
            raise ValueError('The name "{:s}" is not a valid identifier for the object' % name)
        if quantum_id not in self._quanta:
            raise KeyError('The ID "{:d}" does not indicate a valid quantum object' % quantum_id)
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
        self.logger.debug('Tunnel /{:s}\\ attached.'.format(str(tunnel)))

    def detach(self, tunnel: 'Tunnel'):
        tunnel.detach()
        self._tunnels.remove(tunnel)
        self.logger.debug('Tunnel /:s\\ detached.'.format(str(tunnel)))

    def wave_in(self, wave: 'WaveIF'):
        if wave.request_wave is None or wave.request_wave == '':
            self.logger.debug('Wave {:s} hitting the shoebox.'.format(str(wave)))
            res = wave.hit(self)
            if isinstance(res, WaveIF):
                self.wave_out(res)
        else:
            self.logger.debug('Wave {:s} responds to {:s}. Queued!'.format(
                str(wave), wave.request_wave[:8]
            ))
            self._waves_in[wave.request_wave] = wave

    def wave_out(self, wave: 'WaveIF'):
        self.logger.debug('Generated wave {:s} ({:d} tunnels).'.format(
            str(wave), len(self._tunnels)
        ))
        for tunnel in self._tunnels:
            # asyncio.get_event_loop().create_task(tunnel.wave_out(wave))


            if isinstance(tunnel, AsyncTunnel):
                asyncio.run_coroutine_threadsafe(
                    tunnel.wave_out(wave), tunnel.event_loop
                )
            else:
                asyncio.run_coroutine_threadsafe(
                    tunnel.wave_out(wave), asyncio.get_event_loop()
                )

            # tunnel.wave_out(wave)

    def wait_on(self, request_wave: Union[str, 'WaveIF'], timeout: int = 0):
        if isinstance(request_wave, WaveIF):
            request_wave = request_wave.id
        start_time = time.time()
        # wait for response in the queue
        while request_wave not in self._waves_in:
            # is timeout?
            if 0 < timeout < time.time() - start_time:
                raise TimeoutError()
            time.sleep(0.1)
        res = None
        # get response out of the queue
        self._waves_in_lock.acquire()
        if request_wave in self._waves_in:
            res = self._waves_in[request_wave]
            del self._waves_in[request_wave]
            self.logger.debug('Queued wave {:s} consumed by its listener'.format(str(res)))
        self._waves_in_lock.release()
        # return response
        return res

    def serialize(self) -> ShoeboxPB:
        from .serialization.shoebox import serialize_shoebox
        return serialize_shoebox(self)

    def destroy(self, recursive: bool = False):
        for tunnel in self._tunnels:
            self.detach(tunnel)
            if recursive:
                tunnel.shutdown()

    @staticmethod
    def deserialize(shoebox_pb: ShoeboxPB) -> ShoeboxIF:
        from .serialization.shoebox import deserialize_shoebox
        return deserialize_shoebox(shoebox_pb)

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
