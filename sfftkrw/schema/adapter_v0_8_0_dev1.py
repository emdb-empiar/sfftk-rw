# -*- coding: utf-8 -*-

import base64
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
from .base import SFFType, SFFIndexType, SFFAttribute, SFFListType, SFFTypeError
from ..core import _str, _encode, _bytes, _dict, _decode
from ..core.print_tools import print_date

# ensure that we can read/write encoded data
_sff.ExternalEncoding = u"utf-8"


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

    def as_hff(self, parent_group, name=u"colour"):
        """Return the data of this object as an HDF5 group in the given parent group"""
        assert isinstance(parent_group, h5py.Group)
        parent_group[name] = self.value
        return parent_group

    @classmethod
    def from_hff(cls, hff_data):
        """Return an SFFType object given an HDF5 object"""
        assert isinstance(hff_data, h5py.Group)
        obj = cls(new_obj=False)
        obj.value = hff_data[u'colour'][()]
        return obj

    def as_json(self):
        """Export as JSON"""
        return self.value

    @classmethod
    def from_json(cls, data):
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

    def as_json(self):
        e = dict()
        if self.id is not None:  # value can be 0 which would evaluate to `False`
            e[u'id'] = self.id
        if self.resource:
            e[u'resource'] = self.resource
        if self.url:
            e[u'url'] = self.url
        if self.accession:
            e[u'accession'] = self.accession
        if self.label:
            e[u'label'] = self.label
        if self.description:
            e[u'description'] = self.description
        return e

    @classmethod
    def from_json(cls, data):
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


class SFFExternalReferenceList(SFFListType):
    """Container for external references"""
    gds_type = _sff.external_referencesType
    gds_tag_name = u'external_references'
    repr_string = u"SFFExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def as_json(self):
        es = list()
        for extref in self:
            es.append(extref.as_json())
        return es

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        for extref in data:
            obj.append(SFFExternalReference.from_json(extref))
        return obj


class SFFGlobalExternalReferenceList(SFFListType):
    """Container for global external references"""
    gds_type = _sff.global_external_referencesType
    gds_tag_name = u'global_external_references'
    repr_string = u"SFFGlobalExternalReferenceList({})"
    repr_args = (u'list()',)
    iter_attr = (u'ref', SFFExternalReference)

    def as_json(self):
        ge = list()
        for extref in self:
            ge.append(extref.as_json())
        return ge

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        for extref in data:
            obj.append(SFFExternalReference.from_json(extref))
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
    external_references = SFFAttribute(u'external_references', sff_type=SFFExternalReferenceList,
                                       help=u"the set of external references")
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

    def as_json(self):
        return {
            u'name': self.name,
            u'description': self.description,
            u'number_of_instances': self.number_of_instances,
            u'external_references': self.external_references if self.external_references is not None else [],
        }
        # bio_ann = _dict()
        # if self.name:
        #     bio_ann[u'name'] = _str(self.name)
        # if self.description:
        #     bio_ann[u'description'] = _str(self.description)
        # if self.number_of_instances:
        #     bio_ann[u'number_of_instances'] = self.number_of_instances
        # if self.external_references:
        #     bio_ann[u'external_references'] = self.external_references.as_json()
        # return bio_ann

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if u'name' in data:
            obj.name = data[u'name']
        if u'description' in data:
            obj.description = data[u'description']
        if u'number_of_instances' in data:
            obj.number_of_instances = data[u'number_of_instances']
        if u'external_references' in data:
            obj.external_references = SFFExternalReferenceList.from_json(data[u'external_references'])
        # validate
        if obj._is_valid():
            return obj
        else:
            super(SFFBiologicalAnnotation, cls).from_json(data)


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

    def as_json(self, *args, **kwargs):
        return {
            u'lattice_id': self.lattice_id,
            u'value': self.value,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data, *args, **kwargs):
        obj = cls(new_obj=False)
        if u'lattice_id' in data:
            obj.lattice_id = data[u'lattice_id']
        if u'value' in data:
            obj.value = data[u'value']
        if u'transform_id' in data:
            obj.transform_id = data[u'transform_id']
        return obj


