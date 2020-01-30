# -*- coding: utf-8 -*-
import importlib
import os

BASE_DIR = os.path.dirname(__file__)
VALID_EXTENSIONS = ['sff', 'xml', 'hff', 'h5', 'hdf5', 'json']

SFFTKRW_VERSION = 'v0.5.2.dev1'
EMDB_SFF_VERSION = 'v0.8.0.dev1'
# in reverse order; add newer versions on top
SUPPORTED_EMDB_SFF_VERSIONS = [
    'v0.8.0.dev1',
    'v0.7.0.dev0',
]

SFFTKRW_ENTRY_POINT = 'sff-rw'

# load the adapter modules contents here
adapter_name = 'sfftkrw.schema.adapter_{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_'),
)
adapter = importlib.import_module(adapter_name)
# now add the classes to sfftkrw namespace
globals().update({g: getattr(adapter, g) for g in dir(adapter) if g.startswith('SFF')})
# remove the adapter namespace
del adapter_name
del adapter
