import os
os.environ['UBIQUITY_VERBOSE'] = '1'

import time

import asyncio
from ubiquity import Shoebox
from ubiquity.tunnel.websocket import WebSocketClientTunnel


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


if __name__ == '__main__':

    sbox = Shoebox('general2')
    tunnel = WebSocketClientTunnel('localhost')
    sbox.attach(tunnel)

    print('Spinning the event_loop')
    if run_from_ipython():
        import threading
        t = threading.Thread(target=asyncio.get_event_loop().run_forever)
        t.start()
    else:
        asyncio.get_event_loop().run_forever()