class SFFVolume(SFFType):
    """Class for represention 3-space dimension"""
    # attributes
    rows = SFFAttribute(u'rows', help=u"number of rows")
    cols = SFFAttribute(u'cols', help=u"number of columns")
    sections = SFFAttribute(u'sections', help=u"number of sections (sets of congruent row-column collections)")
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

        # def __eq__(self, other):
        self.attrs = [u'']
        # try:
        #     assert isinstance(other, type(self))
        # except AssertionError:
        #     raise SFFTypeError(other, type(self))
        # return self.rows == other.rows and self.cols == other.cols and self.sections == other.sections

    def as_json(self, *args, **kwargs):
        return {
            u'rows': self.rows,
            u'cols': self.cols,
            u'sections': self.sections,
        }

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if u'rows' in data:
            obj.rows = data[u'rows']
        if u'cols' in data:
            obj.cols = data[u'cols']
        if u'sections' in data:
            obj.sections = data[u'sections']
        return obj


class SFFVolumeStructure(SFFVolume):
    gds_type = _sff.volume_structure_type
    gds_tag_name = u'size'
    repr_string = u"SFFVolumeStructure(rows={}, cols={}, sections={})"
    repr_args = (u'rows', u'cols', u'sections')

    @property
    def voxel_count(self):
        """The number of voxels in this volume"""
        return self.cols * self.rows * self.sections


class SFFVolumeIndex(SFFVolume):
    """Class representing volume indices"""
    # todo: implement an iterator to increment indices correctly
    gds_type = _sff.volume_index_type
    gds_tag_name = u'start'
    repr_string = u"SFFVolumeIndex(rows={}, cols={}, sections={})"
    repr_args = (u'rows', u'cols', u'sections')


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

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'mode': self.mode,
            u'endianness': self.endianness,
            u'size': self.size.as_json() if self.size is not None else None,
            u'start': self.start.as_json() if self.start is not None else None,
            u'data': _decode(self.data, 'ASCII'),
        }

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'mode' in data:
            obj.mode = data[u'mode']
        if u'endianness' in data:
            obj.endianness = data[u'endianness']
        if u'size' in data:
            if data[u'size'] is not None:
                obj.size = SFFVolumeStructure.from_json(data[u'size'])
            else:
                obj.size = None
        if u'start' in data:
            if data[u'start'] is not None:
                obj.start = SFFVolumeIndex.from_json(data[u'start'])
            else:
                obj.start = None
        if u'data' in data:  # lazy for numpy
            obj.data = _encode(data[u'data'], 'ASCII')
        return obj


class SFFLatticeList(SFFListType):
    """A container for lattice objects"""
    gds_type = _sff.lattice_listType
    gds_tag_name = u'lattice_list'
    repr_string = u"SFFLatticeList({})"
    repr_args = (u"list()",)
    iter_attr = (u'lattice', SFFLattice)

    def as_json(self, *args, **kwargs):
        llist = list()
        for lattice in self:
            llist.append(lattice.as_json())
        return llist

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        for lattice in data:
            obj.append(SFFLattice.from_json(lattice))
        return obj


