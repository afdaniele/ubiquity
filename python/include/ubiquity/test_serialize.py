from ubiquity import Shoebox


if __name__ == '__main__':
    import json
    from goprocam import GoProCamera
    from types import SimpleNamespace

    goproCamera = GoProCamera.GoPro()

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

    sbox.add('sn', a)
    sbox.add('gopro', goproCamera)

    json.dump(
        sbox.serialize(),
        open('./../../test.quark', 'w'),
        indent=4,
        sort_keys=False
    )
