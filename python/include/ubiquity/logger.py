import logging

dir(logging)
logging.basicConfig()
_ulogger = logging.getLogger('ubiquity')
_ulogger.setLevel(logging.DEBUG)


def get_logger():
    return _ulogger