class SFFEncodedSequence(SFFType):
    """Superclass for `SFFVertices`, `SFFNormals` and `SFFTriangles`"""
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
            elif isinstance(kwargs[u'data'], _bytes):
                self._data = self._decode(kwargs[u'data'], **kwargs)
                # make sure the number of items is correct
                try:
                    assert self._data.shape[0] == kwargs.get(self.num_items_kwarg)
                except AssertionError:
                    raise ValueError(
                        u"mismatch in stated in retrieved number of items: {}/{}".format(
                            kwargs.get(self.num_items_kwarg),
                            self._data.shape[0]))
            elif isinstance(kwargs[u'data'], _str):
                _data = _encode(kwargs[u'data'], u'ASCII')
                self._data = SFFEncodedSequence._decode(_data, **kwargs)
                # make sure the number of items is correct
                try:
                    assert self._data.shape[0] == kwargs.get(self.num_items_kwarg)
                except AssertionError:
                    raise ValueError(
                        u"mismatch in stated in retrieved number of items: {}/{}".format(kwargs[self.num_items_kwarg],
                                                                                         self._data.shape[0]))
                kwargs[u'data'] = _data
                del _data
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
        if isinstance(byte_seq, _str):  # if unicode convert to bytes
            byte_seq = _encode(byte_seq, u'ASCII')
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
        :return bytes: the corresponding bytes sequence
        """
        if mode is None:
            mode = SFFEncodedSequence.default_mode
        if endianness is None:
            endianness = SFFEncodedSequence.default_endianness
        array_in_mode_and_endianness = array.astype(
            '{}{}'.format(ENDIANNESS[endianness], FORMAT_CHARS[mode]))  # cast to required mode
        return base64.b64encode(array_in_mode_and_endianness.tobytes())

    @staticmethod
    def _decode(bin64, mode=None, endianness=None, **kwargs):
        """Decode a base64-encoded byte sequence to a numpy array

        :param str bin64: the base64-encoded byte sequence
        :param str mode: the data type
        :param str endianness: the byte orientation
        :return: a :py:class:`numpy.ndarray` object
        :rtype: :py:class:`numpy.ndarray`
        """
        if mode is None:
            mode = SFFEncodedSequence.default_mode
        if endianness is None:
            endianness = SFFEncodedSequence.default_endianness
        binpack = base64.b64decode(bin64)
        dt = numpy.dtype('{}{}'.format(ENDIANNESS[endianness], FORMAT_CHARS[mode]))
        unpacked = numpy.frombuffer(binpack, dtype=dt)
        return unpacked.reshape(-1, 3)  # leave first value to be auto-filled

    def as_json(self, *args, **kwargs):
        return {
            self.num_items_kwarg: getattr(self, self.num_items_kwarg),
            u'mode': self.mode,
            u'endianness': self.endianness,
            u'data': _decode(self.data, 'ASCII'),
        }

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if cls.num_items_kwarg in data:
            setattr(obj, cls.num_items_kwarg, data[cls.num_items_kwarg])
        if u'mode' in data:
            obj.mode = data[u'mode']
        if u'endianness' in data:
            obj.endianness = data[u'endianness']
        if u'data' in data:
            obj.data = _encode(data[u'data'], 'ASCII')
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
    id = SFFAttribute(u'id')
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
        # todo: device better test for this
        # indexes = set(kwargs['triangles'].data_array.flatten().tolist())
        # try:
        #     assert (kwargs['vertices'].num_vertices - 1) in indexes
        # except AssertionError:
        #     raise ValueError("incompatible vertex and triangle lists")
        super(SFFMesh, self).__init__(**kwargs)

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'vertices': self.vertices.as_json(),
            u'normals': self.normals.as_json() if self.normals is not None else None,
            u'triangles': self.triangles.as_json(),
        }

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'vertices' in data:
            obj.vertices = SFFVertices.from_json(data[u'vertices'])
        if u'normals' in data:
            obj.normals = SFFNormals.from_json(data[u'normals'])
        if u'triangles' in data:
            obj.triangles = SFFTriangles.from_json(data[u'triangles'])
        return obj


class SFFMeshList(SFFListType):
    """Mesh list representation"""
    gds_type = _sff.mesh_listType
    gds_tag_name = u'mesh_list'
    repr_string = u"SFFMeshList({})"
    repr_args = (u'list()',)
    iter_attr = (u'mesh', SFFMesh)

    def as_json(self, *args, **kwargs):
        mlist = list()
        for mesh in self:
            mlist.append(mesh.as_json())
        return mlist

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        for mesh in data:
            obj.append(SFFMesh.from_json(mesh))
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
    repr_string = u"SFFCone(id={}, height={}, bottom_radius={}, transform_id={})"
    repr_args = (u'id', u'height', u'bottom_radius', u'transform_id')
    eq_attrs = [u'height', u'bottom_radius']

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cone height")
    bottom_radius = SFFAttribute(u'bottom_radius', required=True, help=u"cone bottom radius")

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'shape': u'cone',
            u'height': self.height,
            u'bottom_radius': self.bottom_radius,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data):
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
                raise SFFTypeError(u"cannot convert shape '{}' into ellipsoid".format(data[u'type']))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFCuboid(SFFShape):
    """Cuboid shape class"""
    gds_type = _sff.cuboid
    gds_tag_name = u"cuboid"
    repr_string = u"SFFCuboid(id={}, x={}, y={}, z={}, transform_id={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id')
    eq_attrs = [u'x', u'y', u'z']

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'shape': u'cuboid',
            u'x': self.x,
            u'y': self.y,
            u'z': self.z,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data):
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
                raise SFFTypeError(u"cannot convert shape '{}' into cuboid".format(data[u'type']))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFCylinder(SFFShape):
    """Cylinder shape class"""
    gds_type = _sff.cylinder
    gds_tag_name = u"cylinder"
    repr_string = u"SFFCylinder(id={}, height={}, diameter={}, transform_id={})"
    repr_args = (u'id', u'height', u'diameter', u'transform_id')
    eq_attrs = [u'height', u'diameter']

    # attributes
    height = SFFAttribute(u'height', required=True, help=u"cylinder height")
    diameter = SFFAttribute(u'diameter', required=True, help=u"cylinder diameter")

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'shape': u'cylinder',
            u'height': self.height,
            u'diameter': self.diameter,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data):
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
                raise SFFTypeError(u"cannot convert shape '{}' into cylinder".format(data[u'type']))
        else:
            raise ValueError(u"missing 'shape' attribute")


class SFFEllipsoid(SFFShape):
    """Ellipsoid shape class"""
    gds_type = _sff.ellipsoid
    gds_tag_name = u"ellipsoid"
    repr_string = u"SFFEllipsoid(id={}, x={}, y={}, z={}, transform_id={})"
    repr_args = (u'id', u'x', u'y', u'z', u'transform_id')
    eq_attrs = [u'x', u'y', u'z']

    # attributes
    x = SFFAttribute(u'x', required=True, help=u"length in x")
    y = SFFAttribute(u'y', required=True, help=u"length in y")
    z = SFFAttribute(u'z', required=True, help=u"length in z")

    def as_json(self, *args, **kwargs):
        return {
            u'id': self.id,
            u'shape': u'ellipsoid',
            u'x': self.x,
            u'y': self.y,
            u'z': self.z,
            u'transform_id': self.transform_id,
        }

    @classmethod
    def from_json(cls, data):
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
                raise SFFTypeError(u"cannot convert shape '{}' into ellipsoid".format(data[u'type']))
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

    def as_json(self, *args, **kwargs):
        slist = list()
        for shape in self:
            slist.append(shape.as_json())
        return slist

    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        for shape in data:
            if u'shape' in shape:
                if shape[u'shape'] == u'cone':
                    obj.append(SFFCone.from_json(shape))
                elif shape[u'shape'] == u'cuboid':
                    obj.append(SFFCuboid.from_json(shape))
                elif shape[u'shape'] == u'cylinder':
                    obj.append(SFFCylinder.from_json(shape))
                elif shape[u'shape'] == u'ellipsoid':
                    obj.append(SFFEllipsoid.from_json(shape))
                else:
                    raise SFFTypeError(u"cannot convert shape '{}' into ellipsoid".format(data[u'type']))
            else:
                raise ValueError(u"missing 'shape' attribute")
        return obj


class SFFSegment(SFFIndexType):
    """Class that encapsulates segment data"""
    gds_type = _sff.segment_type
    gds_tag_name = u'segment'
    repr_string = u"""SFFSegment(id={}, parent_id={}, biological_annotation={}, colour={}, three_d_volume={}, mesh_list={}, shape_primitive_list={})"""
    repr_args = (u'id', u'parent_id', u'biological_annotation', u'colour', u'volume', u'meshes', u'shapes')
    segment_id = 1
    segment_parent_id = 0
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
        u'parent_id',
        required=True,
        default=0,
        help=u"the ID for the segment that contains this segment; defaults to 0 (the whole segmentation)"
    )
    biological_annotation = SFFAttribute(u'biological_annotation', sff_type=SFFBiologicalAnnotation,
                                         help=u"the biological annotation for this segment; described using a :py:class:`sfftkrw.schema.adapter.SFFBiologicalAnnotation` object")
    colour = SFFAttribute(u'colour', sff_type=SFFRGBA, required=True,
                          help=u"this segments colour; described using a :py:class:`sfftkrw.schema.adapter.SFFRGBA` object")
    meshes = SFFAttribute(u'mesh_list', sff_type=SFFMeshList,
                          help=u"the list of meshes (if any) that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFMeshList` object")
    volume = SFFAttribute(u'three_d_volume', sff_type=SFFThreeDVolume,
                          help=u"the 3D volume (if any) that describes this segment; a :py:class:`sfftkrw.schema.adapter.SFFThreeDVolume` object ")
    shapes = SFFAttribute(u'shape_primitive_list', sff_type=SFFShapePrimitiveList,
                          help=u"the list of shape primitives that describe this segment; a :py:class:`sfftkrw.schema.adapter.SFFShapePrimitiveList` object")

    def as_json(self):
        """Format this segment as JSON"""
        return {
            u'id': self.id,
            u'parent_id': self.parent_id,
            u'biological_annotation': self.biological_annotation.as_json() if self.biological_annotation is not None else None,
            u'colour': self.colour.as_json(),
            u'mesh_list': self.meshes.as_json() if self.meshes is not None else [],
            u'three_d_volume': self.volume.as_json() if self.volume is not None else None,
            u'shape_primitive_list': self.shapes.as_json() if self.shapes is not None else []
        }
        # seg_data = _dict()
        # seg_data[u'id'] = int(self.id)
        # seg_data[u'parent_id'] = int(self.parent_id)
        # if self.biological_annotation is not None:
        #     seg_data[u'biological_annotation'] = self.biological_annotation.as_json()
        # seg_data.update(self.colour.as_json())
        seg_data[u'colour'] = tuple(map(float, self.colour.value))
        # if self.meshes:
        #     seg_data[u'mesh_list'] = len(self.meshes)
        # if self.shapes:
        #     seg_data[u'shape_primitive_list'] = len(self.shapes)
        # return seg_data


    @classmethod
    def from_json(cls, data):
        obj = cls(new_obj=False)
        if u'id' in data:
            obj.id = data[u'id']
        if u'parent_id' in data:
            obj.parent_id = data[u'parent_id']
        if u'colour' in data:
            obj.colour = SFFRGBA.from_json(data)
        if u'biological_annotation' in data:
            obj.biological_annotation = SFFBiologicalAnnotation.from_json(data[u'biological_annotation'])
        if u'mesh_list' in data:
            obj.meshes = data[u'mesh_list']
        if u'shape_primitive_list' in data:
            obj.shapes = data[u'shape_primitive_list']
        if u'threeDVolume' in data:
            obj.volume = data[u'threeDVolume']
        # validate
        if obj._is_valid():
            return obj
        else:
            super(SFFSegment, cls).from_json(data)

class SFFSegmentList(SFFListType):
    """Container for segments"""
    gds_type = _sff.segment_listType
    gds_tag_name = u'segment_list'
    repr_string = u"SFFSegmentList({})"
    repr_args = (u'list()',)
    iter_attr = (u'segment', SFFSegment)


class SFFTransformationMatrix(SFFIndexType):
    """Transformation matrix transform"""
    gds_type = _sff.transformation_matrix_type
    gds_tag_name = u"transformation_matrix"
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

    # attributes
    id = SFFAttribute(u'id', help=u"the software ID")
    name = SFFAttribute(u'name', required=True, help=u"the software/programmeu's name")
    version = SFFAttribute(u'version', help=u"the version used")
    processing_details = SFFAttribute(u'processing_details',
                                      help=u"a description of how the data was processed to produce the segmentation")

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version and \
               self.processing_details == other.processing_details


class SFFSoftwareList(SFFListType):
    """List of SFFSoftware objects"""
    gds_type = _sff.software_listType
    gds_tag_name = u'software_list'
    repr_string = u"SFFSoftwareList({})"
    repr_args = (u'list()',)
    iter_attr = (u'software', SFFSoftware)


class SFFBoundingBox(SFFType):
    """Dimensions of bounding box"""
    #  config
    gds_type = _sff.bounding_box_type
    gds_tag_name = u'bounding_box'
    repr_string = u"SFFBoundingBox(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={})"
    repr_args = (u'xmin', u'xmax', u'ymin', u'ymax', u'zmin', u'zmax')

    # attributes
    xmin = SFFAttribute(u'xmin', default=0, help=u"minimum x co-ordinate value")
    xmax = SFFAttribute(u'xmax', help=u"maximum x co-ordinate value")
    ymin = SFFAttribute(u'ymin', default=0, help=u"minimum y co-ordinate value")
    ymax = SFFAttribute(u'ymax', help=u"maximum y co-ordinate value")
    zmin = SFFAttribute(u'zmin', default=0, help=u"minimum z co-ordinate value")
    zmax = SFFAttribute(u'zmax', help=u"maximum z co-ordinate value")

    def as_json(self):
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
    def from_json(cls, data):
        obj = cls(new_obj=False)
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
        if obj._is_valid():
            return obj
        else:
            super(SFFBoundingBox, cls).from_json(data)


class SFFSegmentation(SFFType):
    """Adapter class to make using the output of ``generateDS`` easier to use"""
    gds_type = _sff.segmentation
    gds_tag_name = u'segmentation'
    repr_string = u"SFFSegmentation(name={})"
    repr_args = (u'name',)

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
    transforms = SFFAttribute(
        u'transform_list',
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
    segments = SFFAttribute(
        u'segment_list',
        sff_type=SFFSegmentList,
        help=u"the list of annotated segments; a :py:class:`sfftkrw.schema.adapter.SFFSegmentList` object"
    )
    lattices = SFFAttribute(
        u'lattice_list',
        sff_type=SFFLatticeList,
        help=u"the list of lattices (if any) containing 3D volumes referred to; "
             u"a :py:class:`sfftkrw.schema.adapter.SFFLatticeList` object"
    )
    details = SFFAttribute(
        u'details', help=u"any other details about this segmentation (free text)")

    @classmethod
    def from_file(cls, fn):
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
        #     elif re.match(r'.*\.(hff|h5|hdf5)$', fn, re.IGNORECASE):
        #         with h5py.File(fn, u'r') as h:
        #             seg._local = seg.from_hff(h)._local
        #     elif re.match(r'.*\.json$', fn, re.IGNORECASE):
        #         seg._local = seg.from_json(fn)._local
        else:
            print_date(_encode(u"Invalid EMDB-SFF file name: {}".format(fn), u'utf-8'))
            sys.exit(os.EX_DATAERR)
        return seg
