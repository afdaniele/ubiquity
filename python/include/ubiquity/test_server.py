import os

os.environ['UBIQUITY_VERBOSE'] = '1'

from ubiquity import Shoebox
from ubiquity.tunnel.websocket import WebSocketServerTunnel


if __name__ == '__main__':
    # from goprocam import GoProCamera
    from types import SimpleNamespace

    # goproCamera = GoProCamera.GoPro()

    def fcn(a, b: str, c: int, *args, **kwargs) -> int:
        return 1

    def sum(a, b, c):
        return a + b + c

    def j():
        return SimpleNamespace(a=22)

    def n():
        return None

    def k(*args):
        return 0

    a = SimpleNamespace(
        a=5,
        b=None,
        c=set(),
        d={'asd': 74},
        e=[],
        f=[1, 2, [4, 5, [8, SimpleNamespace(a=22)], SimpleNamespace(k1=1, k2=3)]],
        g=lambda d: d,
        h=fcn,
        j=j,
        k=k,
        n=n,
        sum=sum,
        s=SimpleNamespace(a=22),
        chain=SimpleNamespace(
            l1=SimpleNamespace(
                l2=SimpleNamespace(
                    l3=SimpleNamespace(
                        value=4,
                        l4=SimpleNamespace(
                            value=5
                        )
                    )
                )
            )
        )
    )

    sbox = Shoebox('general')

    tunnel = WebSocketServerTunnel()

    sbox.attach(tunnel)

    sbox.add('sn', a)

    # sbox.add('gopro', goproCamera)


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
