# -*- coding: utf-8 -*-
"""
adapter_v0_8_0_dev1
=======================
"""
from __future__ import print_function

import base64
import collections
import json
import numbers
import os
import random
import re
import struct
import sys
import zlib

import h5py
import numpy

from . import FORMAT_CHARS, ENDIANNESS
from . import v0_8_0_dev1 as _sff

# ensure that we can read/write encoded data
_sff.ExternalEncoding = u"utf-8"

from .base import SFFType, SFFIndexType, SFFAttribute, SFFListType, SFFTypeError, _assert_or_raise
from ..core import _str, _encode, _bytes, _decode, _dict, _classic_dict
from ..core.print_tools import print_date
from ..core.utils import get_unique_id

_volume = collections.namedtuple(
    u'volume', [u'rows', u'cols', u'sections']
)


class SFFRGBA(SFFType):
    """Colours"""
    gds_type = _sff.rgba_type
    gds_tag_name = u'colour'
    repr_string = u"SFFRGBA(red={}, green={}, blue={}, alpha={})"
    repr_args = (u'red', u'green', u'blue', u'alpha')
    eq_attrs = [u'red', u'green', u'blue', u'alpha']

    # attributes
    red = SFFAttribute(u'red', required=True, help=u"red channel")
    green = SFFAttribute(u'green', required=True, help=u"green channel")
    blue = SFFAttribute(u'blue', required=True, help=u"blue channel")
    alpha = SFFAttribute(u'alpha', default=1.0, help=u"alpha (opacity) channel")

    def __init__(self, random_colour=False, **kwargs):
        """
        Initialise a new `SFFRGBA` object with/without `random_colour`
        :param bool random_colour: set a random colour value
        """
        super(SFFRGBA, self).__init__(**kwargs)
        if random_colour:
            self.value = random.random(), random.random(), random.random()

    @property
    def value(self):
        return self.red, self.green, self.blue, self.alpha

    @value.setter
    def value(self, c):
        if len(c) == 3:
            self.red, self.green, self.blue = c
        elif len(c) == 4:
            self.red, self.green, self.blue, self.alpha = c

    def _boolean_test(self):
        if self.red is None or self.green is None or self.blue is None or self.alpha is None:
            return False
        else:
            return True

    if sys.version_info[0] > 2:
        def __bool__(self):
            return self._boolean_test()
    else:
        def __nonzero__(self):
            return self._boolean_test()

    def as_hff(self, parent_group, name=u"colour", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        parent_group[name] = self.value
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'colour', args=None):
        """Return an SFFType object given an HDF5 object"""
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        obj.value = parent_group[name][()]
        return obj

    def as_json(self, args=None):
        """Export as JSON"""
        return self.value

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        obj.value = data
        return obj


class SFFExternalReference(SFFIndexType):
    gds_type = _sff.external_reference_type
    gds_tag_name = u'ref'
    repr_string = u"SFFExternalReference(id={}, resource={}, url={}, accession={}, label={}, description={})"
    repr_args = (u'id', u'resource', u'url', u'accession', u'label', u'description')
    ref_id = 0
    index_attr = u'ref_id'
    eq_attrs = [u'resource', u'url', u'accession', u'label', u'description']

    # attributes
    id = SFFAttribute(u'id', help=u"this external reference's ID")
    resource = SFFAttribute(u'resource', required=True, help=u"the ontology/archive name")
    url = SFFAttribute(u'url', required=True,
                       help=u"a URL/IRI where data for this external reference may be obtained")
    accession = SFFAttribute(u'accession', required=True, help=u"the accession for this external reference")
    label = SFFAttribute(u'label', help=u"a short description of this external reference")
    description = SFFAttribute(u'description', help=u"a long description of this external reference")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u"id": int(self.id),
            u"resource": self.resource,
            u"url": self.url,
            u"accession": self.accession,
            u"label": self.label,
            u"description": self.description,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'resource' in data:
            obj.resource = data[u'resource']
        if u'url' in data:
            obj.url = data[u'url']
        if u'accession' in data:
            obj.accession = data[u'accession']
        if u'label' in data:
            obj.label = data[u'label']
        if u'description' in data:
            obj.description = data[u'description']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        # first check if we have an ID; if we don't have one then get a globally unique one
        if self.id is None:
            self.id = get_unique_id()
        # now set the name of the group to the id; it's a string of the numerical id
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        # then create the group
        group = parent_group.create_group(name)
        # we can do this because we can guarantee that the id exists
        group[u'id'] = self.id
        if self.resource:
            group[u'resource'] = self.resource
        if self.url:
            group[u'url'] = self.url
        if self.accession:
            group[u'accession'] = self.accession
        if self.label:
            group[u'label'] = self.label
        if self.description:
            group[u'description'] = self.description
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[parent_group.name]
        obj = cls(new_obj=False)
        if u'id' in group:
            obj.id = group[u'id'][()]
        if u'resource' in group:
            obj.resource = group[u'resource'][()]
        if u'url' in group:
            obj.url = group[u'url'][()]
        if u'accession' in group:
            obj.accession = group[u'accession'][()]
        if u'label' in group:
            obj.label = group[u'label'][()]
        if u'description' in group:
            obj.description = group[u'description'][()]
        return obj


# todo: super SFFExternalReferenceList and SFFGlobalExternalReferenceList
# noinspection PyUnresolvedReferences
class SFFExternalReferenceList(SFFListType):
    """Container for external references"""
    gds_type = _sff.external_referencesType
    gds_tag_name = u'external_references'
    repr_string = u"SFFExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def as_json(self, args=None):
        es = list()
        for extref in self:
            es.append(extref.as_json(args=args))
        return es

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for extref in data:
            obj.append(SFFExternalReference.from_json(extref, args=args))
        return obj

    def as_hff(self, parent_group, name=u'external_references', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for extref in self:
            group = extref.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'external_references', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[name]
        obj = cls(new_obj=False)
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFExternalReference.from_hff(subgroup, args=args))
        return obj


# noinspection PyUnresolvedReferences
class SFFGlobalExternalReferenceList(SFFListType):
    """Container for global external references"""
    gds_type = _sff.global_external_referencesType
    gds_tag_name = u'global_external_references'
    repr_string = u"SFFGlobalExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def as_json(self, args=None):
        ge = list()
        for extref in self:
            ge.append(extref.as_json(args=args))
        return ge

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for extref in data:
            obj.append(SFFExternalReference.from_json(extref, args=args))
        return obj

    def as_hff(self, parent_group, name=u'global_external_references', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for extref in self:
            group = extref.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'global_external_references', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[name]
        obj = cls(new_obj=False)
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFExternalReference.from_hff(subgroup, args=args))
        return obj


