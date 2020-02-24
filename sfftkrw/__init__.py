# -*- coding: utf-8 -*-
import os
import importlib
from .conf import SFFTKRW_VERSION, SFFTKRW_ENTRY_POINT

BASE_DIR = os.path.dirname(__file__)

VALID_EXTENSIONS = ['sff', 'xml', 'hff', 'h5', 'hdf5', 'json']
EMDB_SFF_VERSION = '0.8.0.dev1'

# in reverse order; add newer versions on top
SUPPORTED_EMDB_SFF_VERSIONS = [
    '0.8.0.dev1',
    '0.7.0.dev0',
]

# we try because otherwise we invoke modules with imports
# during installation the modules to be imported do not exist!
try:
    # load the adapter modules contents here
    adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
        schema_version=EMDB_SFF_VERSION.replace('.', '_'),
    )
    adapter = importlib.import_module(adapter_name)

    # now add the classes to sfftkrw namespace
    globals().update({g: getattr(adapter, g) for g in dir(adapter) if g.startswith('SFF')})
    gds_api_name = 'sfftkrw.schema.v{schema_version}'.format(
        schema_version=EMDB_SFF_VERSION.replace('.', '_')
    )
    gds_api = importlib.import_module(gds_api_name)
    # add the corresponding generateDS API
    globals().update({u'gds_api': gds_api})

    # remove the adapter namespace
    del adapter_name
    del adapter

    # gds_api
    del gds_api_name
except ImportError:
    import warnings

    warnings.warn("required packages not found. Please ignore if you are installing. "
                  "Otherwise please install six, h5py, numpy, RandomWords and lxml")
