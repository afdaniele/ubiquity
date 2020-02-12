import json
from ubiquity import Shoebox

from ubiquity.serialization.wave import deserialize_wave
from google.protobuf.text_format import Parse

if __name__ == '__main__':
    # data = json.load(open('./../../test.quark', 'r'))

    # Write the new address book back to disk.
    f = open('./../../test.quark', 'rt')

    Parse(f.read())
    f.close()

    sb = Shoebox.deserialize(data)
