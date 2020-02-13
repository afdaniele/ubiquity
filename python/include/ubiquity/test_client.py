import os

os.environ['UBIQUITY_VERBOSE'] = '1'

from ubiquity import Shoebox
from ubiquity.tunnel.websocket import WebSocketClientTunnel


if __name__ == '__main__':

    sbox = Shoebox('general2')

    tunnel = WebSocketClientTunnel('localhost')

    sbox.attach(tunnel)
