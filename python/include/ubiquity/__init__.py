import os as __os
import logging as __logging
from .shoebox import Shoebox

__verbose_logging = 'UBIQUITY_VERBOSE' in __os.environ and bool(__os.environ['UBIQUITY_VERBOSE'])

__logging.basicConfig()
logger = __logging.getLogger('ubiquity')
logger.setLevel(__logging.DEBUG if __verbose_logging else __logging.INFO)
