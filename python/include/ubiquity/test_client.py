import asyncio
from ubiquity import Shoebox
from ubiquity.tunnel.websocket import WebSocketClientTunnel


if __name__ == '__main__':

    sbox = Shoebox('general2')
    tunnel = WebSocketClientTunnel('localhost')

    sbox.attach(tunnel)

    # sbox.add('sn', a)
    # sbox.add('gopro', goproCamera)

    # print(json.dumps(sbox.serialize(), indent=4, sort_keys=False))

    print('Spinning the event_loop')
    asyncio.get_event_loop().run_forever()




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
