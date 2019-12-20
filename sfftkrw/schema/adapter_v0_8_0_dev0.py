# -*- coding: utf-8 -*-

import importlib

from .base import SFFType, SFFAttribute, SFFListType, SFFTypeError, SFFIndexType

from .. import EMDB_SFF_VERSION

# dynamically import the latest schema generateDS API
_emdb_sff_name = 'sfftkrw.schema.{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
_sff = importlib.import_module(_emdb_sff_name)

class SFFRGBA(SFFType):
    """Colours"""
    gds_type = _sff.rgba_type
