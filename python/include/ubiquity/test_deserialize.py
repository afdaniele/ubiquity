import os

os.environ['UBIQUITY_VERBOSE'] = '1'


from ubiquity.serialization.wave import deserialize_wave
from google.protobuf.text_format import Parse, MessageToString

from ubiquity.serialization.Wave_pb2 import WavePB

if __name__ == '__main__':

    # Write the new address book back to disk.
    f = open('./../../test.quark', 'rt')

    wave_pb = WavePB()
    Parse(f.read(), wave_pb)
    f.close()

    # print(MessageToString(wave_pb))

    sb = deserialize_wave(wave_pb).shoebox
