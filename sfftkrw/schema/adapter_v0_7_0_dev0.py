# -*- coding: utf-8 -*-
"""
adapter_v0_7_0_dev0
=======================
"""
from __future__ import division, print_function

import base64
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
from . import v0_7_0_dev0 as _sff
from .base import SFFType, SFFAttribute, SFFListType, SFFTypeError, SFFIndexType, _assert_or_raise
from .. import SFFTKRW_VERSION
from ..core import _decode, _dict, _str, _encode, _bytes, _xrange, _classic_dict
from ..core.print_tools import print_date

# ensure that we can read/write encoded data
_sff.ExternalEncoding = u"utf-8"


class SFFRGBA(SFFType):
    """RGBA colour"""
    gds_type = _sff.rgbaType
    repr_string = u"SFFRGBA(red={}, green={}, blue={}, alpha={})"
    repr_args = (u'red', u'green', u'blue', u'alpha')

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

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return self.value == other.value

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
        # group = parent_group.create_group(name)
        # group[u'rgba'] = self.value
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=u'colour', args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        # r = SFFRGBA()
        obj.value = hff_data[name][()]
        # obj.rgba = r
        return obj

    def as_json(self, args=None):
        """Export as JSON"""
        return {u'colour': self.value}

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'colour' in data:
            obj.value = data[u'colour']
        return obj


class SFFComplexList(SFFListType):
    """Class that encapsulates complex"""
    gds_type = _sff.complexType
    repr_string = u"SFFComplexList({})"
    repr_args = (u'list()',)
    iter_attr = (u'id', _str)

    # fixme: without an `sff_type` attribute we can set the ids attribute to anything!
    ids = SFFAttribute(u'id', help=u"the list of complex ids")

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Dataset)
        obj = cls()
        [obj.append(_decode(_, u'utf-8')) for _ in hff_data]
        return obj


class SFFMacromoleculeList(SFFListType):
    """Class that encapsulates macromolecule"""
    gds_type = _sff.macromoleculeType
    repr_string = u"SFFMacromoleculeList({})"
    repr_args = (u"list()",)
    # todo: same problem as SFFComplexList
    iter_attr = (u'id', _str)

    ids = SFFAttribute(u'id', help=u"the list of macromolecule ids")

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Dataset)
        obj = cls()
        [obj.append(_decode(_, u'utf-8')) for _ in hff_data]
        return obj