class SFFBiologicalAnnotation(SFFType):
    """Biological annotation"""
    gds_type = _sff.biological_annotationType
    gds_tag_name = u'biological_annotation'
    repr_string = u"""SFFBiologicalAnnotation(name={}, description={}, number_of_instances={}, external_references={})"""
    repr_args = (u'name', u'description', u'number_of_instances', u'external_references')
    eq_attrs = [u'name', u'description', u'external_references', u'number_of_instances']

    # attributes
    name = SFFAttribute(u'name', help=u"the name of this segment")
    description = SFFAttribute(u'description', help=u"a brief description for this segment")
    external_references = SFFAttribute(
        u'external_references',
        sff_type=SFFExternalReferenceList,
        help=u"the set of external references"
    )
    number_of_instances = SFFAttribute(u'number_of_instances', default=1,
                                       help=u"the number of instances of this segment")

    # methods
    def _boolean_test(self):
        if not self.description and not self.external_references and not self.number_of_instances:
            return False
        else:
            return True

    if sys.version_info[0] > 2:
        def __bool__(self):
            return self._boolean_test()
    else:
        def __nonzero__(self):
            return self._boolean_test()

    @property
    def num_external_references(self):
        if self.external_references:
            return len(self.external_references)
        else:
            return 0

    def as_json(self, args=None):
        return {
            u'name': self.name,
            u'description': self.description,
            u'number_of_instances': self.number_of_instances,
            u'external_references': self.external_references.as_json(args=args),
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'name' in data:
            obj.name = data[u'name']
        if u'description' in data:
            obj.description = data[u'description']
        if u'number_of_instances' in data:
            obj.number_of_instances = data[u'number_of_instances']
        if u'external_references' in data:
            obj.external_references = SFFExternalReferenceList.from_json(data[u'external_references'], args=args)
        return obj

    def as_hff(self, parent_group, name=u'biological_annotation', args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        # description and nubmerOfInstances as datasets
        if self.name:
            group[u'name'] = self.name
        if self.description:
            group[u'description'] = self.description
        if isinstance(self.number_of_instances, numbers.Integral):
            group[u'number_of_instances'] = self.number_of_instances if self.number_of_instances > 0 else 1
        else:
            group[u'number_of_instances'] = 1
        if self.external_references:
            _ = self.external_references.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'biological_annotation', args=None):
        """Return an SFFType object given an HDF5 object"""
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[name]
        obj = cls(new_obj=False)
        if u'name' in group:
            obj.name = _decode(group[u'name'][()], u'utf-8')
        else:
            obj.name = None
        if u'description' in group:
            obj.description = _decode(group[u'description'][()], u'utf-8')
        if u'number_of_instances' in group:
            obj.number_of_instances = int(group[u'number_of_instances'][()])
        if u"external_references" in group:
            obj.external_references = SFFExternalReferenceList.from_hff(group, args=args)
        return obj


class SFFThreeDVolume(SFFType):
    """Class representing segments described using a 3D volume"""
    gds_type = _sff.three_d_volume_type
    gds_tag_name = u'three_d_volume'
    repr_string = u"SFFThreeDVolume(lattice_id={}, value={}, transform_id={})"
    repr_args = (u'lattice_id', u'value', u'transform_id')
    eq_attrs = [u'lattice_id', u'value', u'transform_id']

    # attributes
    lattice_id = SFFAttribute(u'lattice_id', required=True,
                              help=u"the ID of the lattice that has the data for this 3D volume")
    value = SFFAttribute(u'value', required=True, help=u"the voxel values associated with this 3D volume")
    transform_id = SFFAttribute(u'transform_id', help=u"a transform applied to this 3D volume [optional]")

    def as_json(self, args=None):
        return {
            u'lattice_id': int(self.lattice_id) if self.lattice_id is not None else None,
            u'value': float(self.value) if self.value is not None else None,
            u'transform_id': int(self.transform_id) if self.transform_id is not None else None,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'lattice_id' in data:
            obj.lattice_id = data[u'lattice_id']
        if u'value' in data:
            obj.value = data[u'value']
        if u'transform_id' in data:
            obj.transform_id = data[u'transform_id']
        return obj

    def as_hff(self, parent_group, name=u'three_d_volume', args=None):
        """Return an SFFType object given an HDF5 object"""
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        if self.lattice_id is not None:
            group[u'lattice_id'] = self.lattice_id
        if self.value is not None:
            group[u'value'] = self.value
        if self.transform_id is not None:
            group[u'transform_id'] = self.transform_id
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'three_d_volume', args=None):
        """Return an SFFType object given an HDF5 object"""
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[name]
        obj = cls(new_obj=False)
        if u'lattice_id' in group:
            obj.lattice_id = group[u'lattice_id'][()]
        if u'value' in group:
            obj.value = group[u'value'][()]
        if u'transform_id' in group:
            obj.transform_id = group[u'transform_id'][()]
        return obj


class SFFVolume(SFFType):
    """Class for represention 3-space dimension"""
    # attributes
    rows = SFFAttribute(u'rows', required=True, help=u"number of rows")
    cols = SFFAttribute(u'cols', required=True, help=u"number of columns")
    sections = SFFAttribute(u'sections', required=True,
                            help=u"number of sections (sets of congruent row-column collections)")
    eq_attrs = [u'rows', u'cols', u'sections']

    @property
    def value(self):
        return self.cols, self.rows, self.sections

    @value.setter
    def value(self, value):
        if len(value) == 3:
            self.cols, self.rows, self.sections = value
        else:
            raise SFFTypeError(value, u"Iterable", message=u"should be of length 3")

    def as_json(self, args=None):
        return {
            u'rows': int(self.rows) if self.rows is not None else None,
            u'cols': int(self.cols) if self.cols is not None else None,
            u'sections': int(self.sections) if self.sections is not None else None,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'rows' in data:
            obj.rows = data[u'rows']
        if u'cols' in data:
            obj.cols = data[u'cols']
        if u'sections' in data:
            obj.sections = data[u'sections']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        _assert_or_raise(name, _str)  # will be set in the children
        group = parent_group.create_group(name)
        if self.rows is not None:
            group[u'rows'] = self.rows
        if self.cols is not None:
            group[u'cols'] = self.cols
        if self.sections is not None:
            group[u'sections'] = self.sections
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        _assert_or_raise(name, _str)  # will be set in the children
        obj = cls(new_obj=False)
        group = parent_group[name]
        if u'rows' in group:
            obj.rows = group[u'rows'][()]
        if u'cols' in group:
            obj.cols = group[u'cols'][()]
        if u'sections' in group:
            obj.sections = group[u'sections'][()]
        return obj


class SFFVolumeStructure(SFFVolume):
    gds_type = _sff.volume_structure_type
    gds_tag_name = u'size'
    repr_string = u"SFFVolumeStructure(cols={}, rows={},sections={})"
    repr_args = (u'cols', u'rows', u'sections')

    @property
    def voxel_count(self):
        """The number of voxels in this volume"""
        return self.cols * self.rows * self.sections

    def as_hff(self, parent_group, name=u'size', args=None):
        return super(SFFVolumeStructure, self).as_hff(parent_group, name=name, args=args)

    @classmethod
    def from_hff(cls, parent_group, name=u'size', args=None):
        return super(SFFVolumeStructure, cls).from_hff(parent_group, name=name, args=args)


class SFFVolumeIndex(SFFVolume):
    """Class representing volume indices"""
    # todo: implement an iterator to increment indices correctly
    gds_type = _sff.volume_index_type
    gds_tag_name = u'start'
    repr_string = u"SFFVolumeIndex(rows={}, cols={}, sections={})"
    repr_args = (u'rows', u'cols', u'sections')

    def as_hff(self, parent_group, name=u'start', args=None):
        return super(SFFVolumeIndex, self).as_hff(parent_group, name=name, args=args)

    @classmethod
    def from_hff(cls, parent_group, name=u'start', args=None):
        return super(SFFVolumeIndex, cls).from_hff(parent_group, name=name, args=args)


class SFFLattice(SFFIndexType):
    """Class representing 3D """
    gds_type = _sff.lattice_type
    gds_tag_name = u'lattice'
    repr_string = u"SFFLattice(id={}, mode={}, endianness={}, size={}, start={}, data={})"
    repr_args = (u'id', u'mode', u'endianness', u'size', u'start', u'data[:100]')
    lattice_id = 0
    index_attr = u'lattice_id'
    eq_attrs = [u'mode', u'endianness', u'size', u'start', u'data']

    # attributes
    id = SFFAttribute(u'id', required=True, help=u"the ID for this lattice (referenced by 3D volumes)")
    mode = SFFAttribute(u'mode', required=True, default=u'uint32',
                        help=u"type of data for each voxel; valid values are: int8, uint8, int16, uint16, int32, "
                             u"uint32, int64, uint64, float32, float64")
    endianness = SFFAttribute(u'endianness', required=True, default=u'little',
                              help=u"endianness; either 'little' (default) or 'big'")
    size = SFFAttribute(u'size', sff_type=SFFVolumeStructure, required=True,
                        help=u"size of the lattice described using a "
                             ":py:class:`sfftkrw.schema.adapter.SFFVolumeStructure` object")
    start = SFFAttribute(u'start', sff_type=SFFVolumeIndex, default=SFFVolumeIndex(rows=0, cols=0, sections=0),
                         required=True,
                         help=u"starting index of the lattices described using a"
                              ":py:class:`sfftkrw.schema.adapter.SFFVolumeIndex` object")
    data = SFFAttribute(u'data', required=True,
                        help=u"data provided by a :py:class:`numpy.ndarray`, byte-sequence or unicode string; "
                             u"the dimensions should correspond with those specified in the 'size' attribute")

    def __init__(self, **kwargs):
        if u'data' in kwargs:
            if isinstance(kwargs[u'data'], numpy.ndarray):
                self._data = kwargs[u'data']
                kwargs[u'data'] = SFFLattice._encode(kwargs[u'data'], **kwargs)
            elif isinstance(kwargs[u'data'], (_bytes, _str)):
                self._data = SFFLattice._decode(kwargs[u'data'], **kwargs)
            # elif isinstance(kwargs[u'data'], _str):
            #     _data = _encode(kwargs[u'data'], u'ASCII')
            #     self._data = SFFLattice._decode(_data, **kwargs)
            #     kwargs[u'data'] = _data
            #     del _data
        super(SFFLattice, self).__init__(**kwargs)

    @classmethod
    def from_array(cls, data, size=None, mode=u'uint32', endianness=u'little',
                   start=SFFVolumeIndex(rows=0, cols=0, sections=0)):
        """Create a :py:class:`SFFLattice` object from a numpy array inferring size and assuming certain defaults

        :param data: the data as a :py:class:`numpy.ndarray` object
        :type data: :py:class:`numpy.ndarray`
        :param size: the size of the lattice as a :py:class:`SFFVolumeStructure` object
        :type size: :py:class:`SFFVolumeStructure`
        :param start: the values of the corner voxel
        :type start: :py:class:`SFFVolumeIndex`
        :param mode: the size of each voxel; valid values are: `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64``float32`, `float64`
        :type mode: bytes or str or unicode
        :param endianness: byte ordering: ``little`` (default) or ``big``
        :type endianness: bytes or str or unicode
        :return: a :py:class:`SFFLattice` object
        :rtype: :py:class:`SFFLattice`
        """
        # assertions
        r, c, s = data.shape
        encoded_data = SFFLattice._encode(data, mode=mode, endianness=endianness)
        if size is None:
            size = SFFVolumeStructure(rows=r, cols=c, sections=s)
        obj = cls(
            mode=mode,
            endianness=endianness,
            size=size,
            start=start,
            data=encoded_data
        )
        obj._data = data
        return obj

    @property
    def data_array(self):
        """The data as a :py:class:`numpy.ndarray`"""
        if not hasattr(self, u'_data'):
            # make numpy from bytes
            self._data = SFFLattice._decode(
                self.data,
                size=self.size,
                mode=self.mode,
                endianness=self.endianness,
                start=self.start
            )
        return self._data

    @classmethod
    def from_bytes(cls, byte_seq, size, mode=u'uint32', endianness=u'little',
                   start=SFFVolumeIndex(rows=0, cols=0, sections=0)):
        """Create a :py:class:`SFFLattice` object using a bytes object

        :param byte_seq: the data as a base64-encoded, zipped sequence; can be bytes or unicode
        :type byte_seq: bytes or unicode
        :param size: the size of the lattice as a :py:class:`SFFVolumeStructure` object
        :type size: :py:class:`SFFVolumeStructure`
        :param start: the values of the corner voxel
        :type start: :py:class:`SFFVolumeIndex`
        :param mode: the size of each voxel; valid values are: `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64``float32`, `float64`
        :type mode: bytes or str or unicode
        :param endianness: byte ordering: ``little`` (default) or ``big``
        :type endianness: bytes or str or unicode
        :return: a :py:class:`SFFLattice` object
        :rtype: :py:class:`SFFLattice`
        """
        try:
            assert isinstance(size, SFFVolumeStructure)
        except AssertionError:
            raise SFFTypeError(size, SFFVolumeStructure)
        if isinstance(byte_seq, _str):  # if unicode convert to bytes
            _encode(byte_seq, u'ASCII')
        obj = cls(
            mode=mode,
            endianness=endianness,
            size=size,
            start=start,
            data=byte_seq,
        )
        return obj

    @staticmethod
    def _encode(array, mode=u'uint32', endianness=u'little', **kwargs):
        """Encode a :py:class:`numpy.ndarray` as a base64-encoded, zipped byte sequence

        :param array: a :py:class:`numpy.ndarray` array
        :type array: :py:class:`numpy.ndarray`
        :return str: the corresponding zipped object as a string
        """
        r, c, s = array.shape
        voxel_count = r * c * s
        format_string = "{}{}{}".format(ENDIANNESS[endianness], voxel_count, FORMAT_CHARS[mode])
        try:
            binpack = struct.pack(format_string, *array.flat)
            del array
            binzip = zlib.compress(binpack)
            del binpack
            bin64 = base64.b64encode(binzip)
            del binzip
        except MemoryError:
            print_date("Insufficient memory. Please run with more memory.")
            bin64 = ""
        return _decode(bin64, u'utf-8')

    @staticmethod
    def _decode(bin64, size, mode=u'uint32', endianness=u'little', **kwargs):
        """Decode a base64-encoded, zipped byte sequence to a numpy array

        :param bin64: the base64-encoded zipped data
        :type bin64: bytes or unicode string
        :param size: the size of the expected volume
        :type size: :py:class:`SFFVolumeStructure`
        :return: a :py:class:`numpy.ndarray` object
        :rtype: :py:class:`numpy.ndarray`
        """
        if isinstance(bin64, _str):
            binzip = base64.b64decode(_encode(bin64, u'utf-8'))
        else:
            binzip = base64.b64decode(bin64)
        del bin64
        binpack = zlib.decompress(binzip)
        del binzip
        _count = size.voxel_count
        _len = len(binpack)
        endianness_ = ENDIANNESS[endianness]
        format_char = FORMAT_CHARS[mode]
        bindata = struct.unpack("{}{}{}".format(endianness_, _count, format_char), binpack)
        del binpack
        data = numpy.array(bindata).reshape(*size.value[::-1])
        del bindata
        return data

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'mode': self.mode,
            u'endianness': self.endianness,
            u'size': self.size.as_json(args=args) if self.size is not None else None,
            u'start': self.start.as_json(args=args) if self.start is not None else None,
            u'data': self.data,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'mode' in data:
            obj.mode = data[u'mode']
        if u'endianness' in data:
            obj.endianness = data[u'endianness']
        if u'size' in data:
            if data[u'size'] is not None:
                obj.size = SFFVolumeStructure.from_json(data[u'size'], args=args)
            else:
                obj.size = None
        if u'start' in data:
            if data[u'start'] is not None:
                obj.start = SFFVolumeIndex.from_json(data[u'start'], args=args)
            else:
                obj.start = None
        if u'data' in data:  # lazy for numpy
            obj.data = data[u'data']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)  # use the string of the id as the name
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.mode:
            group[u'mode'] = self.mode
        if self.endianness:
            group[u'endianness'] = self.endianness
        if self.size:
            group = self.size.as_hff(group, args=args)
        if self.start:
            group = self.start.as_hff(group, args=args)
        if self.data:
            group[u'data'] = self.data
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'id' in group:
            obj.id = int(group[u'id'][()])
        if u'mode' in group:
            obj.mode = group[u'mode'][()]
        if u'endianness' in group:
            obj.endianness = group[u'endianness'][()]
        if u'size' in group:
            obj.size = SFFVolumeStructure.from_hff(group, args=args)
        if u'start' in group:
            obj.start = SFFVolumeIndex.from_hff(group, args=args)
        if u'data' in group:
            obj.data = group[u'data'][()]
        return obj


class SFFLatticeList(SFFListType):
    """A container for lattice objects"""
    gds_type = _sff.lattice_listType
    gds_tag_name = u'lattice_list'
    repr_string = u"SFFLatticeList({})"
    repr_args = (u"list()",)
    iter_attr = (u'lattice', SFFLattice)

    def as_json(self, args=None):
        llist = list()
        for lattice in self:
            llist.append(lattice.as_json(args=args))
        return llist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for lattice in data:
            obj.append(SFFLattice.from_json(lattice, args=args))
        return obj

    def as_hff(self, parent_group, name=u'lattice_list', args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for lattice in self:
            group = lattice.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'lattice_list', args=None):
        """Return an SFFType object given an HDF5 object"""
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFLattice.from_hff(subgroup, args=args))
        return obj


