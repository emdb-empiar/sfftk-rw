# -*- coding: utf-8 -*-
import importlib
from . import EMDB_SFF_VERSION

# load the adapter modules contents here
adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_'),
)
adapter = importlib.import_module(adapter_name)

# now add the classes to sfftkrw namespace
globals().update({g: getattr(adapter, g) for g in dir(adapter) if g.startswith('SFF')})

# remove the adapter namespace
del adapter_name
del adapter
