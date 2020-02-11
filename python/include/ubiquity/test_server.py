import asyncio
from ubiquity import Shoebox
from ubiquity.tunnel.websocket import WebSocketServerTunnel


def run_from_ipython():
    try:
        # noinspection PyStatementEffect
        __IPYTHON__
        return True
    except NameError:
        return False


if __name__ == '__main__':
    import json
    from goprocam import GoProCamera
    from types import SimpleNamespace

    # goproCamera = GoProCamera.GoPro()

    def fcn(a, b: str, c: int, *args, **kwargs) -> int:
        return 1

    a = SimpleNamespace(
        a=5,
        b=None,
        c={},
        d={'asd': 74},
        e=[],
        f=[1, 2],
        g=lambda d: [],
        h=fcn
    )

    sbox = Shoebox('general')
    tunnel = WebSocketServerTunnel()

    sbox.attach(tunnel)

    sbox.add('sn', a)
    # sbox.add('gopro', goproCamera)

    print('Spinning the event_loop')
    if run_from_ipython():
        import threading

        t = threading.Thread(target=asyncio.get_event_loop().run_forever)
        t.start()
    else:
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