class SFFEncodedSequence(SFFType):
    """Abstract base class for `SFFVertices`, `SFFNormals` and `SFFTriangles`"""
    default_mode = u'float32'
    default_endianness = u'little'
    num_items_kwarg = None  # 'num_vertices' | 'num_normals' | 'num_triangles'
    """the name of the attribute with the size"""

    def __init__(self, **kwargs):
        if u'data' in kwargs:
            if isinstance(kwargs[u'data'], numpy.ndarray):
                # check that the dimensions are correct
                try:
                    assert kwargs[u'data'].shape[1] == 3  # x, y, z
                except AssertionError:
                    raise ValueError(u"data has invalid dimensions: {}; should be (n, 3)".format(kwargs[u'data'].shape))
                self._data = kwargs[u'data']
                kwargs['data'] = self._encode(kwargs[u'data'], **kwargs)
            elif isinstance(kwargs[u'data'], (_bytes, _str)):
                self._data = self._decode(kwargs[u'data'], **kwargs)
                # make sure the number of items is correct
                try:
                    assert self._data.shape[0] == kwargs.get(self.num_items_kwarg)
                except AssertionError:
                    raise ValueError(
                        u"mismatch in stated and retrieved number of items: {}/{}".format(
                            kwargs.get(self.num_items_kwarg),
                            self._data.shape[0]))
        super(SFFEncodedSequence, self).__init__(**kwargs)

    def __getitem__(self, item):
        return self.data_array[item]

    def __len__(self):
        return getattr(self, self.num_items_kwarg)

    @classmethod
    def from_array(cls, data, mode=None, endianness=None):
        """Create a :py:class:`SFFVertices` object from a numpy array inferring size and assuming certain defaults

        :param data: the data as a :py:class:`numpy.ndarray` object
        :type data: :py:class:`numpy.ndarray`
        :param mode: the size of each voxel; valid values are: `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64``float32`, `float64`
        :type mode: bytes or str or unicode
        :param endianness: byte ordering: ``little`` (default) or ``big``
        :type endianness: bytes or str or unicode
        :return: a :py:class:`SFFVertices` object
        :rtype: :py:class:`SFFVertices`
        """
        if mode is None:
            mode = cls.default_mode
        if endianness is None:
            endianness = cls.default_endianness
        # assertions
        encoded_data = SFFEncodedSequence._encode(data, mode=mode, endianness=endianness)
        kwargs = {
            cls.num_items_kwarg: data.shape[0],
            'mode': mode,
            'endianness': endianness,
            'data': encoded_data,
        }
        obj = cls(**kwargs)
        obj._data = data
        return obj

    @classmethod
    def from_bytes(cls, byte_seq, num_items, mode=None, endianness=None):
        """Create a :py:class:`SFFVertices` object using a bytes object

        :param byte_seq: the data as a base64-encoded sequence; can be bytes or unicode
        :type byte_seq: bytes or unicode
        :param int num_vertices: the number of vertices contained (for validation)
        :param mode: the size of each voxel; valid values are: `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64``float32`, `float64`
        :type mode: bytes or str or unicode
        :param endianness: byte ordering: ``little`` (default) or ``big``
        :type endianness: bytes or str or unicode
        :return: a :py:class:`SFFVertices` object
        :rtype: :py:class:`SFFVertices`
        """
        if mode is None:
            mode = cls.default_mode
        if endianness is None:
            endianness = cls.default_endianness
        # if isinstance(byte_seq, _str):  # if unicode convert to bytes
        #     byte_seq = _encode(byte_seq, u'ASCII')
        kwargs = {
            cls.num_items_kwarg: num_items,
            'mode': mode,
            'endianness': endianness,
            'data': byte_seq,
        }
        obj = cls(**kwargs)
        return obj

    @property
    def data_array(self):
        """The data as a :py:class:`numpy.ndarray`"""
        if not hasattr(self, u'_data'):
            # make numpy from bytes
            self._data = SFFEncodedSequence._decode(
                self.data,
                mode=self.mode,
                endianness=self.endianness,
            )
        return self._data

    @staticmethod
    def _encode(array, mode=None, endianness=None, **kwargs):
        """Encode a :py:class:`numpy.ndarray` as a base64-encoded byte sequence

        :param array: a :py:class:`numpy.ndarray` array
        :type array: :py:class:`numpy.ndarray`
        :param str mode: the data type
        :param str endianness: the byte orientation
        :return str: the corresponding encoded sequence
        """
        if mode is None:
            mode = SFFEncodedSequence.default_mode
        if endianness is None:
            endianness = SFFEncodedSequence.default_endianness
        array_in_mode_and_endianness = array.astype(
            '{}{}'.format(ENDIANNESS[endianness], FORMAT_CHARS[mode]))  # cast to required mode
        return _decode(base64.b64encode(array_in_mode_and_endianness.tobytes()), u'utf-8')

    @staticmethod
    def _decode(bin64, mode=None, endianness=None, **kwargs):
        """Decode a base64-encoded byte sequence to a numpy array

        :param bin64: the base64-encoded byte sequence
        :type bin64: bytes or unicode
        :param str mode: the data type
        :param str endianness: the byte orientation
        :return: a :py:class:`numpy.ndarray` object
        :rtype: :py:class:`numpy.ndarray`
        """
        if mode is None:
            mode = SFFEncodedSequence.default_mode
        if endianness is None:
            endianness = SFFEncodedSequence.default_endianness
        if isinstance(bin64, _str):
            binpack = base64.b64decode(_encode(bin64, u'utf-8'))
        else:
            binpack = base64.b64decode(bin64)
        dt = numpy.dtype('{}{}'.format(ENDIANNESS[endianness], FORMAT_CHARS[mode]))
        unpacked = numpy.frombuffer(binpack, dtype=dt)
        return unpacked.reshape(-1, 3)  # leave first value to be auto-filled

    def as_json(self, args=None):
        return {
            self.num_items_kwarg: int(getattr(self, self.num_items_kwarg)),
            u'mode': self.mode,
            u'endianness': self.endianness,
            u'data': self.data
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if cls.num_items_kwarg in data:
            setattr(obj, cls.num_items_kwarg, data[cls.num_items_kwarg])
        if u'mode' in data:
            obj.mode = data[u'mode']
        if u'endianness' in data:
            obj.endianness = data[u'endianness']
        if u'data' in data:
            obj.data = data[u'data']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        num_items = getattr(self, self.num_items_kwarg, None)
        if num_items is not None:
            group[self.num_items_kwarg] = int(num_items)
        if self.mode:
            group[u'mode'] = self.mode
        if self.endianness:
            group[u'endianness'] = self.endianness
        if self.data:
            group[u'data'] = self.data
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        _assert_or_raise(name, _str)
        obj = cls(new_obj=False)
        group = parent_group[name]
        if cls.num_items_kwarg in group:
            setattr(obj, cls.num_items_kwarg, int(group[cls.num_items_kwarg][()]))
        if u'mode' in group:
            obj.mode = group[u'mode'][()]
        if u'endianness' in group:
            obj.endianness = group[u'endianness'][()]
        if u'data' in group:
            obj.data = group[u'data'][()]
        return obj


class SFFVertices(SFFEncodedSequence):
    """Vertices: neither a list nor an index type but is encoded

    Suggests the need for an `SFFCodedType` which has encoded data
    with `_encode` and `_decode` services/methods.
    """
    gds_type = _sff.vertices_type
    gds_tag_name = u'vertices'
    repr_string = u"SFFVertices(num_vertices={}, mode={}, endianness={}, data={})"
    repr_args = (u'num_vertices', u'mode', u'endianness', u'data[:100]')
    num_items_kwarg = u'num_vertices'
    eq_attrs = [u'num_vertices', u'mode', u'endianness', u'data']

    # attributes
    num_vertices = SFFAttribute(u'num_vertices', required=True, help=u"the number of vertices contained")
    mode = SFFAttribute(u'mode', default=u"float32", help=u"data type; valid values are: int8, uint8, int16, uint16, "
                                                          u"int32, uint32, int64, uint64, float32, float64 [default: 'float32']")
    endianness = SFFAttribute(u'endianness', default=u"little", help=u"binary packing endianness [default: 'little']")
    data = SFFAttribute(u'data', required=True, help=u"base64-encoded packed binary data")

    def as_hff(self, parent_group, name=u'vertices', args=None):
        return super(SFFVertices, self).as_hff(parent_group, name=name, args=args)

    @classmethod
    def from_hff(cls, parent_group, name=u'vertices', args=None):
        return super(SFFVertices, cls).from_hff(parent_group, name=name, args=args)


class SFFNormals(SFFEncodedSequence):
    """Normals"""
    gds_type = _sff.normals_type
    gds_tag_name = u'normals'
    repr_string = u"SFFNormals(num_normals={}, mode={}, endianness={}, data={})"
    repr_args = (u'num_normals', u'mode', u'endianness', u'data[:100]')
    num_items_kwarg = u'num_normals'
    eq_attrs = [u'num_normals', u'mode', u'endianness', u'data']

    # attributes
    num_normals = SFFAttribute(u'num_normals', required=True, help=u"the number of normals contained")
    mode = SFFAttribute(u'mode', default=u"float32", help=u"data type; valid values are: int8, uint8, int16, uint16, "
                                                          u"int32, uint32, int64, uint64, float32, float64 [default: 'float32']")
    endianness = SFFAttribute(u'endianness', default=u"little", help=u"binary packing endianness [default: 'little']")
    data = SFFAttribute(u'data', required=True, help=u"base64-encoded packed binary data")

    def as_hff(self, parent_group, name=u'normals', args=None):
        return super(SFFNormals, self).as_hff(parent_group, name=name, args=args)

    @classmethod
    def from_hff(cls, parent_group, name=u'normals', args=None):
        return super(SFFNormals, cls).from_hff(parent_group, name=name, args=args)


class SFFTriangles(SFFEncodedSequence):
    """Triangles"""
    gds_type = _sff.triangles_type
    gds_tag_name = u'triangles'
    repr_string = u"SFFTriangles(num_triangles={}, mode={}, endianness={}, data={})"
    repr_args = (u'num_triangles', u'mode', u'endianness', u'data[:100]')
    default_mode = u'uint32'
    num_items_kwarg = u'num_triangles'
    eq_attrs = [u'num_triangles', u'mode', u'endianness', u'data']

    # attributes
    num_triangles = SFFAttribute(u'num_triangles', required=True, help=u"the number of triangles contained")
    mode = SFFAttribute(u'mode', default=u"uint32", help=u"data type; valid values are: int8, uint8, int16, uint16, "
                                                         u"int32, uint32, int64, uint64, float32, float64 [default: 'float32']")
    endianness = SFFAttribute(u'endianness', default=u"little", help=u"binary packing endianness [default: 'little']")
    data = SFFAttribute(u'data', required=True, help=u"base64-encoded packed binary data")

    def as_hff(self, parent_group, name=u'triangles', args=None):
        return super(SFFTriangles, self).as_hff(parent_group, name=name, args=args)

    @classmethod
    def from_hff(cls, parent_group, name=u'triangles', args=None):
        return super(SFFTriangles, cls).from_hff(parent_group, name=name, args=args)


class SFFMesh(SFFIndexType):
    """Single mesh"""
    gds_type = _sff.mesh_type
    gds_tag_name = u'mesh'
    repr_string = u"SFFMesh(id={}, vertices={}, normals={}, triangles={})"
    repr_args = (u'id', u'vertices', u'normals', u'triangles')
    mesh_id = 0
    index_attr = u'mesh_id'
    eq_attrs = [u'vertices', u'normals', u'triangles']

    # attributes
    id = SFFAttribute(u'id', help='the mesh ID')
    vertices = SFFAttribute(u'vertices', required=True, sff_type=SFFVertices, help="a list of vertices")
    normals = SFFAttribute(u'normals', sff_type=SFFNormals, help="a list of normals which correspond to vertices")
    triangles = SFFAttribute(u'triangles', required=True, sff_type=SFFTriangles,
                             help="a list of triangles; each triangle is represented by a trio of vertex indices")
    transform_id = SFFAttribute(u'transform_id', help=u"a transform applied to the mesh")

    def __init__(self, **kwargs):
        if 'normals' in kwargs:
            try:
                assert kwargs['vertices'].data_array.shape == kwargs['normals'].data_array.shape
            except AssertionError:
                raise ValueError("vertex list and normal list are of different lengths/dimensions")
        # check that the triangle list is valid
        # todo: devise better test for this
        # indexes = set(kwargs['triangles'].data_array.flatten().tolist())
        # try:
        #     assert (kwargs['vertices'].num_vertices - 1) in indexes
        # except AssertionError:
        #     raise ValueError("incompatible vertex and triangle lists")
        super(SFFMesh, self).__init__(**kwargs)

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'vertices': self.vertices.as_json(args=args),
            u'normals': self.normals.as_json(args=args) if self.normals is not None else None,
            u'triangles': self.triangles.as_json(args=args),
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'vertices' in data:
            obj.vertices = SFFVertices.from_json(data[u'vertices'], args=args)
        if u'normals' in data:  # because normals are optional
            if data[u'normals']:
                obj.normals = SFFNormals.from_json(data[u'normals'], args=args)
        if u'triangles' in data:
            obj.triangles = SFFTriangles.from_json(data[u'triangles'], args=args)
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        if self.id is None:
            self.id = get_unique_id()
        _assert_or_raise(parent_group, h5py.Group)
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.vertices:
            group = self.vertices.as_hff(group, args=args)
        if self.normals:
            group = self.normals.as_hff(group, args=args)
        if self.triangles:
            group = self.triangles.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'id' in group:
            obj.id = int(group[u'id'][()])
        if u'vertices' in group:
            obj.vertices = SFFVertices.from_hff(group, args=args)
        if u'normals' in group:
            obj.normals = SFFNormals.from_hff(group, args=args)
        if u'triangles' in group:
            obj.triangles = SFFTriangles.from_hff(group, args=args)
        return obj


class SFFMeshList(SFFListType):
    """Mesh list representation"""
    gds_type = _sff.mesh_listType
    gds_tag_name = u'mesh_list'
    repr_string = u"SFFMeshList({})"
    repr_args = (u'list()',)
    iter_attr = (u'mesh', SFFMesh)

    def as_json(self, args=None):
        mlist = list()
        for mesh in self:
            mlist.append(mesh.as_json(args=args))
        return mlist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for mesh in data:
            obj.append(SFFMesh.from_json(mesh, args=args))
        return obj

    def as_hff(self, parent_group, name=u'mesh_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for mesh in self:
            group = mesh.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'mesh_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        # since the names of the mesh groups are string versions of the mesh ids
        # when iterating they are sorted lexicographically
        # therefore we sort by int-casted names
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFMesh.from_hff(subgroup, args=args))
        return obj


class SFFShape(SFFIndexType):
    """Base shape class"""
    shape_id = 0
    index_attr = u'shape_id'
    index_in_super = True

    # attributes
    id = SFFAttribute(u'id', required=True, help=u"the ID of this shape")
    transform_id = SFFAttribute(u'transform_id', required=True,
                                help=u"the transform applied to this shape to position it in the space")
    attribute = SFFAttribute(u'attribute', help=u"extra attribute information e.g. 'FOM'")

    @classmethod
    def update_counter(cls, value):
        """Update the index for all subclasses sequentially for sibling classes

        This method works alongside the `index_in_super` class attribute.

        The superclass must specify this method to ensure correct sequencing of shared indices.
        """
        SFFShape.shape_id = value


class SFFCone(SFFShape):
    """Cone shape class"""
    gds_type = _sff.cone
    gds_tag_name = u"cone"
    repr_string = u"SFFCone(id={}, height={}, bottom_radius={}, transform_id={}, attribute={})"
    repr_args = (u'id', u'height', u'bottom_radius', u'transform_id', u'attribute')
    eq_attrs = [u'height', u'bottom_radius']

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cone height")
    bottom_radius = SFFAttribute(u'bottom_radius', required=True, help=u"cone bottom radius")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'shape': u'cone',
            u'height': self.height,
            u'bottom_radius': self.bottom_radius,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data, args=None):
        if u'shape' in data:
            if data[u'shape'] == u'cone':
                obj = cls(new_obj=False)
                if u'id' in data:
                    obj.id = data[u'id']
                if u'height' in data:
                    obj.height = data[u'height']
                if u'bottom_radius' in data:
                    obj.bottom_radius = data[u'bottom_radius']
                if u'transform_id' in data:
                    obj.transform_id = data[u'transform_id']
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cone".format(data[u'shape']))
        else:
            raise ValueError(u"missing 'shape' attribute")

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.height is not None:
            group[u'height'] = self.height
        if self.bottom_radius is not None:
            group[u'bottom_radius'] = self.bottom_radius
        if self.transform_id is not None:
            group[u'transform_id'] = self.transform_id
        group[u'shape'] = u'cone'
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'shape' in group:
            if group[u'shape'][()] == u'cone':
                if u'id' in group:
                    obj.id = group[u'id'][()]
                if u'height' in group:
                    obj.height = group[u'height'][()]
                if u'bottom_radius' in group:
                    obj.bottom_radius = group[u'bottom_radius'][()]
                if u'transform_id' in group:
                    obj.transform_id = group[u'transform_id'][()]
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cone".format(group[u'shape'][()]))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFCuboid(SFFShape):
    """Cuboid shape class"""
    gds_type = _sff.cuboid
    gds_tag_name = u"cuboid"
    repr_string = u"SFFCuboid(id={}, x={}, y={}, z={}, transform_id={}, attribute={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id', u'attribute')
    eq_attrs = [u'x', u'y', u'z']

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'shape': u'cuboid',
            u'x': self.x,
            u'y': self.y,
            u'z': self.z,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data, args=None):
        if u'shape' in data:
            if data[u'shape'] == u'cuboid':
                obj = cls(new_obj=False)
                if u'id' in data:
                    obj.id = data[u'id']
                if u'x' in data:
                    obj.x = data[u'x']
                if u'y' in data:
                    obj.y = data[u'y']
                if u'z' in data:
                    obj.z = data[u'z']
                if u'transform_id' in data:
                    obj.transform_id = data[u'transform_id']
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cuboid".format(data[u'shape']))
        else:
            raise ValueError(u"missing 'shape' attribute")

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.x is not None:
            group[u'x'] = self.x
        if self.y is not None:
            group[u'y'] = self.y
        if self.z is not None:
            group[u'z'] = self.z
        if self.transform_id is not None:
            group[u'transform_id'] = self.transform_id
        group[u'shape'] = u'cuboid'
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'shape' in group:
            if group[u'shape'][()] == u'cuboid':
                if u'id' in group:
                    obj.id = group[u'id'][()]
                if u'x' in group:
                    obj.x = group[u'x'][()]
                if u'y' in group:
                    obj.y = group[u'y'][()]
                if u'z' in group:
                    obj.z = group[u'z'][()]
                if u'transform_id' in group:
                    obj.transform_id = group[u'transform_id'][()]
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cuboid".format(group[u'shape'][()]))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFCylinder(SFFShape):
    """Cylinder shape class"""
    gds_type = _sff.cylinder
    gds_tag_name = u"cylinder"
    repr_string = u"SFFCylinder(id={}, height={}, diameter={}, transform_id={}, attribute={})"
    repr_args = (u'id', u'height', u'diameter', u'transform_id', u'attribute')
    eq_attrs = [u'height', u'diameter']

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cylinder height")
    diameter = SFFAttribute(u'diameter', required=True, help=u"cylinder diameter")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'shape': u'cylinder',
            u'height': self.height,
            u'diameter': self.diameter,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data, args=None):
        if u'shape' in data:
            if data[u'shape'] == u'cylinder':
                obj = cls(new_obj=False)
                if u'id' in data:
                    obj.id = data[u'id']
                if u'height' in data:
                    obj.height = data[u'height']
                if u'diameter' in data:
                    obj.diameter = data[u'diameter']
                if u'transform_id' in data:
                    obj.transform_id = data[u'transform_id']
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cylinder".format(data[u'shape']))
        else:
            raise ValueError(u"missing 'shape' attribute")

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.height is not None:
            group[u'height'] = self.height
        if self.diameter is not None:
            group[u'diameter'] = self.diameter
        if self.transform_id is not None:
            group[u'transform_id'] = self.transform_id
        group[u'shape'] = u'cylinder'
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'shape' in group:
            if group[u'shape'][()] == u'cylinder':
                if u'id' in group:
                    obj.id = group[u'id'][()]
                if u'height' in group:
                    obj.height = group[u'height'][()]
                if u'diameter' in group:
                    obj.diameter = group[u'diameter'][()]
                if u'transform_id' in group:
                    obj.transform_id = group[u'transform_id'][()]
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into cylinder".format(group[u'shape'][()]))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFEllipsoid(SFFShape):
    """Ellipsoid shape class"""
    gds_type = _sff.ellipsoid
    gds_tag_name = u"ellipsoid"
    repr_string = u"SFFEllipsoid(id={}, x={}, y={}, z={}, transform_id={}, attribute={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id', u'attribute')
    eq_attrs = [u'x', u'y', u'z']

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u'id': int(self.id),
            u'shape': u'ellipsoid',
            u'x': self.x,
            u'y': self.y,
            u'z': self.z,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data, args=None):
        if u'shape' in data:
            if data[u'shape'] == u'ellipsoid':
                obj = cls(new_obj=False)
                if u'id' in data:
                    obj.id = data[u'id']
                if u'x' in data:
                    obj.x = data[u'x']
                if u'y' in data:
                    obj.y = data[u'y']
                if u'z' in data:
                    obj.z = data[u'z']
                if u'transform_id' in data:
                    obj.transform_id = data[u'transform_id']
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into ellipsoid".format(data[u'shape']))
        else:
            raise ValueError(u"missing 'shape' attribute")

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.x is not None:
            group[u'x'] = self.x
        if self.y is not None:
            group[u'y'] = self.y
        if self.z is not None:
            group[u'z'] = self.z
        if self.transform_id is not None:
            group[u'transform_id'] = self.transform_id
        group[u'shape'] = u'ellipsoid'
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'shape' in group:
            if group[u'shape'][()] == u'ellipsoid':
                if u'id' in group:
                    obj.id = group[u'id'][()]
                if u'x' in group:
                    obj.x = group[u'x'][()]
                if u'y' in group:
                    obj.y = group[u'y'][()]
                if u'z' in group:
                    obj.z = group[u'z'][()]
                if u'transform_id' in group:
                    obj.transform_id = group[u'transform_id'][()]
                return obj
            else:
                raise SFFTypeError(u"cannot convert shape '{}' into ellipsoid".format(group[u'shape'][()]))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFShapePrimitiveList(SFFListType):
    """Container for shapes"""
    gds_type = _sff.shape_primitive_listType
    gds_tag_name = u'shape_primitive_list'
    repr_string = u"SFFShapePrimitiveList({})"
    repr_args = (u'list()',)
    iter_attr = (u'shape_primitive', SFFShape)
    sibling_classes = [
        (_sff.cone, SFFCone),
        (_sff.cuboid, SFFCuboid),
        (_sff.cylinder, SFFCylinder),
        (_sff.ellipsoid, SFFEllipsoid),
    ]

    def _shape_count(self, shape_type):
        return len(list(filter(lambda s: isinstance(s, shape_type), self._local.shape_primitive)))

    @property
    def num_ellipsoids(self):
        """The number of ellipsoids in this container"""
        return self._shape_count(_sff.ellipsoid)

    @property
    def num_cuboids(self):
        """The number of cuboids in this container"""
        return self._shape_count(_sff.cuboid)

    @property
    def num_cylinders(self):
        """The number of cylinders in this container"""
        return self._shape_count(_sff.cylinder)

    @property
    def num_cones(self):
        """The number of cones in this container"""
        return self._shape_count(_sff.cone)

    #     @property
    #     def num_subtomogram_averages(self):
    #         return self._shape_count(sff.subtomogramAverage)

    def as_json(self, args=None):
        slist = list()
        for shape in self:
            slist.append(shape.as_json(args=args))
        return slist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for shape in data:
            if u'shape' in shape:
                if shape[u'shape'] == u'cone':
                    obj.append(SFFCone.from_json(shape, args=args))
                elif shape[u'shape'] == u'cuboid':
                    obj.append(SFFCuboid.from_json(shape, args=args))
                elif shape[u'shape'] == u'cylinder':
                    obj.append(SFFCylinder.from_json(shape, args=args))
                elif shape[u'shape'] == u'ellipsoid':
                    obj.append(SFFEllipsoid.from_json(shape, args=args))
                else:
                    raise SFFTypeError(u"cannot convert shape '{}'".format(data[u'shape']))
            else:
                raise ValueError(u"missing 'shape' attribute")
        return obj

    def as_hff(self, parent_group, name=u'shape_primitive_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for shape in self:
            group = shape.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'shape_primitive_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            if u'shape' in subgroup:
                if subgroup[u'shape'][()] == u'cone':
                    obj.append(SFFCone.from_hff(subgroup, args=args))
                elif subgroup[u'shape'][()] == u'cuboid':
                    obj.append(SFFCuboid.from_hff(subgroup, args=args))
                elif subgroup[u'shape'][()] == u'cylinder':
                    obj.append(SFFCylinder.from_hff(subgroup, args=args))
                elif subgroup[u'shape'][()] == u'ellipsoid':
                    obj.append(SFFEllipsoid.from_hff(subgroup, args=args))
                else:
                    raise SFFTypeError(u"cannot convert shape '{}'".format(subgroup[u'shape'][()]))
            else:
                raise ValueError(u"missing 'shape' attribute")
        return obj


class SFFSegment(SFFIndexType):
    """Class that encapsulates segment data"""
    gds_type = _sff.segment_type
    gds_tag_name = u'segment'
    repr_string = u"""SFFSegment(id={}, parent_id={}, biological_annotation={}, colour={}, three_d_volume={}, mesh_list={}, shape_primitive_list={})"""
    repr_args = (
        u'id', u'parent_id', u'biological_annotation', u'colour', u'three_d_volume', u'mesh_list',
        u'shape_primitive_list')
    segment_id = 1
    segment_parent_id = 0
    index_attr = u'segment_id'
    start_at = 1
    eq_attrs = [u'biological_annotation', u'colour', u'mesh_list', u'three_d_volume', u'shape_primitive_list']

    # attributes
    id = SFFAttribute(
        u'id',
        required=True,
        help=u"the ID for this segment; segment IDs begin at 1 with the value of 0 implying the segmentation "
             u"i.e. all segments are children of the root segment (the segmentation)"
    )
    parent_id = SFFAttribute(
        u'parent_id',
        required=True,
        default=0,
        help=u"the ID for the segment that contains this segment; defaults to 0 (the whole segmentation)"
    )
    biological_annotation = SFFAttribute(u'biological_annotation', sff_type=SFFBiologicalAnnotation,
                                         help=u"the biological annotation for this segment; described using a :py:class:`sfftkrw.schema.adapter.SFFBiologicalAnnotation` object")
    colour = SFFAttribute(u'colour', sff_type=SFFRGBA, required=True,
                          help=u"this segments colour; described using a :py:class:`sfftkrw.schema.adapter.SFFRGBA` object")
    mesh_list = SFFAttribute(u'mesh_list', sff_type=SFFMeshList,
                             help=u"the list of mesh_list (if any) that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFMeshList` object")
    three_d_volume = SFFAttribute(u'three_d_volume', sff_type=SFFThreeDVolume,
                                  help=u"the 3D volume (if any) that describes this segment; a :py:class:`sfftkrw.schema.adapter.SFFThreeDVolume` object ")
    shape_primitive_list = SFFAttribute(u'shape_primitive_list', sff_type=SFFShapePrimitiveList,
                                        help=u"the list of shape primitives that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFShapePrimitiveList` object")

    def as_json(self, args=None):
        """Format this segment as JSON"""
        if self.id is None:
            self.id = get_unique_id()
        if args is not None:
            if args.exclude_geometry:
                return {
                    u'id': int(self.id),
                    u'parent_id': int(self.parent_id),
                    u'biological_annotation': self.biological_annotation.as_json(args=args) if self.biological_annotation is not None else None,
                    u'colour': self.colour.as_json(args=args) if self.colour is not None else None,
                    u'mesh_list': [],
                    u'three_d_volume': None,
                    u'shape_primitive_list': [],
                }
        return {
            u'id': int(self.id),
            u'parent_id': int(self.parent_id),
            u'biological_annotation': self.biological_annotation.as_json(args=args) if self.biological_annotation is not None else None,
            u'colour': self.colour.as_json(args=args) if self.colour is not None else None,
            u'mesh_list': self.mesh_list.as_json(args=args),
            u'three_d_volume': self.three_d_volume.as_json(args=args) if self.three_d_volume is not None else None,
            u'shape_primitive_list': self.shape_primitive_list.as_json(args=args)
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'parent_id' in data:
            obj.parent_id = data[u'parent_id']
        if u'colour' in data:
            obj.colour = SFFRGBA.from_json(data[u'colour'], args=args)
        if u'biological_annotation' in data:
            if data[u'biological_annotation']:
                obj.biological_annotation = SFFBiologicalAnnotation.from_json(data[u'biological_annotation'], args=args)
        if u'mesh_list' in data:
            if data[u'mesh_list']:
                obj.mesh_list = SFFMeshList.from_json(data[u'mesh_list'], args=args)
        if u'shape_primitive_list' in data:
            if data[u'shape_primitive_list']:
                obj.shape_primitive_list = SFFShapePrimitiveList.from_json(data[u'shape_primitive_list'], args=args)
        if u'three_d_volume' in data:
            if data[u'three_d_volume']:
                obj.three_d_volume = SFFThreeDVolume.from_json(data[u'three_d_volume'], args=args)
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.parent_id is not None:
            group[u'parent_id'] = self.parent_id
        if self.biological_annotation is not None:
            group = self.biological_annotation.as_hff(group, args=args)
        if self.colour is not None:
            group = self.colour.as_hff(group, args=args)
        if self.mesh_list:
            group = self.mesh_list.as_hff(group, args=args)
        if self.three_d_volume is not None:
            group = self.three_d_volume.as_hff(group, args=args)
        if self.shape_primitive_list:
            group = self.shape_primitive_list.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group[parent_group.name]
        obj = cls(new_obj=False)
        if u'id' in group:
            obj.id = group[u'id'][()]
        if u'parent_id' in group:
            obj.parent_id = group[u'parent_id'][()]
        if u'biological_annotation' in group:
            obj.biological_annotation = SFFBiologicalAnnotation.from_hff(group, args=args)
        if u'colour' in group:
            obj.colour = SFFRGBA.from_hff(group, args=args)
        if u'mesh_list' in group:
            obj.mesh_list = SFFMeshList.from_hff(group, args=args)
        if u'three_d_volume' in group:
            obj.three_d_volume = SFFThreeDVolume.from_hff(group, args=args)
        if u'shape_primitive_list' in group:
            obj.shape_primitive_list = SFFShapePrimitiveList.from_hff(group, args=args)
        return obj


class SFFSegmentList(SFFListType):
    """Container for segments"""
    gds_type = _sff.segment_listType
    gds_tag_name = u'segment_list'
    repr_string = u"SFFSegmentList({})"
    repr_args = (u'list()',)
    iter_attr = (u'segment', SFFSegment)

    def as_json(self, args=None):
        slist = list()
        for seg in self:
            slist.append(seg.as_json(args=args))
        return slist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for seg in data:
            obj.append(SFFSegment.from_json(seg, args=args))
        return obj

    def as_hff(self, parent_group, name=u'segment_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for segment in self:
            group = segment.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'segment_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFSegment.from_hff(subgroup, args=args))
        return obj


class SFFTransformationMatrix(SFFIndexType):
    """Transformation matrix transform"""
    gds_type = _sff.transformation_matrix_type
    gds_tag_name = u"transformation_matrix"
    repr_string = u"SFFTransformationMatrix(id={}, rows={}, cols={}, data={})"
    repr_args = (u'id', u'rows', u'cols', u'data')
    transform_id = 0
    index_attr = u'transform_id'
    eq_attrs = [u'rows', u'cols', u'data']

    # attributes
    id = SFFAttribute(u'id', required=True, help=u"an ID for this transform")
    rows = SFFAttribute(u'rows', required=True, help=u"the number of rows in this matrix")
    cols = SFFAttribute(u'cols', required=True, help=u"the number of columns in this matrix")
    data = SFFAttribute(u'data', required=True, help=u"a string sequence by row of the data in this matrix")

    # todo: work with numpy arrays transparently
    def __init__(self, **kwargs):
        """SFFTransformationMatrix(rows=None, cols=None, data=None)"""
        if u'data' in kwargs:
            if isinstance(kwargs[u'data'], numpy.ndarray):
                # sanity check
                _rows, _cols = kwargs[u'data'].shape
                if u'rows' in kwargs and u'cols' in kwargs:
                    try:
                        assert _rows == kwargs[u'rows'] and _cols == kwargs[u'cols']
                    except AssertionError:
                        raise ValueError(u"incompatible rows/cols and array")
                else:
                    kwargs[u'rows'], kwargs[u'cols'] = _rows, _cols
                self._data = kwargs[u'data']
                # make string from numpy array
                kwargs[u'data'] = SFFTransformationMatrix.stringify(kwargs[u'data'])
            elif isinstance(kwargs[u'data'], (_bytes, _str)):
                # make numpy array from string
                _raw_data = kwargs[u'data'].split(' ')
                _rows = kwargs[u'rows']
                _cols = kwargs[u'cols']
                # check for consistency
                try:
                    assert _rows * _cols == len(_raw_data)
                except AssertionError:
                    raise ValueError(u"incompatible rows/cols and array")
                else:
                    _data = numpy.array(list(map(float, _raw_data))).reshape(_rows,
                                                                             _cols)
                    self._data = _data
        super(SFFTransformationMatrix, self).__init__(**kwargs)

    @classmethod
    def from_array(cls, ndarray, **kwargs):
        """Construct an `SFFTransformationMatrix` object from a numpy `numpy.ndarray` array

        :param ndarray: a numpy array
        :type ndarray: :py:class:`numpy.ndarray`
        :return: a :py:class:`SFFTransformationMatrix` object
        """
        rows, cols = ndarray.shape
        obj = cls(
            rows=rows,
            cols=cols,
            data=SFFTransformationMatrix.stringify(ndarray),
            **kwargs
        )
        obj._data = ndarray
        return obj

    @staticmethod
    def stringify(array):
        """Convert a :py:class:`numpy.ndarray` to a space-separated list of numbers """
        return u" ".join(list(map(repr, array.flatten().tolist())))

    @property
    def data_array(self):
        if not hasattr(self, u'_data'):
            # make numpy array from string
            self._data = numpy.array(list(map(float, self.data.split(' ')))).reshape(
                self.rows,
                self.cols
            )
        return self._data

    @data_array.setter
    def data_array(self, ndarray):
        """
        Set the data when an object is defined post hoc. This setter overrides the values of the matrix
        :param ndarray: a numpy array
        :type ndarray: `numpy.ndarray`
        :raises ValueError: if ndarray is not of the right type
        """
        # overwrite whatever we had before
        try:
            assert isinstance(ndarray, numpy.ndarray)
        except AssertionError:
            raise ValueError("not a numpy array")
        self.rows, self.cols = ndarray.shape
        self._data = ndarray
        self.data = self.stringify(ndarray)

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u"id": int(self.id),
            u"rows": int(self.rows),
            u"cols": int(self.cols),
            u"data": self.data,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        obj.id = data[u'id']
        obj.rows = int(data[u'rows'])
        obj.cols = int(data[u'cols'])
        obj.data = data[u'data']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.rows is not None:
            group[u'rows'] = self.rows
        if self.cols is not None:
            group[u'cols'] = self.cols
        if self.data is not None:
            group[u'data'] = self.data
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'id' in group:
            obj.id = group[u'id'][()]
        if u'rows' in group:
            obj.rows = group[u'rows'][()]
        if u'cols' in group:
            obj.cols = group[u'cols'][()]
        if u'data' in group:
            obj.data = group[u'data'][()]
        return obj


class SFFTransformList(SFFListType):
    """Container for transforms"""
    gds_type = _sff.transform_listType
    gds_tag_name = u'transform_list'
    repr_string = u"SFFTransformList({})"
    repr_args = (u'list()',)
    iter_attr = (u'transformation_matrix', SFFTransformationMatrix)
    min_length = 1

    def _check_transformation_matrix_homogeneity(self):
        """Helper method to check transformation matrix homogeneity

        If the transformation matrices are not homogeneous then we cannot use
        structured arrays in numpy :'(
        """
        transformation_matrices_similar = True  # assume they are all similar
        first = True
        rows = None
        cols = None
        for transform in self:
            if first:
                rows = transform.rows
                cols = transform.cols
                first = False
            else:
                if transform.rows != rows or transform.cols != cols:
                    transformation_matrices_similar = False
                    break
        return transformation_matrices_similar, rows, cols

    def as_json(self, args=None):
        tlist = list()
        for tx in self:
            tlist.append(tx.as_json(args=args))
        return tlist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for tx in data:
            obj.append(SFFTransformationMatrix.from_json(tx, args=args))
        return obj

    def as_hff(self, parent_group, name=u'transform_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for sw in self:
            group = sw.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'transform_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFTransformationMatrix.from_hff(subgroup, args=args))
        return obj


class SFFSoftware(SFFIndexType):
    """Class definition for specifying software used to create this segmentation

    .. py:attribute:: name

        The name of the software used

    .. py:attribute:: version

        The version string

    .. py:attribute:: processing_details

        Details of how the segmentation was produced
    """
    gds_type = _sff.software_type
    gds_tag_name = u'software'
    repr_string = u"SFFSoftware(id={}, name={}, version={}, processing_details={})"
    repr_args = (u'id', u'name', u'version', u'processing_details')
    software_id = 0
    index_attr = u'software_id'
    eq_attrs = [u'name', u'version', u'processing_details']

    # attributes
    id = SFFAttribute(u'id', help=u"the software ID")
    name = SFFAttribute(u'name', required=True, help=u"the software/programmeu's name")
    version = SFFAttribute(u'version', help=u"the version used")
    processing_details = SFFAttribute(u'processing_details',
                                      help=u"a description of how the data was processed to produce the segmentation")

    def as_json(self, args=None):
        if self.id is None:
            self.id = get_unique_id()
        return {
            u"id": int(self.id),
            u"name": self.name,
            u"version": self.version,
            u"processing_details": self.processing_details,
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        obj.id = data[u'id']
        obj.name = data[u'name']
        obj.version = data[u'version']
        obj.processing_details = data[u'processing_details']
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        if self.id is None:
            self.id = get_unique_id()
        if not name:
            name = _str(self.id)
        else:
            _assert_or_raise(name, _str)
        group = parent_group.create_group(name)
        if self.id is not None:
            group[u'id'] = self.id
        if self.name is not None:
            group[u'name'] = self.name
        if self.version is not None:
            group[u'version'] = self.version
        if self.processing_details is not None:
            group[u'processing_details'] = self.processing_details
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[parent_group.name]
        if u'id' in group:
            obj.id = group[u'id'][()]
        if u'name' in group:
            obj.name = group[u'name'][()]
        if u'version' in group:
            obj.version = group[u'version'][()]
        if u'processing_details' in group:
            obj.processing_details = group[u'processing_details'][()]
        return obj


class SFFSoftwareList(SFFListType):
    """List of SFFSoftware objects"""
    gds_type = _sff.software_listType
    gds_tag_name = u'software_list'
    repr_string = u"SFFSoftwareList({})"
    repr_args = (u'list()',)
    iter_attr = (u'software', SFFSoftware)

    def as_json(self, args=None):
        slist = list()
        for sw in self:
            slist.append(sw.as_json(args=args))
        return slist

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for sw in data:
            obj.append(SFFSoftware.from_json(sw, args=args))
        return obj

    def as_hff(self, parent_group, name=u'software_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for sw in self:
            group = sw.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'software_list', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        for subgroup in sorted(group.values(), key=lambda g: int(os.path.basename(g.name))):
            obj.append(SFFSoftware.from_hff(subgroup, args=args))
        return obj


class SFFBoundingBox(SFFType):
    """Dimensions of bounding box"""
    #  config
    gds_type = _sff.bounding_box_type
    gds_tag_name = u'bounding_box'
    repr_string = u"SFFBoundingBox(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={})"
    repr_args = (u'xmin', u'xmax', u'ymin', u'ymax', u'zmin', u'zmax')
    eq_attrs = [u'xmin', u'xmax', u'ymin', u'ymax', u'zmin', u'zmax']

    # attributes
    xmin = SFFAttribute(u'xmin', default=0, help=u"minimum x co-ordinate value")
    xmax = SFFAttribute(u'xmax', required=True, help=u"maximum x co-ordinate value")
    ymin = SFFAttribute(u'ymin', default=0, help=u"minimum y co-ordinate value")
    ymax = SFFAttribute(u'ymax', required=True, help=u"maximum y co-ordinate value")
    zmin = SFFAttribute(u'zmin', default=0, help=u"minimum z co-ordinate value")
    zmax = SFFAttribute(u'zmax', required=True, help=u"maximum z co-ordinate value")

    def as_json(self, args=None):
        bb = dict()
        if self.xmin is not None:
            bb[u'xmin'] = self.xmin
        if self.xmax is not None:
            bb[u'xmax'] = self.xmax
        if self.ymin is not None:
            bb[u'ymin'] = self.ymin
        if self.ymax is not None:
            bb[u'ymax'] = self.ymax
        if self.zmin is not None:
            bb[u'zmin'] = self.zmin
        if self.zmax is not None:
            bb[u'zmax'] = self.zmax
        return bb

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if data is not None:
            _assert_or_raise(data, (_classic_dict, _dict))
            if u'xmin' in data:
                obj.xmin = data[u'xmin']
            if u'xmax' in data:
                obj.xmax = data[u'xmax']
            if u'ymin' in data:
                obj.ymin = data[u'ymin']
            if u'ymax' in data:
                obj.ymax = data[u'ymax']
            if u'zmin' in data:
                obj.zmin = data[u'zmin']
            if u'zmax' in data:
                obj.zmax = data[u'zmax']
        return obj

    def as_hff(self, parent_group, name=u'bounding_box', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        group[u'xmin'] = self.xmin
        if self.xmax is not None:
            group[u'xmax'] = self.xmax
        group[u'ymin'] = self.ymin
        if self.ymax is not None:
            group[u'ymax'] = self.ymax
        group[u'zmin'] = self.zmin
        if self.zmax is not None:
            group[u'zmax'] = self.zmax
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=u'bounding_box', args=None):
        _assert_or_raise(parent_group, h5py.Group)
        obj = cls(new_obj=False)
        group = parent_group[name]
        if u'xmin' in group:
            obj.xmin = group[u'xmin'][()]
        if u'xmax' in group:
            obj.xmax = group[u'xmax'][()]
        if u'ymin' in group:
            obj.ymin = group[u'ymin'][()]
        if u'ymax' in group:
            obj.ymax = group[u'ymax'][()]
        if u'zmin' in group:
            obj.zmin = group[u'zmin'][()]
        if u'zmax' in group:
            obj.zmax = group[u'zmax'][()]
        return obj


class SFFSegmentation(SFFType):
    """Adapter class to make using the output of ``generateDS`` easier to use"""
    gds_type = _sff.segmentation
    gds_tag_name = u'segmentation'
    repr_string = u"SFFSegmentation(name={}, version={})"
    repr_args = (u'name', u"version")
    eq_attrs = [
        u'name', u'version', u'software_list', u'primary_descriptor', u'transform_list', u'bounding_box',
        u'global_external_references', u'segment_list', u'lattice_list', u'details']

    # attributes
    name = SFFAttribute(u'name', required=True, help=u"the name of this segmentation")
    version = SFFAttribute(u'version', required=True, help=u"EMDB-SFF version")
    software_list = SFFAttribute(
        u'software_list',
        sff_type=SFFSoftwareList,
        help=u"the list of software tools used to crate this segmentation a :py:class:`sfftkrw.schema.adapter.SFFSoftwareList` object"
    )
    primary_descriptor = SFFAttribute(
        u'primary_descriptor',
        required=True,
        help=u"the main type of representation used for this segmentation; "
             u"can be one of 'mesh_list', 'shape_primitive_list' or 'threeDVolume'"
    )
    transform_list = SFFAttribute(
        u'transform_list',
        required=True,
        sff_type=SFFTransformList,
        help=u"a list of transforms; a :py:class:`sfftkrw.schema.adapter.SFFTransformList` object"
    )
    bounding_box = SFFAttribute(
        u'bounding_box',
        sff_type=SFFBoundingBox,
        help=u"the bounding box in which the segmentation sits; a :py:class:`sfftkrw.schema.adapter.SFFBoundingBox` object"
    )
    global_external_references = SFFAttribute(
        u'global_external_references',
        sff_type=SFFGlobalExternalReferenceList,
        help=u"a list of external references that apply to the whole segmentation (global); "
             u"a :py:class:`sfftkrw.schema.adapter.SFFGlobalexternal_references` object"
    )
    segment_list = SFFAttribute(
        u'segment_list',
        sff_type=SFFSegmentList,
        help=u"the list of annotated segments; a :py:class:`sfftkrw.schema.adapter.SFFSegmentList` object"
    )
    lattice_list = SFFAttribute(
        u'lattice_list',
        sff_type=SFFLatticeList,
        help=u"the list of lattices (if any) containing 3D volumes referred to; "
             u"a :py:class:`sfftkrw.schema.adapter.SFFLatticeList` object"
    )
    details = SFFAttribute(
        u'details', help=u"any other details about this segmentation (free text)")

    @property
    def transforms(self):
        return self.transform_list

    @transforms.setter
    def transforms(self, value):
        self.transform_list = value

    @property
    def segments(self):
        return self.segment_list

    @segments.setter
    def segments(self, value):
        self.segment_list = value

    @property
    def lattices(self):
        return self.lattice_list

    @lattices.setter
    def lattices(self, value):
        self.lattice_list = value

    def as_json(self, args=None):
        if args is not None:
            if args.exclude_geometry:
                return {
                    u'version': self.version,
                    u'name': self.name,
                    u'details': self.details,
                    u'software_list': self.software_list.as_json(args=args),
                    u'primary_descriptor': self.primary_descriptor,
                    u'transform_list': self.transform_list.as_json(args=args),
                    u'bounding_box': self.bounding_box.as_json(args=args) if self.bounding_box else None,
                    u'global_external_references': self.global_external_references.as_json(args=args),
                    u'segment_list': self.segment_list.as_json(args=args),
                }
        return {
            u'version': self.version,
            u'name': self.name,
            u'details': self.details,
            u'software_list': self.software_list.as_json(args=args),
            u'primary_descriptor': self.primary_descriptor,
            u'transform_list': self.transform_list.as_json(args=args),
            u'bounding_box': self.bounding_box.as_json(args=args) if self.bounding_box else None,
            u'global_external_references': self.global_external_references.as_json(args=args),
            u'segment_list': self.segment_list.as_json(args=args),
            u'lattice_list': self.lattice_list.as_json(args=args),
        }

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'version' in data:
            obj.version = data[u'version']
        if u'name' in data:
            obj.name = data[u'name']
        if u'details' in data:
            obj.details = data[u'details']
        if u'software_list' in data:
            obj.software_list = SFFSoftwareList.from_json(data[u'software_list'], args=args)
        if u'primary_descriptor' in data:
            obj.primary_descriptor = data[u'primary_descriptor']
        if u'transform_list' in data:
            obj.transform_list = SFFTransformList.from_json(data[u'transform_list'], args=args)
        if u'bounding_box' in data:
            obj.bounding_box = SFFBoundingBox.from_json(data[u'bounding_box'], args=args)
        if u'global_external_references' in data:
            obj.global_external_references = SFFGlobalExternalReferenceList.from_json(
                data[u'global_external_references'], args=args)
        if u'segment_list' in data:
            obj.segment_list = SFFSegmentList.from_json(data[u'segment_list'], args=args)
        if u'lattice_list' in data:
            obj.lattice_list = SFFLatticeList.from_json(data[u'lattice_list'])
        return obj

    def as_hff(self, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.File)
        group = parent_group
        if self.version is not None:
            group[u'version'] = self.version
        if self.name is not None:
            group[u'name'] = self.name
        if self.details is not None:
            group[u'details'] = self.details
        if self.software_list:
            group = self.software_list.as_hff(group, args=args)
        if self.primary_descriptor is not None:
            group[u'primary_descriptor'] = self.primary_descriptor
        if self.transform_list:
            group = self.transform_list.as_hff(group, args=args)
        if self.bounding_box is not None:
            group = self.bounding_box.as_hff(group, args=args)
        if self.global_external_references:
            group = self.global_external_references.as_hff(group, args=args)
        if self.segment_list:
            group = self.segment_list.as_hff(group, args=args)
        if self.lattice_list:
            group = self.lattice_list.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        _assert_or_raise(parent_group, h5py.File)
        obj = cls(new_obj=False)
        group = parent_group
        if u'version' in group:
            obj.version = group[u'version'][()]
        if u'name' in group:
            obj.name = group[u'name'][()]
        if u'details' in group:
            obj.details = group[u'details'][()]
        if u'software_list' in group:
            obj.software_list = SFFSoftwareList.from_hff(group, args=args)
        if u'primary_descriptor' in group:
            obj.primary_descriptor = group[u'primary_descriptor'][()]
        if u'transform_list' in group:
            obj.transform_list = SFFTransformList.from_hff(group, args=args)
        if u'bounding_box' in group:
            obj.bounding_box = SFFBoundingBox.from_hff(group, args=args)
        if u'global_external_references' in group:
            obj.global_external_references = SFFGlobalExternalReferenceList.from_hff(group, args=args)
        if u'segment_list' in group:
            obj.segment_list = SFFSegmentList.from_hff(group, args=args)
        if u'lattice_list' in group:
            obj.lattice_list = SFFLatticeList.from_hff(group, args=args)
        return obj

    @classmethod
    def from_file(cls, fn, args=None):
        """Instantiate an :py:class:`SFFSegmentations` object from a file name

        The file suffix determines how the data is extracted.

        :param str fn: name of a file hosting an EMDB-SFF-structured segmentation
        :return seg: the corresponding :py:class:`SFFSegmentation` object
        :rtype seg: :py:class:`SFFSegmentation`
        """
        if not os.path.exists(fn):
            print_date(_encode(u"File {} not found".format(fn), u'utf-8'))
            sys.exit(os.EX_IOERR)
        else:
            if re.match(r'.*\.(sff|xml)$', fn, re.IGNORECASE):
                seg_local = _sff.parse(fn, silence=True)
            elif re.match(r'.*\.(hff|h5|hdf5)$', fn, re.IGNORECASE):
                with h5py.File(fn, u'r') as h:
                    seg = cls.from_hff(h, args=args)
                seg_local = seg._local
            elif re.match(r'.*\.json$', fn, re.IGNORECASE):
                with open(fn, u'r') as f:
                    data = json.load(f)
                seg = cls.from_json(data, args=args)
                seg_local = seg._local
            else:
                print_date(_encode(u"Invalid EMDB-SFF file name: {}".format(fn), u'utf-8'))
                sys.exit(os.EX_DATAERR)
        # now create the output object
        obj = cls(new_obj=False)
        obj._local = seg_local
        return obj

    def to_file(self, *args, **kwargs):
        """Alias for :py:meth:`.export` method. Passes all args and kwargs onto :py:meth:`.export`"""
        return super(SFFSegmentation, self).export(*args, **kwargs)

    def merge_annotation(self, other_seg):
        """Merge the annotation from another sff_seg to this one

        :param other_seg: segmentation to get annotations from
        :type other_seg: :py:class:`sfftkrw.SFFSegmentation`
        """
        _assert_or_raise(other_seg, SFFSegmentation)
        # global data
        # self.name = other_seg.name
        # self.software_list = other_seg.software_list
        self.global_external_references = other_seg.global_external_references
        # self.details = other_seg.details
        # loop through segments
        for segment in self.segments:
            other_segment = other_seg.segments.get_by_id(segment.id)
            segment.biological_annotation = other_segment.biological_annotation

    def copy_annotation(self, from_id, to_id):
        """Copy annotation across segments

        :param int/list from_id: segment ID to get notes from; use -1 for for global notes
        :param int/list to_id: segment ID to copy notes to; use -1 for global notes
        """
        if from_id == -1:
            _from = self.global_external_references
        else:
            _from = self.segments.get_by_id(from_id).biological_annotation.external_references
        if to_id == -1:
            to = self.global_external_references
        else:
            to = self.segments.get_by_id(to_id).biological_annotation.external_references
        # the id for global notes
        for extref in _from:
            to.append(extref)

    def clear_annotation(self, from_id):
        """Clear all annotations from the segment with ID specified

        :param from_id: segment ID
        :return:
        """
        if from_id == -1:
            self.global_external_references.clear() # = SFFGlobalExternalReferenceList()
        else:
            segment = self.segments.get_by_id(from_id)
            segment.biological_annotation.external_references.clear() # = SFFExternalReferenceList()
