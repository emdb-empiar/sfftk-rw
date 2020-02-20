# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(__file__)

VALID_EXTENSIONS = ['sff', 'xml', 'hff', 'h5', 'hdf5', 'json']
EMDB_SFF_VERSION = '0.8.0.dev1'

# in reverse order; add newer versions on top
SUPPORTED_EMDB_SFF_VERSIONS = [
    '0.8.0.dev1',
    '0.7.0.dev0',
]
SFFTKRW_VERSION = 'v0.6.0.dev0'
SFFTKRW_ENTRY_POINT = 'sff'