class SFFComplexesAndMacromolecules(SFFType):
    """Complexes and macromolecules"""
    gds_type = _sff.macromoleculesAndComplexesType
    repr_string = u"SFFComplexesAndMacromolecules(complexes={}, macromolecules={})"
    repr_args = (u'complexes', u'macromolecules')

    # attributes
    complexes = SFFAttribute(u'complex', sff_type=SFFComplexList, help=u"a list of complex accessions")
    macromolecules = SFFAttribute(u'macromolecule', sff_type=SFFMacromoleculeList,
                                  help=u"a list of macromolecule accessions")

    @property
    def num_complexes(self):
        return len(self.complexes)

    @property
    def num_macromolecules(self):
        return len(self.macromolecules)

    def _boolean_test(self):
        if self.complexes or self.macromolecules:
            return True
        else:
            return False

    if sys.version_info[0] > 2:
        def __bool__(self):
            return self._boolean_test()
    else:
        def __nonzero__(self):
            return self._boolean_test()

    def as_hff(self, parent_group, name=u"complexesAndMacromolecules", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        if self.complexes:
            group[u'complexes'] = self.complexes
        if self.macromolecules:
            group[u'macromolecules'] = self.macromolecules
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        if u"complexes" in hff_data:
            obj.complexes = SFFComplexList.from_hff(hff_data[u'complexes'], args=args)
        if u"macromolecules" in hff_data:
            obj.macromolecules = SFFMacromoleculeList.from_hff(hff_data[u'macromolecules'], args=args)
        return obj


class SFFExternalReference(SFFIndexType):
    """Class that encapsulates an external reference"""
    gds_type = _sff.externalReferenceType
    repr_string = u"SFFExternalReference(id={}, type={}, otherType={}, value={}, label={}, description={})"
    repr_args = (u'id', u'type', u'other_type', u'value', u'label', u'description')
    ref_id = 0
    index_attr = u'ref_id'

    # attributes
    id = SFFAttribute(u'id', help=u"this external reference's ID")
    type = SFFAttribute(u'type_', required=True, help=u"the ontology/archive name")
    other_type = SFFAttribute(u'otherType', required=True,
                              help=u"a URL/IRI where data for this external reference may be obtained")
    value = SFFAttribute(u'value', required=True, help=u"the accession for this external reference")
    label = SFFAttribute(u'label', help=u"a short description of this external reference")
    description = SFFAttribute(u'description', help=u"a long description of this external reference")

    # methods
    def __init__(self, **kwargs):
        # remap kwargs
        if u'type' in kwargs:
            kwargs[u'type_'] = kwargs[u'type']
            del kwargs[u'type']
        super(SFFExternalReference, self).__init__(**kwargs)

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        attrs = [u'type', u'other_type', u'value', u'label', u'description']
        return all(list(map(lambda a: getattr(self, a) == getattr(other, a), attrs)))

    def as_json(self, args=None):
        e = dict()
        if self.id is not None:  # value can be 0 which would evaluate to `False`
            e[u'id'] = self.id
        if self.type:
            e[u'type'] = self.type
        if self.other_type:
            e[u'otherType'] = self.other_type
        if self.value:
            e[u'value'] = self.value
        if self.label:
            e[u'label'] = self.label
        if self.description:
            e[u'description'] = self.description
        return e

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'type' in data:
            obj.type = data[u'type']
        if u'otherType' in data:
            obj.other_type = data[u'otherType']
        if u'value' in data:
            obj.value = data[u'value']
        if u'label' in data:
            obj.label = data[u'label']
        if u'description' in data:
            obj.description = data[u'description']
        return obj


class SFFExternalReferenceList(SFFListType):
    """Container for external references"""
    gds_type = _sff.externalReferencesType
    repr_string = u"SFFExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return all(list(map(lambda v: v[0] == v[1], zip(self, other))))

    def as_json(self, args=None):
        es = list()
        for extref in self:
            es.append(extref.as_json(args=None))
        return es

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        for extref in data:
            obj.append(SFFExternalReference.from_json(extref, args=args))
        return obj


class SFFBiologicalAnnotation(SFFType):
    """Biological annotation"""
    gds_type = _sff.biologicalAnnotationType
    repr_string = u"""SFFBiologicalAnnotation(name={}, description={}, numberOfInstances={}, externalReferences={})"""
    repr_args = (u'name', u'description', u'number_of_instances', u'external_references')

    # attributes
    name = SFFAttribute(u'name', help=u"the name of this segment")
    description = SFFAttribute(u'description', help=u"a brief description for this segment")
    external_references = SFFAttribute(u'externalReferences', sff_type=SFFExternalReferenceList,
                                       help=u"the set of external references")
    number_of_instances = SFFAttribute(u'numberOfInstances', default=1, help=u"the number of instances of this segment")

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

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        attrs = [u'name', u'description', u'external_references', u'number_of_instances']
        return all(list(map(lambda a: getattr(self, a) == getattr(other, a), attrs)))

    @property
    def num_external_references(self):
        if self.external_references:
            return len(self.external_references)
        else:
            return 0

    def as_hff(self, parent_group, name=u"biologicalAnnotation", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        # description and nubmerOfInstances as datasets
        if self.name:
            group[u'name'] = self.name
        if self.description:
            group[u'description'] = self.description
        if isinstance(self.number_of_instances, numbers.Integral):
            group[u'numberOfInstances'] = self.number_of_instances if self.number_of_instances > 0 else 1
        else:
            group[u'numberOfInstances'] = 1
        if self.external_references:
            vl_str = h5py.special_dtype(vlen=_str)
            h_ext = group.create_dataset(
                u"externalReferences",
                (self.num_external_references,),
                dtype=[
                    (u'type', vl_str),
                    (u'otherType', vl_str),
                    (u'value', vl_str),
                    (u'label', vl_str),
                    (u'description', vl_str),
                ]
            )
            i = 0
            for extref in self.external_references:
                h_ext[i] = (extref.type, extref.other_type, extref.value, extref.label, extref.description)
                i += 1
        return parent_group

    def as_json(self, args=None):
        bio_ann = _dict()
        if self.name:
            bio_ann[u'name'] = _str(self.name)
        if self.description:
            bio_ann[u'description'] = _str(self.description)
        if self.number_of_instances:
            bio_ann[u'numberOfInstances'] = self.number_of_instances
        if self.external_references:
            bio_ann[u'externalReferences'] = self.external_references.as_json(args=args)
        return bio_ann

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'name' in data:
            obj.name = data[u'name']
        if u'description' in data:
            obj.description = data[u'description']
        if u'numberOfInstances' in data:
            obj.number_of_instances = data[u'numberOfInstances']
        if u'externalReferences' in data:
            obj.external_references = SFFExternalReferenceList.from_json(data[u'externalReferences'], args=args)
        return obj

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls(new_obj=False)
        if u'name' in hff_data:
            obj.name = _decode(hff_data[u'name'][()], u'utf-8')
        else:
            obj.name = None
        if u'description' in hff_data:
            obj.description = _decode(hff_data[u'description'][()], u'utf-8')
        obj._number_ofi = int(hff_data[u'numberOfInstances'][()])
        if u"externalReferences" in hff_data:
            obj.external_references = SFFExternalReferenceList()
            for ref in hff_data[u'externalReferences']:
                e = SFFExternalReference(new_obj=False)
                # fixme: make sure external references are saved with their ID!
                e.type, e.other_type, e.value, e.label, e.description = list(map(lambda r: _decode(r, u'utf-8'), ref))
                obj.external_references.append(e)
        return obj


class SFFThreeDVolume(SFFType):
    """Class representing segments described using a 3D volume"""
    gds_type = _sff.threeDVolumeType
    repr_string = u"SFFThreeDVolume(latticeId={}, value={}, transformId={})"
    repr_args = (u'lattice_id', u'value', u'transform_id')

    # attributes
    lattice_id = SFFAttribute(u'latticeId', required=True,
                              help=u"the ID of the lattice that has the data for this 3D volume")
    value = SFFAttribute(u'value', required=True, help=u"the voxel values associated with this 3D volume")
    transform_id = SFFAttribute(u'transformId', help=u"a transform applied to this 3D volume [optional]")

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        attrs = [u'lattice_id', u'value', u'transform_id']
        return all(list(map(lambda a: getattr(self, a) == getattr(other, a), attrs)))

    def _boolean_test(self):
        if self.value is None:
            return False
        else:
            return True

    if sys.version_info[0] > 2:
        def __bool__(self):
            return self._boolean_test()
    else:
        def __nonzero__(self):
            return self._boolean_test()

    def as_hff(self, parent_group, name=u"volume", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        group[u'latticeId'] = self.lattice_id
        group[u'value'] = self.value
        if self.transform_id is not None:
            group[u'transformId'] = self.transform_id
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        obj.lattice_id = hff_data[u'latticeId'][()]
        obj.value = hff_data[u'value'][()]
        if u'transformId' in hff_data:
            obj.transform_id = hff_data[u'transformId'][()]
        return obj


class SFFVolume(SFFType):
    """Class for represention 3-space dimension"""
    # attributes
    cols = SFFAttribute(u'cols', help=u"number of columns")
    rows = SFFAttribute(u'rows', help=u"number of rows")
    sections = SFFAttribute(u'sections', help=u"number of sections (sets of congruent row-column collections)")

    @property
    def value(self):
        return self.cols, self.rows, self.sections

    @value.setter
    def value(self, value):
        if len(value) == 3:
            self.cols, self.rows, self.sections = value
        else:
            raise SFFTypeError(value, u"Iterable", message=u"should be of length 3")

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Dataset)
        obj = cls()
        obj.cols = hff_data[0]
        obj.rows = hff_data[1]
        obj.sections = hff_data[2]
        return obj


class SFFVolumeStructure(SFFVolume):
    gds_type = _sff.volumeStructureType
    repr_string = u"SFFVolumeStructure(cols={}, rows={}, sections={})"
    repr_args = (u'cols', u'rows', u'sections')

    @property
    def voxel_count(self):
        """The number of voxels in this volume"""
        return self.cols * self.rows * self.sections


class SFFVolumeIndex(SFFVolume):
    """Class representing volume indices"""
    # todo: implement an iterator to increment indices correctly
    gds_type = _sff.volumeIndexType
    repr_string = u"SFFVolumeIndex(cols={}, rows={}, sections={})"
    repr_args = (u'cols', u'rows', u'sections')


class SFFLattice(SFFIndexType):
    """Class representing 3D """
    gds_type = _sff.latticeType
    repr_string = u"SFFLattice(mode={}, endianness={}, size={}, start={}, data={})"
    repr_args = (u'mode', u'endianness', u'size', u'start', u'data[:100]')
    lattice_id = 0

    index_attr = u'lattice_id'

    # attributes
    id = SFFAttribute(u'id', required=True, help=u"the ID for this lattice (referenced by 3D volumes)")
    mode = SFFAttribute(u'mode', required=True,
                        help=u"type of data for each voxel; valid values are: int8, uint8, int16, uint16, int32, "
                             u"uint32, int64, uint64, float32, float64")
    endianness = SFFAttribute(u'endianness', required=True, help=u"endianness; either 'little' (default) or 'big'")
    size = SFFAttribute(u'size', sff_type=SFFVolumeStructure, required=True,
                        help=u"size of the lattice described using a "
                             ":py:class:`sfftkrw.schema.adapter.SFFVolumeStructure` object")
    start = SFFAttribute(u'start', sff_type=SFFVolumeIndex, required=True,
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
            elif isinstance(kwargs[u'data'], _bytes):
                self._data = SFFLattice._decode(kwargs[u'data'], **kwargs)
            elif isinstance(kwargs[u'data'], _str):
                _data = _encode(kwargs[u'data'], u'ASCII')
                self._data = SFFLattice._decode(_data, **kwargs)
                kwargs[u'data'] = _data
                del _data
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
        if not hasattr(self, u'_data'):
            # make numpy from bytes
            self._data = SFFLattice._decode(
                self.data,
                size=self.size,
                mode=self.mode,
                endiannes=self.endianness,
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
        :return bytes: the corresponding zipped bytes object
        """
        r, c, s = array.shape
        voxel_count = r * c * s
        format_string = "{}{}{}".format(ENDIANNESS[endianness], voxel_count, FORMAT_CHARS[mode])
        binpack = struct.pack(format_string, *array.flat)
        del array
        binzip = zlib.compress(binpack)
        del binpack
        bin64 = base64.b64encode(binzip)
        del binzip
        return bin64

    @staticmethod
    def _decode(bin64, size, mode=u'uint32', endianness=u'little', **kwargs):
        """Decode a base64-encoded, zipped byte sequence to a numpy array

        :param bin64: the base64-encoded zipped bytes
        :param size: the size of the expected volume
        :type size: :py:class:`SFFVolumeStructure`
        :return: a :py:class:`numpy.ndarray` object
        :rtype: :py:class:`numpy.ndarray`
        """
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

    def as_hff(self, parent_group, name=u"{}", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name.format(self.id))
        group[u'mode'] = _decode(self.mode, u'utf-8')
        group[u'endianness'] = _decode(self.endianness, u'utf-8')
        group[u'size'] = self.size.value
        group[u'start'] = self.start.value
        group[u'data'] = self.data
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        mode_ = _decode(hff_data[u'mode'][()], u'utf-8')
        obj = cls(
            mode=mode_,
            endianness=_decode(hff_data[u'endianness'][()], u'utf-8'),
            size=SFFVolumeStructure.from_hff(hff_data[u'size'], args=args),
            start=SFFVolumeIndex.from_hff(hff_data[u'start'], args=args),
            data=_decode(hff_data[u'data'][()], u'utf-8'),
        )
        return obj


class SFFLatticeList(SFFListType):
    """A container for lattice objects"""
    gds_type = _sff.latticeListType
    repr_string = u"SFFLatticeList({})"
    repr_args = (u"list()",)
    iter_attr = (u'lattice', SFFLattice)

    def as_hff(self, parent_group, name=u'lattices', args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for lattice in self:
            group = lattice.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        for lattice_id in hff_data:
            L = SFFLattice.from_hff(hff_data[lattice_id], args=args)
            L.id = int(lattice_id)  # good! we preserve IDs
            obj.append(L)
        return obj


class SFFShape(SFFIndexType):
    """Base shape class"""
    # repr_string = "{} {}"
    # repr_args = (u'ref', u'id')
    shape_id = 0
    index_attr = u'shape_id'
    index_in_super = True

    # attributes
    id = SFFAttribute(u'id', required=True, help=u"the ID of this shape")
    transform_id = SFFAttribute(u'transformId', required=True,
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
    repr_string = u"SFFCone(id={}, height={}, bottomRadius={}, transformId={})"
    repr_args = (u'id', u'height', u'bottom_radius', u'transform_id')

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cone height")
    bottom_radius = SFFAttribute(u'bottomRadius', required=True, help=u"cone bottom radius")


class SFFCuboid(SFFShape):
    """Cuboid shape class"""
    gds_type = _sff.cuboid
    gds_tag_name = u"cuboid"
    repr_string = u"SFFCuboid(id={}, x={}, y={}, z={}, transformId={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id')

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")


class SFFCylinder(SFFShape):
    """Cylinder shape class"""
    gds_type = _sff.cylinder
    gds_tag_name = u"cylinder"
    repr_string = u"SFFCylinder(id={}, height={}, diameter={}, transformId={})"
    repr_args = (u'id', u'height', u'diameter', u'transform_id')

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cylinder height")
    diameter = SFFAttribute(u'diameter', required=True, help=u"cylinder diameter")


class SFFEllipsoid(SFFShape):
    """Ellipsoid shape class"""
    gds_type = _sff.ellipsoid
    gds_tag_name = u"ellipsoid"
    repr_string = u"SFFEllipsoid(id={}, x={}, y={}, z={}, transformId={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id')

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")


class SFFShapePrimitiveList(SFFListType):
    """Container for shapes"""
    gds_type = _sff.shapePrimitiveListType
    repr_string = u"SFFShapePrimitiveList({})"
    repr_args = (u'list()',)
    iter_attr = (u'shapePrimitive', SFFShape)
    sibling_classes = [
        (_sff.cone, SFFCone),
        (_sff.cuboid, SFFCuboid),
        (_sff.cylinder, SFFCylinder),
        (_sff.ellipsoid, SFFEllipsoid),
    ]

    def _shape_count(self, shape_type):
        return len(list(filter(lambda s: isinstance(s, shape_type), self._local.shapePrimitive)))

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

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        if u"ellipsoids" in hff_data:
            for ellipsoid in hff_data[u"ellipsoids"]:
                e = SFFEllipsoid(new_obj=False)
                e.id = int(ellipsoid[u'id'])
                e.x = float(ellipsoid[u'x'])
                e.y = float(ellipsoid[u'y'])
                e.z = float(ellipsoid[u'z'])
                e.transform_id = int(ellipsoid[u'transformId'])
                if not numpy.isnan(ellipsoid[u'attribute']):
                    e.attribute = float(ellipsoid[u'attribute'])
                obj.append(e)
        if u"cones" in hff_data:
            for cone in hff_data[u"cones"]:
                c = SFFCone(new_obj=False)
                c.id = int(cone[u'id'])
                c.bottom_radius = float(cone[u'bottomRadius'])
                c.height = float(cone[u'height'])
                c.transform_id = int(cone[u'transformId'])
                if not numpy.isnan(cone[u'attribute']):
                    c.attribute = float(cone[u'attribute'])
                obj.append(c)
        if u"cuboids" in hff_data:
            for cuboid in hff_data[u"cuboids"]:
                c = SFFCuboid(new_obj=False)
                c.id = int(cuboid[u'id'])
                c.x = float(cuboid[u'x'])
                c.y = float(cuboid[u'y'])
                c.z = float(cuboid[u'z'])
                c.transform_id = int(cuboid[u'transformId'])
                if not numpy.isnan(cuboid[u'attribute']):
                    c.attribute = float(cuboid[u'attribute'])
                obj.append(c)
        if u"cylinders" in hff_data:
            for cylinder in hff_data[u"cylinders"]:
                c = SFFCylinder(new_obj=False)
                c.id = int(cylinder[u'id'])
                c.height = float(cylinder[u'height'])
                c.diameter = float(cylinder[u'diameter'])
                c.transform_id = int(cylinder[u'transformId'])
                if not numpy.isnan(cylinder[u'attribute']):
                    c.attribute = float(cylinder[u'attribute'])
                obj.append(c)
        return obj


class SFFVertex(SFFIndexType):
    """Single vertex"""
    gds_type = _sff.vertexType
    repr_string = u"SFFVertex(vID={}, designation={}, x={}, y={}, z={})"
    repr_args = (u'id', u'designation', u'x', u'y', u'z')
    vertex_id = 0
    index_attr = u'vertex_id'

    # attributes
    # fixme: rename `vID` to `id` for simplicity in schema
    id = SFFAttribute(u'vID', required=True, help=u"vertex ID; referenced by polygons")
    designation = SFFAttribute(u'designation', default='surface',
                               help=u"type of vertex ('surface' (default) or 'normal')")
    x = SFFAttribute(u'x', required=True, help=u"x co-ordinate")
    y = SFFAttribute(u'y', required=True, help=u"y co-ordinate")
    z = SFFAttribute(u'z', required=True, help=u"z co-ordinate")

    @property
    def point(self):
        """The co-ordinates for this vertex"""
        return self.x, self.y, self.z

    @point.setter
    def point(self, p):
        if isinstance(p, tuple):
            if len(p) == 3:
                self.x, self.y, self.z = p
            else:
                raise TypeError(u"point does not have three values")
        else:
            raise SFFTypeError(p, tuple)

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        attrs = [u'x', u'y', u'z']
        return all(list(map(lambda a: getattr(self, a) == getattr(other, a), attrs)))


class SFFPolygon(SFFListType, SFFIndexType):
    """Single polygon"""
    gds_type = _sff.polygonType
    repr_string = u"SFFPolygon(PID={}, v={})"
    repr_args = (u'id', u'vertices')
    iter_attr = (u'v', int)
    polygon_id = 0
    index_attr = u'polygon_id'

    # attributes
    # fixme: rename `PID` to `id` for simplicity in schema
    id = SFFAttribute(u'PID', required=True, help=u"the ID for this polygon")
    vertices = SFFAttribute(u'v', required=True, help=u"the list of vertices")

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return self.vertices == other.vertices


class SFFVertexList(SFFListType):
    """List of vertices"""
    gds_type = _sff.vertexListType
    repr_string = u"SFFVertexList({})"
    repr_args = (u'list()',)
    iter_attr = (u'v', SFFVertex)
    min_length = 3

    def __init__(self, **kwargs):
        super(SFFVertexList, self).__init__(**kwargs)
        self._vertex_dict = {v.vID: v for v in map(SFFVertex.from_gds_type, self._local.v)}

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return all(list(map(lambda v: v[0] == v[1], zip(self, other))))

    @property
    def num_vertices(self):
        """The number of vertices in this vertex container"""
        return len(self)

    @property
    def vertex_ids(self):
        """Iterable of vertex IDs contained in this vertex container"""
        return self.get_ids()

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Dataset)
        obj = cls()
        for vertex in hff_data:
            obj.append(
                SFFVertex(
                    vID=vertex[u'vID'],
                    designation=_decode(vertex[u'designation'], u'utf-8'),
                    x=float(vertex[u'x']),
                    y=float(vertex[u'y']),
                    z=float(vertex[u'z']),
                    new_obj=False
                )
            )
        return obj


class SFFPolygonList(SFFListType):
    """List of polygons"""
    gds_type = _sff.polygonListType
    repr_string = u"SFFPolygonList({})"
    repr_args = (u'list()',)
    iter_attr = (u'P', SFFPolygon)
    min_length = 1

    def __init__(self, **kwargs):
        super(SFFPolygonList, self).__init__(**kwargs)
        self._polygon_dict = {P.PID: P for P in list(map(SFFPolygon, self._local.P))}

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return all(list(map(lambda v: v[0] == v[1], zip(self, other))))

    @property
    def num_polygons(self):
        """The number of polygons in this list of polygons"""
        return len(self)

    @property
    def polygon_ids(self):
        """An iterable over the polygon IDs of the contained polygons"""
        return self.get_ids()

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Dataset)
        obj = cls()
        for polygon in hff_data:
            P = SFFPolygon(new_obj=False)
            P.PID = int(polygon[u'PID'])
            [P.append(int(_)) for _ in polygon[u'v']]
            obj.append(P)
        return obj


class SFFMesh(SFFIndexType):
    """Single mesh"""
    gds_type = _sff.meshType
    repr_string = u"SFFMesh(id={}, vertexList={}, polygonList={})"
    repr_args = (u'id', u'vertices', u'polygons')
    mesh_id = 0
    index_attr = u'mesh_id'

    # attributes
    id = SFFAttribute(u'id')
    vertices = SFFAttribute(u'vertexList', required=True, sff_type=SFFVertexList,
                            help=u"a list of vertices (object of class :py:class:`sfftkrw.schema.adapter.SFFVertexList`)")
    polygons = SFFAttribute(u'polygonList', required=True, sff_type=SFFPolygonList,
                            help=u"a list of derived polygons (object of class :py:class:`sfftkrw.schema.adapter.SFFPolygonList`)")
    transform_id = SFFAttribute(u'transformId', help=u"a transform applied to the mesh")

    @property
    def num_vertices(self):
        """The number of vertices in this mesh"""
        return len(self.vertices)

    @property
    def num_polygons(self):
        """The number of polygons in this mesh"""
        return len(self.polygons)

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        attrs = [u'vertices', u'polygons', u'transform_id']
        return all(list(map(lambda a: getattr(self, a) == getattr(other, a), attrs)))

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls(new_obj=False)
        obj.vertices = SFFVertexList.from_hff(hff_data[u'vertices'], args=args)
        obj.polygons = SFFPolygonList.from_hff(hff_data[u'polygons'], args=args)
        return obj


class SFFMeshList(SFFListType):
    """Mesh list representation"""
    gds_type = _sff.meshListType
    repr_string = u"SFFMeshList({})"
    repr_args = (u'list()',)
    iter_attr = (u'mesh', SFFMesh)

    def as_hff(self, parent_group, name=u"meshes", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        # structures
        vlen_str = h5py.special_dtype(vlen=_str)
        vertex_array = h5py.special_dtype(vlen=numpy.dtype(u'u4'))  # create a variable-length for vertices
        for mesh in self:
            # /sff/segments/1/meshes/0 - mesh 0
            h_mesh = group.create_group(u"{}".format(mesh.id))
            # /sff/segments/1/meshes/0/vertices
            h_v = h_mesh.create_dataset(
                u"vertices",
                (mesh.num_vertices,),
                dtype=[
                    (u'vID', u'u8'),
                    (u'designation', vlen_str),
                    (u'x', u'f4'),
                    (u'y', u'f4'),
                    (u'z', u'f4'),
                ],
            )
            # load vertex data
            i = 0
            for vertex in mesh.vertices:
                h_v[i] = (vertex.vID, vertex.designation, vertex.x, vertex.y, vertex.z)
                i += 1
            # /sff/segments/1/meshes/0/polygons
            h_P = h_mesh.create_dataset(
                u"polygons",
                (mesh.num_polygons,),
                dtype=[
                    (u'PID', u'u8'),
                    (u'v', vertex_array),
                ],
            )
            #  load polygon data
            j = 0
            for polygon in mesh.polygons:
                h_P[j] = (polygon.PID, numpy.array(polygon.vertex_ids))
                j += 1
            if mesh.transform_id:
                h_mesh[u"transformId"] = mesh.transform_id
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        for mesh_id in hff_data:
            M = SFFMesh.from_hff(hff_data[u"{}".format(mesh_id)], args=args)
            M.id = int(mesh_id)
            obj.append(M)
        return obj


class SFFSegment(SFFIndexType):
    """Class that encapsulates segment data"""
    gds_type = _sff.segmentType
    repr_string = u"""SFFSegment(id={}, parentID={}, biologicalAnnotation={}, colour={}, threeDVolume={}, meshList={}, shapePrimitiveList={})"""
    repr_args = (u'id', u'parent_id', u'biological_annotation', u'colour', u'volume', u'meshes', u'shapes')
    segment_id = 1
    segment_parentID = 0
    index_attr = u'segment_id'
    start_at = 1

    # attributes
    id = SFFAttribute(
        u'id',
        required=True,
        help=u"the ID for this segment; segment IDs begin at 1 with the value of 0 implying the segmentation "
             u"i.e. all segments are children of the root segment (the segmentation)"
    )
    parent_id = SFFAttribute(
        u'parentID',
        required=True,
        default=0,
        help=u"the ID for the segment that contains this segment; defaults to 0 (the whole segmentation)"
    )
    biological_annotation = SFFAttribute(u'biologicalAnnotation', sff_type=SFFBiologicalAnnotation,
                                         help=u"the biological annotation for this segment; described using a :py:class:`sfftkrw.schema.adapter.SFFBiologicalAnnotation` object")
    complexes_and_macromolecules = SFFAttribute(u'complexesAndMacromolecules', sff_type=SFFComplexesAndMacromolecules,
                                                help=u"the complexes and macromolecules associated with this segment; described using a :py:class:`sfftkrw.schema.adapter.SFFComplexesAndMacromolecules` object")
    colour = SFFAttribute(u'colour', sff_type=SFFRGBA, required=True,
                          help=u"this segments colour; described using a :py:class:`sfftkrw.schema.adapter.SFFRGBA` object")
    meshes = SFFAttribute(u'meshList', sff_type=SFFMeshList,
                          help=u"the list of meshes (if any) that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFMeshList` object")
    volume = SFFAttribute(u'threeDVolume', sff_type=SFFThreeDVolume,
                          help=u"the 3D volume (if any) that describes this segment; a :py:class:`sfftkrw.schema.adapter.SFFThreeDVolume` object ")
    shapes = SFFAttribute(u'shapePrimitiveList', sff_type=SFFShapePrimitiveList,
                          help=u"the list of shape primitives that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFShapePrimitiveList` object")

    def __init__(self, **kwargs):
        super(SFFSegment, self).__init__(**kwargs)
        # parentID
        # unlink segment_id, parentID is not managed by `SFFIndexType`
        if u'parentID' in kwargs:
            self._local.parentID = kwargs[u'parentID']
        else:
            self._local.parentID = self.segment_parentID

    def as_hff(self, parent_group, name=u"{}", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name.format(self.id))
        group[u'parentID'] = self.parent_id
        # add annotation data
        if self.biological_annotation:
            group = self.biological_annotation.as_hff(group, args=args)
        if self.complexes_and_macromolecules:
            group = self.complexes_and_macromolecules.as_hff(group, args=args)
        if self.colour:
            group = self.colour.as_hff(group, args=args)
        # add segmentation data
        if self.meshes:
            group = self.meshes.as_hff(group, args=args)
        if self.shapes:
            # /sff/segments/1/shapes
            h_shapes = group.create_group(u"shapes")
            # /sff/segments/1/shapes/ellipsoids
            h_ell = h_shapes.create_dataset(
                u"ellipsoids",
                (self.shapes.num_ellipsoids,),
                dtype=[
                    (u'id', u'u4'),
                    (u'x', u'f4'),
                    (u'y', u'f4'),
                    (u'z', u'f4'),
                    (u'transformId', u'u4'),
                    (u'attribute', u'f4'),
                ]
            )
            h_cub = h_shapes.create_dataset(
                u"cuboids",
                (self.shapes.num_cuboids,),
                dtype=[
                    (u'id', u'u4'),
                    (u'x', u'f4'),
                    (u'y', u'f4'),
                    (u'z', u'f4'),
                    (u'transformId', u'u4'),
                    (u'attribute', u'f4'),
                ]
            )

            h_cyl = h_shapes.create_dataset(
                u"cylinders",
                (self.shapes.num_cylinders,),
                dtype=[
                    (u'id', u'u4'),
                    (u'height', u'f4'),
                    (u'diameter', u'f4'),
                    (u'transformId', u'u4'),
                    (u'attribute', u'f4'),
                ]
            )

            h_con = h_shapes.create_dataset(
                u"cones",
                (self.shapes.num_cones,),
                dtype=[
                    (u'id', u'u4'),
                    (u'height', u'f4'),
                    (u'bottomRadius', u'f4'),
                    (u'transformId', u'u4'),
                    (u'attribute', u'f4'),
                ]
            )
            i = 0  # ellipsoid
            j = 0  # cuboid
            k = 0  # cylinder
            m = 0  # cone
            # n = 0 # subtomogram average
            for shape in self.shapes:
                if shape.gds_type == _sff.ellipsoid:  # u"ellipsoid":
                    h_ell[i] = (shape.id, shape.x, shape.y, shape.z, shape.transform_id,
                                shape.attribute if hasattr(shape, u'attribute') else None)
                    i += 1
                elif shape.gds_type == _sff.cuboid:  # u"cuboid":
                    h_cub[j] = (shape.id, shape.x, shape.y, shape.z, shape.transform_id,
                                shape.attribute if hasattr(shape, u'attribute') else None)
                    j += 1
                elif shape.gds_type == _sff.cylinder:  # u"cylinder":
                    h_cyl[k] = (shape.id, shape.height, shape.diameter, shape.transform_id,
                                shape.attribute if hasattr(shape, u'attribute') else None)
                    k += 1
                elif shape.gds_type == _sff.cone:  # u"cone":
                    h_con[m] = (shape.id, shape.height, shape.bottom_radius, shape.transform_id,
                                shape.attribute if hasattr(shape, u'attribute') else None)
                    m += 1
                # elif shape.gds_type == sff.threeDVolume: # u"Subtomogram average":
                #     warn(u"Unimplemented portion")
        if self.volume:
            # /sff/segments/1/volume
            group = self.volume.as_hff(group, args=args)
        return parent_group

    def as_json(self, args=None):
        """Format this segment as JSON"""
        seg_data = _dict()
        seg_data[u'id'] = int(self.id)
        seg_data[u'parentID'] = int(self.parent_id)
        if self.biological_annotation is not None:
            seg_data[u'biologicalAnnotation'] = self.biological_annotation.as_json(args=args)
        if self.complexes_and_macromolecules:
            complexes = list()
            for _complex in self.complexes_and_macromolecules.complexes:
                complexes.append(_complex)
            macromolecules = list()
            for macromolecule in self.complexes_and_macromolecules.macromolecules:
                macromolecules.append(macromolecule)
            seg_data[u'complexesAndMacromolecules'] = {
                u'complexes': complexes,
                u'macromolecules': macromolecules,
            }
        seg_data.update(self.colour.as_json(args=args))
        # seg_data[u'colour'] = tuple(map(float, self.colour.value))
        if self.meshes:
            seg_data[u'meshList'] = len(self.meshes)
        if self.shapes:
            seg_data[u'shapePrimitiveList'] = len(self.shapes)
        return seg_data

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        obj.parentID = int(hff_data[u'parentID'][()])
        if u"biologicalAnnotation" in hff_data:
            obj.biological_annotation = SFFBiologicalAnnotation.from_hff(hff_data[u"biologicalAnnotation"], args=args)
        if u"complexesAndMacromolecules" in hff_data:
            obj.complexes_and_macromolecules = SFFComplexesAndMacromolecules.from_hff(
                hff_data[u"complexesAndMacromolecules"], args=args)
        if u"colour" in hff_data:
            obj.colour = SFFRGBA.from_hff(hff_data, args=args)
        if u"meshes" in hff_data:
            obj.meshes = SFFMeshList.from_hff(hff_data[u"meshes"], args=args)
        if u"shapes" in hff_data:
            obj.shapes = SFFShapePrimitiveList.from_hff(hff_data[u"shapes"], args=args)
        if u"volume" in hff_data:
            obj.volume = SFFThreeDVolume.from_hff(hff_data[u"volume"], args=args)
        return obj

    @classmethod
    def from_json(cls, data, args=None):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'parentID' in data:
            obj.parent_id = data[u'parentID']
        if u'colour' in data:
            obj.colour = SFFRGBA.from_json(data, args=args)
        if u'biologicalAnnotation' in data:
            obj.biological_annotation = SFFBiologicalAnnotation.from_json(data[u'biologicalAnnotation'], args=args)
        if u'complexesAndMacromolecules' in data:
            obj.complexes_and_macromolecules = data[u'complexesAndMacromolecules']
        if u'meshList' in data:
            obj.meshes = data[u'meshList']
        if u'shapePrimitiveList' in data:
            obj.shapes = data[u'shapePrimitiveList']
        if u'threeDVolume' in data:
            obj.volume = data[u'threeDVolume']
        return obj


class SFFSegmentList(SFFListType):
    """Container for segments"""
    gds_type = _sff.segmentListType
    repr_string = u"SFFSegmentList({})"
    repr_args = (u'list()',)
    iter_attr = (u'segment', SFFSegment)

    def as_hff(self, parent_group, name=u"segments", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        for segment in self:
            group = segment.as_hff(group, args=args)
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        for segment_id in hff_data:
            S = SFFSegment.from_hff(hff_data[segment_id], args=args)
            S.id = int(segment_id)
            obj.append(S)
        return obj


class SFFTransformationMatrix(SFFIndexType):
    """Transformation matrix transform"""
    gds_type = _sff.transformationMatrixType
    gds_tag_name = u"transformationMatrix"
    repr_string = u"SFFTransformationMatrix(id={}, rows={}, cols={}, data={})"
    repr_args = (u'id', u'rows', u'cols', u'data')
    transform_id = 0
    index_attr = u'transform_id'

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
                self._data = kwargs[u'data']
                # make string from numpy array
                kwargs[u'data'] = SFFTransformationMatrix.stringify(kwargs[u'data'])
            elif isinstance(kwargs[u'data'], _str):
                # make numpy array from string
                self._data = numpy.array(list(map(float, kwargs[u'data'].split(' ')))).reshape(
                    kwargs[u'rows'],
                    kwargs[u'cols']
                )
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
        return u" ".join(list(map(_str, array.flatten().tolist())))

    @property
    def data_array(self):
        if not hasattr(self, u'_data'):
            # make numpy array from string
            self._data = numpy.array(list(map(float, self.data.split(' ')))).reshape(
                self.rows,
                self.cols
            )
        return self._data


class SFFTransformList(SFFListType):
    """Container for transforms"""
    gds_type = _sff.transformListType
    repr_string = u"SFFTransformList({})"
    repr_args = (u'list()',)
    iter_attr = (u'transform', SFFTransformationMatrix)

    @property
    def num_tranformation_matrices(self):
        """The number of :py:class:`SFFTransformationMatrix` objects in this transform container"""
        return len(self._local.transform)

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

    def as_hff(self, parent_group, name=u"transforms", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        # we need to check whether all transformation_matrices are of the same dimension
        # what we need to know:
        # - rows
        #  - cols
        # if they are then we just use rows and cols
        # else we should
        transformation_matrices_similar, rows, cols = self._check_transformation_matrix_homogeneity()
        if self.num_tranformation_matrices:
            if transformation_matrices_similar:
                h_tM = group.create_dataset(
                    u"transformationMatrix",
                    (self.num_tranformation_matrices,),
                    dtype=[
                        (u'id', u'u4'),
                        (u'rows', u'u1'),
                        (u'cols', u'u1'),
                        (u'data', u'f4', (rows, cols)),
                    ]
                )
            else:
                h_tM = group.create_group(u"transformationMatrix")
        i = 0  # h_tM index
        j = 0  # h_cEA index
        k = 0  # h_vVR index
        for transform in self:
            if transform.gds_type == _sff.transformationMatrixType:  # u"transformation_matrix":
                if transformation_matrices_similar:
                    h_tM[i] = (transform.id, transform.rows, transform.cols, transform.data_array)
                    i += 1
                else:
                    rows_, cols_ = transform.data_array.shape
                    tM = h_tM.create_dataset(
                        u"{}".format(transform.id),
                        (1,),
                        dtype=[
                            (u'id', u'u4'),
                            (u'rows', u'u1'),
                            (u'cols', u'u1'),
                            (u'data', u'f4', (rows_, cols_)),
                        ]
                    )
                    tM[0] = (transform.id, transform.rows, transform.cols, transform.data_array)
                    i += 1
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        if u"transformationMatrix" in hff_data:
            for _transform in hff_data[u'transformationMatrix']:
                if isinstance(hff_data[u'transformationMatrix'], h5py.Group):
                    transform = hff_data[u'transformationMatrix'][_transform][0]
                else:
                    transform = _transform
                T = SFFTransformationMatrix.from_array(transform[u'data'], new_obj=False)
                T.id = transform[u'id']
                obj.append(T)
        return obj


# todo: create a software list for software objects
class SFFSoftware(SFFType):
    """Class definition for specifying software used to create this segmentation

    .. py:attribute:: name

        The name of the software used

    .. py:attribute:: version

        The version string

    .. py:attribute:: processing_details

        Details of how the segmentation was produced
    """
    gds_type = _sff.softwareType
    repr_string = u"SFFSoftware(name={}, version={}, processingDetails={})"
    repr_args = (u'name', u'version', u'processing_details')

    # attributes
    name = SFFAttribute(u'name', required=True, help=u"the software/programmeu's name")
    version = SFFAttribute(u'version', help=u"the version used")
    processing_details = SFFAttribute(u'processingDetails',
                                      help=u"a description of how the data was processed to produce the segmentation")

    def as_hff(self, parent_group, name=u"software", args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        group[u'name'] = self.name if self.name else ''
        group[u'version'] = _str(self.version) if self.version else ''
        if self.processing_details:
            group[u'processingDetails'] = self.processing_details
        return parent_group

    def as_json(self, args=None):
        return {
            u'name': self.name if self.name else '',
            u'version': _str(self.version) if self.version else '',
            u'processingDetails': self.processing_details if self.processing_details else None
        }

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls()
        obj.name = _decode(hff_data[u'name'][()], u'utf-8')
        obj.version = _decode(hff_data[u'version'][()], u'utf-8')
        if u'processingDetails' in hff_data:
            obj.processing_details = _decode(hff_data[u'processingDetails'][()], u'utf-8')
        return obj


class SFFBoundingBox(SFFType):
    """Dimensions of bounding box"""
    #  config
    gds_type = _sff.boundingBoxType
    repr_string = u"SFFBoundingBox(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={})"
    repr_args = (u'xmin', u'xmax', u'ymin', u'ymax', u'zmin', u'zmax')

    # attributes
    xmin = SFFAttribute(u'xmin', default=0, help=u"minimum x co-ordinate value")
    xmax = SFFAttribute(u'xmax', help=u"maximum x co-ordinate value")
    ymin = SFFAttribute(u'ymin', default=0, help=u"minimum y co-ordinate value")
    ymax = SFFAttribute(u'ymax', help=u"maximum y co-ordinate value")
    zmin = SFFAttribute(u'zmin', default=0, help=u"minimum z co-ordinate value")
    zmax = SFFAttribute(u'zmax', help=u"maximum z co-ordinate value")

    # methods
    def as_hff(self, parent_group, name=u"boundingBox", args=None):
        """Bounding box as HDF5 group"""
        assert isinstance(parent_group, h5py.Group)
        group = parent_group.create_group(name)
        group[u'xmin'] = self.xmin
        group[u'xmax'] = self.xmax if self.xmax else 1.0
        group[u'ymin'] = self.ymin
        group[u'ymax'] = self.ymax if self.ymax else 1.0
        group[u'zmin'] = self.zmin
        group[u'zmax'] = self.zmax if self.zmax else 1.0
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Bounding box from HDF5 group"""
        _assert_or_raise(hff_data, h5py.Group)
        obj = cls(new_obj=False)
        if u'xmin' in hff_data:
            obj.xmin = hff_data[u'xmin'][()]
        if u'xmax' in hff_data:
            obj.xmax = hff_data[u'xmax'][()]
        if u'ymin' in hff_data:
            obj.ymin = hff_data[u'ymin'][()]
        if u'ymax' in hff_data:
            obj.ymax = hff_data[u'ymax'][()]
        if u'zmin' in hff_data:
            obj.zmin = hff_data[u'zmin'][()]
        if u'zmax' in hff_data:
            obj.zmax = hff_data[u'zmax'][()]
        return obj

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
        return obj


class SFFGlobalExternalReferenceList(SFFListType):
    """Container for global external references"""
    gds_type = _sff.globalExternalReferencesType
    repr_string = u"SFFGlobalExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return all(list(map(lambda v: v[0] == v[1], zip(self, other))))


class SFFSegmentation(SFFType):
    """Adapter class to make using the output of ``generateDS`` easier to use"""
    gds_type = _sff.segmentation
    repr_string = u"SFFSegmentation(name={})"
    repr_args = (u'name',)

    # attributes
    name = SFFAttribute(u'name', required=True, help=u"the name of this segmentation")
    version = SFFAttribute(u'version', required=True, help=u"EMDB-SFF version")
    software = SFFAttribute(
        u'software',
        sff_type=SFFSoftware,
        help=u"the software details used to generate this segmentation a :py:class:`sfftkrw.schema.adapter.SFFSoftware` object"
    )
    primary_descriptor = SFFAttribute(
        u'primaryDescriptor',
        required=True,
        help=u"the main type of representation used for this segmentation; "
             u"can be one of 'meshList', 'shapePrimitiveList' or 'threeDVolume'"
    )
    transforms = SFFAttribute(
        u'transformList',
        sff_type=SFFTransformList,
        help=u"a list of transforms; a :py:class:`sfftkrw.schema.adapter.SFFTransformList` object"
    )
    bounding_box = SFFAttribute(
        u'boundingBox',
        sff_type=SFFBoundingBox,
        help=u"the bounding box in which the segmentation sits; a :py:class:`sfftkrw.schema.adapter.SFFBoundingBox` object"
    )
    global_external_references = SFFAttribute(
        u'globalExternalReferences',
        sff_type=SFFGlobalExternalReferenceList,
        help=u"a list of external references that apply to the whole segmentation (global); "
             u"a :py:class:`sfftkrw.schema.adapter.SFFGlobalExternalReferences` object"
    )
    segments = SFFAttribute(
        u'segmentList',
        sff_type=SFFSegmentList,
        help=u"the list of annotated segments; a :py:class:`sfftkrw.schema.adapter.SFFSegmentList` object"
    )
    lattices = SFFAttribute(
        u'latticeList',
        sff_type=SFFLatticeList,
        help=u"the list of lattices (if any) containing 3D volumes referred to; "
             u"a :py:class:`sfftkrw.schema.adapter.SFFLatticeList` object"
    )
    details = SFFAttribute(
        u'details', help=u"any other details about this segmentation (free text)")

    @classmethod
    def from_file(cls, fn, args=None):
        """Instantiate an :py:class:`SFFSegmentations` object from a file name

        The file suffix determines how the data is extracted.

        :param str fn: name of a file hosting an EMDB-SFF-structured segmentation
        :return seg: the corresponding :py:class:`SFFSegmentation` object
        :rtype seg: :py:class:`SFFSegmentation`
        """
        seg = cls()
        if re.match(r'.*\.(sff|xml)$', fn, re.IGNORECASE):
            try:
                seg._local = _sff.parse(fn, silence=True)
            except IOError:
                print_date(_encode(u"File {} not found".format(fn), u'utf-8'))
                sys.exit(os.EX_IOERR)
        elif re.match(r'.*\.(hff|h5|hdf5)$', fn, re.IGNORECASE):
            with h5py.File(fn, u'r') as h:
                seg._local = seg.from_hff(h, args=args)._local
        elif re.match(r'.*\.json$', fn, re.IGNORECASE):
            seg._local = seg.from_json(fn, args=args)._local
        else:
            print_date(_encode(u"Invalid EMDB-SFF file name: {}".format(fn), u'utf-8'))
            sys.exit(os.EX_USAGE)
        return seg

    @property
    def num_global_external_references(self):
        """The number of global external references"""
        if self.global_external_references:
            return len(self.global_external_references)
        else:
            return 0

    def as_hff(self, parent_group, name=None, args=None):
        """Return the data of this object as an HDF5 group in the given parent group"""
        # fixme: use print_date(...) to notify the user
        assert isinstance(parent_group, h5py.File)
        if name:
            group = parent_group.create_group(name)
        else:
            group = parent_group
        group[u'name'] = self.name if self.name else ""
        group[u'version'] = self.version
        if self.primary_descriptor is None:
            print_date(_encode(u"Invalid segmentation: primary_descriptor required", u'utf-8'))
            return os.EX_DATAERR
        group[u'primaryDescriptor'] = self.primary_descriptor
        # if we are adding another group then donu't set dict style; just return the populated group
        if self.software is None:
            self.software = SFFSoftware(
                name=u"sfftk",
                version=SFFTKRW_VERSION,
            )
        group = self.software.as_hff(group, args=args)
        if self.transforms is None:
            self.transforms = SFFTransformList()
        group = self.transforms.as_hff(group, args=args)
        if self.bounding_box is None:
            self.bounding_box = SFFBoundingBox()
        group = self.bounding_box.as_hff(group, args=args)
        if self.global_external_references:
            vl_str = h5py.special_dtype(vlen=_str)
            h_gext = group.create_dataset(
                u"globalExternalReferences",
                (self.num_global_external_references,),
                dtype=[
                    (u'type', vl_str),
                    (u'otherType', vl_str),
                    (u'value', vl_str),
                    (u'label', vl_str),
                    (u'description', vl_str),
                ]
            )
            i = 0
            for g_ext_ref in self.global_external_references:
                h_gext[i] = (
                    g_ext_ref.type, g_ext_ref.other_type, g_ext_ref.value, g_ext_ref.label, g_ext_ref.description)
                i += 1
        if self.segments is None:
            self.segments = SFFSegmentList()
        group = self.segments.as_hff(group, args=args)
        if self.lattices is None:
            self.lattices = SFFLatticeList()
        group = self.lattices.as_hff(group, args=args)
        group[u'details'] = self.details if self.details else ''
        return parent_group

    @classmethod
    def from_hff(cls, hff_data, name=None, args=None):
        """Create an :py:class:`sfftkrw.schema.adapter.SFFSegmentation` object from HDF5 formatted data

        :param hff_data: an HDF5 File object
        :type hff_data: ``h5py.File``
        :return sff_seg: an EMDB-SFF segmentation
        :rtype sff_seg: :py:class:`sfftkrw.schema.adapter.SFFSegmentation`
        """
        assert isinstance(hff_data, h5py.File)
        obj = cls()
        try:
            obj.name = _decode(hff_data[u'name'][()], u'utf-8')
        except KeyError:
            print_date(_encode(u'Segmentation name not found. Please check that {} is a valid EMDB-SFF file'.format(
                hff_data.filename
            ), u'utf-8'))
            sys.exit(os.EX_DATAERR)
        obj.version = _decode(hff_data[u'version'][()], u'utf-8')
        obj.software = SFFSoftware.from_hff(hff_data[u'software'], args=args)
        obj.transforms = SFFTransformList.from_hff(hff_data[u'transforms'], args=args)
        obj.primary_descriptor = _decode(hff_data[u'primaryDescriptor'][()], u'utf-8')
        if u'boundingBox' in hff_data:
            obj.bounding_box = SFFBoundingBox.from_hff(hff_data[u'boundingBox'], args=args)
        else:
            obj.bounding_box = SFFBoundingBox()
        if u"globalExternalReferences" in hff_data:
            obj.global_external_references = SFFGlobalExternalReferenceList()
            for gref in hff_data[u'globalExternalReferences']:
                g = SFFExternalReference(new_obj=False)
                g.type, g.other_type, g.value, g.label, g.description = list(map(lambda g: _decode(g, u'utf-8'), gref))
                obj.global_external_references.append(g)
        obj.segments = SFFSegmentList.from_hff(hff_data[u'segments'], args=args)
        obj.lattices = SFFLatticeList.from_hff(hff_data[u'lattices'], args=args)
        obj.details = hff_data[u'details'][()]
        return obj

    def as_json(self, f, args=None):
        """Render an EMDB-SFF to JSON

        :param file f: open file handle
        :param bool annotation_only: only extract annotation information and do not render geometric data
        :param bool sort_keys: whether (default) or not to sort keys in the dictionaries
        :param int indent_width: indent width (default: 2)
        """
        # todo: also extract geometrical data
        sff_data = _dict()
        # can be simplified
        sff_data[u'name'] = self.name
        sff_data[u'version'] = self.version
        if self.software is None:
            self.software = SFFSoftware(
                name=u'sfftk',
                version=SFFTKRW_VERSION,
            )
        sff_data[u'software'] = self.software.as_json(args=args)
        sff_data[u'primaryDescriptor'] = self.primary_descriptor
        if self.details is not None:
            sff_data[u'details'] = _decode(self.details, u'utf-8')
        else:
            sff_data[u'details'] = None
        sff_data[u'transforms'] = list()
        sff_data[u'boundingBox'] = self.bounding_box.as_json(args=args) if self.bounding_box else None
        if self.global_external_references:
            global_external_references = list()
            for gextref in self.global_external_references:
                global_external_references.append({
                    u'type': gextref.type,
                    u'otherType': gextref.other_type,
                    u'value': gextref.value,
                    u'label': gextref.label,
                    u'description': gextref.description
                })
            sff_data[u'globalExternalReferences'] = global_external_references
        sff_data[u'segments'] = list()
        for segment in self.segments:
            sff_data[u'segments'].append(segment.as_json(args=args))
        # write to f
        with f:
            import json
            try:
                json_sort = args.json_sort
                json_indent = args.json_indent
            except AttributeError:
                json_sort = False
                json_indent = 2
            json.dump(sff_data, f, sort_keys=json_sort, indent=json_indent)

    @classmethod
    def from_json(cls, json_file, args=None):
        """Create an :py:class:`sfftkrw.schema.adapter.SFFSegmentation` object from JSON formatted data

        :param str json_file: name of a JSON-formatted file
        :return sff_seg: an EMDB-SFF segmentation
        :rtype sff_seg: :py:class:`sfftkrw.schema.adapter.SFFSegmentation`
        """
        with open(json_file) as j:
            import json
            J = json.load(j)
        sff_seg = cls()
        # header
        sff_seg.name = J[u'name']
        sff_seg.version = J[u'version']
        sff_seg.software = SFFSoftware(
            name=J[u'software'][u'name'],
            version=J[u'software'][u'version'],
            processingDetails=J[u'software'][u'processingDetails'],
        )
        sff_seg.primary_descriptor = J[u'primaryDescriptor']
        if u'boundingBox' in J:
            sff_seg.bounding_box = SFFBoundingBox.from_json(J[u'boundingBox'], args=args)
        if u'globalExternalReferences' in J:
            sff_seg.global_external_references = SFFGlobalExternalReferenceList()
            for gextref in J[u'globalExternalReferences']:
                try:
                    label = gextref[u'label']
                except KeyError:
                    label = None
                try:
                    description = gextref[u'description']
                except KeyError:
                    description = None
                sff_seg.global_external_references.append(
                    SFFExternalReference(
                        type=gextref[u'type'],
                        otherType=gextref[u'otherType'],
                        value=gextref[u'value'],
                        label=label,
                        description=description,
                    )
                )
        # segments
        segments = SFFSegmentList()
        for s in J[u'segments']:
            # fixme: move to respective contained classes
            r, g, b, a = s[u'colour']
            segment = SFFSegment()
            segment.id = s[u'id']
            segment.parentID = s[u'parentID']
            if u'biologicalAnnotation' in s:
                """
                biological_annotation = SFFBiologicalAnnotation()
                biological_annotation.name = s[u'biologicalAnnotation'][u'name']
                biological_annotation.description = s[u'biologicalAnnotation'][u'description']
                biological_annotation.number_of_instances = s[u'biologicalAnnotation'][u'numberOfInstances']
                if u'externalReferences' in s[u'biologicalAnnotation']:
                    biological_annotation.external_references = SFFExternalReferenceList()
                    for ext_ref in s[u'biologicalAnnotation'][u'externalReferences']:
                        try:
                            label = ext_ref[u'label']
                        except KeyError:
                            label = None
                        try:
                            description = ext_ref[u'description']
                        except KeyError:
                            description = None
                        external_reference = SFFExternalReference(
                            type=ext_ref[u'type'],
                            otherType=ext_ref[u'otherType'],
                            value=ext_ref[u'value'],
                            label=label,
                            description=description,
                        )
                        biological_annotation.external_references.append(external_reference)
                segment.biological_annotation = biological_annotation
                """
                segment.biological_annotation = SFFBiologicalAnnotation.from_json(s[u'biologicalAnnotation'], args=args)
            if u'complexesAndMacromolecules' in s:
                complexes_and_macromolecules = SFFComplexesAndMacromolecules()
                if u'complexes' in s[u'complexesAndMacromolecules']:
                    complexes = SFFComplexList()
                    complexes.ids = s[u'complexesAndMacromolecules'][u'complexes']
                    complexes_and_macromolecules.complexes = complexes
                if u'macromolecules' in s[u'complexesAndMacromolecules']:
                    macromolecules = SFFMacromoleculeList()
                    macromolecules.ids = s[u'complexesAndMacromolecules'][u'macromolecules']
                    complexes_and_macromolecules.macromolecules = macromolecules
                segment.complexes_and_macromolecules = complexes_and_macromolecules
            segment.colour = SFFRGBA(
                red=r,
                green=g,
                blue=b,
                alpha=a,
            )
            # in order for sff notes to work with JSON there should be an empty geom
            if u'meshList' in s:
                segment.meshes = SFFMeshList()
                for _ in _xrange(s[u'meshList']):
                    segment.meshes.append(SFFMesh())
            if u'threeDVolume' in s:
                # fixme: invalid model
                segment.volume = SFFThreeDVolume()
            if u'shapePrimitiveList' in s:
                segment.shapes = SFFShapePrimitiveList()
                for _ in _xrange(s[u'shapePrimitiveList']):
                    segment.shapes.append(SFFEllipsoid())
            segments.append(segment)
        sff_seg.segments = segments
        # details
        sff_seg.details = J[u'details']
        return sff_seg

    # todo: the following methods should be moved to sfftk from sfftk-rw
    def merge_annotation(self, other_seg):
        """Merge the annotation from another sff_seg to this one

        :param other_seg: segmentation to get annotations from
        :type other_seg: :py:class:`sfftk.schema.SFFSegmentation`
        """
        try:
            assert isinstance(other_seg, SFFSegmentation)
        except AssertionError:
            print_date(_encode(u"Invalid type for other_seg: {}".format(type(other_seg)), u'utf-8'))
            sys.exit(os.EX_DATAERR)
        # global data
        self.name = other_seg.name
        self.software = other_seg.software
        self.global_external_references = other_seg.global_external_references
        self.details = other_seg.details
        # loop through segments
        for segment in self.segments:
            other_segment = other_seg.segments.get_by_id(segment.id)
            segment.biological_annotation = other_segment.biological_annotation
            segment.complexes_and_macromolecules = other_segment.complexes_and_macromolecules

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
            self.global_external_references = SFFGlobalExternalReferenceList()
        else:
            segment = self.segments.get_by_id(from_id)
            segment.biological_annotation.external_references = SFFExternalReferenceList()
