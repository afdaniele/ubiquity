import json
from ubiquity import Shoebox


if __name__ == '__main__':
    data = json.load(open('./../../test.quark', 'r'))
    sb = Shoebox.deserialize(data)
