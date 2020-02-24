# -*- coding: utf-8 -*-
# test_adapter.py
"""
Unit for schema adapter
"""
from __future__ import print_function

import importlib
import os
import random
import sys
import tempfile

import numpy
from random_words import RandomWords, LoremIpsum

rw = RandomWords()
li = LoremIpsum()

from . import _random_integer, Py23FixTestCase, _random_float, _random_floats
from .. import EMDB_SFF_VERSION
from ..core import _xrange, _str, _print
from ..schema import base  # , emdb_sff

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
# dynamically import the adapter for the API
adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
emdb_sff = importlib.import_module(emdb_sff_name)
adapter = importlib.import_module(adapter_name)


class TestSFFTypeError(Py23FixTestCase):
    """Tests for the exception"""

    def test_default(self):
        """Test default operation"""
        c = adapter.SFFRGBA()
        with self.assertRaisesRegex(base.SFFTypeError, r".*?is not object of type.*?"):
            c == adapter.SFFSegment()

    def test_message(self):
        """Test error raised with message"""
        v = adapter.SFFVolumeStructure()
        with self.assertRaisesRegex(base.SFFTypeError, r"should be of length 3"):
            v.value = (1, 2)


class TestSFFType(Py23FixTestCase):
    """Tests for the main base class"""

    def test_create_segmentation(self):
        """Test that a created empty segmentation has the correct version"""
        S = adapter.SFFSegmentation()
        _S = emdb_sff.segmentation()
        self.assertEqual(S.version, _S.schema_version)

    def test_gds_type_missing(self):
        """Test for presence of `gds_type` attribute"""

        class _SomeEntity(base.SFFType):
            """Empty entity"""

        with self.assertRaisesRegex(ValueError, r'.*gds_type.*'):
            _s = _SomeEntity()

    def test_create_from_gds_type(self):
        """Test creating an `SFFType` subclass object from a `gds_type' object"""
        # we will try with SFFRGBA and rgba_type
        red = _random_float()
        green = _random_float()
        blue = _random_float()
        _r = emdb_sff.rgba_type(
            red=red, green=green, blue=blue,
        )
        r = adapter.SFFRGBA.from_gds_type(_r)
        self.assertIsInstance(r, adapter.SFFRGBA)
        self.assertEqual(r.red, red)
        self.assertEqual(r.green, green)
        self.assertEqual(r.blue, blue)
        # from None returns None
        r = adapter.SFFRGBA.from_gds_type()
        self.assertIsNone(r)

    def test_create_from_gds_type_raises_error(self):
        """Test that we get an exception when the `SFFType` subclass object's `gds_type` attribute is not the same
        as the one provided"""
        _r = emdb_sff.biological_annotationType()
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            r = adapter.SFFRGBA.from_gds_type(_r)

    def test_ref_attr(self):
        """Test the `gds_tag_name` attribute"""
        c = adapter.SFFRGBA(
            red=1, green=1, blue=0, alpha=0.5
        )
        r = repr(c)
        self.assertRegex(r, r"\(.*\d+,.*\)")

    def test_repr_string_repr_args(self):
        """Test the string representation using `repr_string` and `repr_args`"""
        # correct rendering for colour: prints out repr_string filled with repr_args
        c = adapter.SFFRGBA(random_colour=True)
        self.assertRegex(_str(c), r"SFFRGBA\(red=\d\.\d+.*\)")
        # correct assessment of length: prints out a string with the correct len() value
        c = adapter.SFFSoftwareList()
        c.id = rw.random_words(count=10)
        self.assertRegex(_str(c), r"SFFSoftwareList\(\[.*\]\)")
        # plain string: prints the plain string
        v = adapter.SFFThreeDVolume()
        self.assertRegex(_str(v), r"""SFFThreeDVolume\(lattice_id=None, value=None, transform_id=None\)""")

        # len() works
        class _SoftwareList(adapter.SFFSoftwareList):
            repr_string = u'software list of length {}'
            repr_args = (u'len()',)

        Sw = _SoftwareList()
        no_sw = _random_integer(start=2, stop=10)
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(no_sw)]
        self.assertRegex(_str(Sw), r".*{}.*".format(no_sw))

        # using index syntax
        class _Lattice(adapter.SFFLattice):
            repr_string = u"{}"
            repr_args = (u"data[:20]",)

        L = _Lattice.from_array(numpy.random.randint(0, 10, size=(5, 5, 5)),
                                size=adapter.SFFVolumeStructure(rows=5, cols=5, sections=5))
        self.assertRegex(_str(L), r"\".*\.\.\.\"")

        # no repr_args
        class _Complexes(adapter.SFFSoftwareList):
            repr_string = u"complexes"
            repr_args = ()

        Sw = _Complexes()
        self.assertEqual(_str(Sw), u"complexes")

        # repr_str is missing: prints out the output of type
        class _RGBA(adapter.SFFRGBA):
            repr_string = ""

        _c = _RGBA(random_colour=True)
        self.assertRegex(str(_c), r".class.*_RGBA.*")

        # unmatched repr_args (it should be a tuple of four values)
        class _RGBA(adapter.SFFRGBA):
            repr_args = (u'red', u'green')

        _c = _RGBA(random_colour=True)
        with self.assertRaisesRegex(ValueError, r'Unmatched number.*'):
            str(_c)

    def test_export_xml(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = u'test segmentation'
        S.primary_descriptor = u'mesh_list'
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.sff'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S, _S)

    def test_export_hdf5(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = u'test segmentation'
        S.primary_descriptor = u'mesh_list'
        S.software = adapter.SFFSoftware()
        S.transforms = adapter.SFFTransformList()
        S.bounding_box = adapter.SFFBoundingBox()
        S.global_external_references = adapter.SFFGlobalExternalReferenceList()
        S.segments = adapter.SFFSegmentList()
        S.lattices = adapter.SFFLatticeList()
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += u'.hff'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S, _S)

    def test_export_json(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = u'test segmentation'
        S.primary_descriptor = u'mesh_list'
        S.software = adapter.SFFSoftware()
        S.transforms = adapter.SFFTransformList()
        S.bounding_box = adapter.SFFBoundingBox()
        S.global_external_references = adapter.SFFGlobalExternalReferenceList()
        S.segments = adapter.SFFSegmentList()
        S.lattices = adapter.SFFLatticeList()
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.json'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S, _S)

    def test_export_stderr(self):
        """Test that we can export to stderr"""
        S = adapter.SFFSegmentation(
            name=rw.random_word(),
            primary_descriptor=u'mesh_list',
        )
        # we check that everything was OK
        self.assertEqual(S.export(sys.stderr), os.EX_OK)

    def test_export_errors(self):
        """Test that we catch all export errors"""
        tf = tempfile.NamedTemporaryFile()
        tf.name += u'.invalid'
        self.assertEqual(os.EX_DATAERR,
                         adapter.SFFSegmentation(name=rw.random_word(), primary_descriptor=u'mesh_list').export(
                             tf.name))

    def test_format_method_missing(self):
        """Test that we get `NotImplementedError`s"""

        class _SomeEntity(base.SFFType):
            """Empty entity"""
            gds_type = emdb_sff.segmentation

        _S = _SomeEntity()
        with self.assertRaises(NotImplementedError):
            _S.as_hff(u'test')

        with self.assertRaises(NotImplementedError):
            _S.from_hff(u'test')

    def test_validation(self):
        """Test validation check"""
        s = adapter.SFFSegment(colour=adapter.SFFRGBA(random_colour=True))
        self.assertTrue(s._is_valid())
        s = adapter.SFFSegment(colour=adapter.SFFRGBA(random_colour=True), new_obj=False)
        self.assertFalse(s._is_valid())

    def test_eq_attrs(self):
        """Test the attribute that is a list of attributes for equality testing"""

        class _SomeEntity(adapter.SFFBoundingBox):
            eq_attrs = [u'xmin', u'xmax']
            # we test equality of bounding boxes only on xmin and xmax

        # equal
        b1 = _SomeEntity(xmin=1, xmax=2)
        b2 = _SomeEntity(xmin=1, xmax=2)
        self.assertEqual(b1, b2)
        # not equal
        b1 = _SomeEntity(xmin=1, xmax=2)
        b2 = _SomeEntity(xmin=0, xmax=2)
        self.assertNotEqual(b1, b2)

        # when not defined we get False by default
        class _SomeEntity(adapter.SFFBoundingBox):
            """eq_attrs is empty by default"""
            eq_attrs = []

        b1 = _SomeEntity(xmin=1)
        b2 = _SomeEntity(xmin=1)
        self.assertNotEqual(b1, b2)

        # exception: we can't compare things that are not of the same type
        with self.assertRaises(base.SFFTypeError):
            s = adapter.SFFSegment()
            b1 == s


class TestSFFIndexType(Py23FixTestCase):
    """Test the indexing mixin class `SFFIndexType"""

    def setUp(self):
        """Reset ids"""
        adapter.SFFSegment.segment_id = 1  # reset ID informarly
        adapter.SFFShape.shape_id = 0

    def test_create_from_gds_type(self):
        """Test creating an `SFFIndexType` subclass object from a gds type"""
        # segment
        _s = emdb_sff.segment_type()
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        _t = emdb_sff.segment_type(id=10)
        t = adapter.SFFSegment.from_gds_type(_t)
        self.assertEqual(t.id, 10)
        u = adapter.SFFSegment.from_gds_type(None)
        self.assertIsNone(u)
        with self.assertRaises(adapter.SFFTypeError):
            adapter.SFFSegment.from_gds_type([])

    def test_explicit_set_id(self):
        """Test that we can explicitly set ID apart from incrementing"""
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment(id=999)
        self.assertEqual(s.id, 999)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1000)

    def test_new_obj_True(self):
        """Test that an empty `SFFIndexType` subclass has correct indexes"""
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment(new_obj=True)  # verbose: `new_obj=True` by default
        self.assertEqual(s.id, 2)

    def test_new_obj_False(self):
        """Test that `new_obj=False` for empty `SFFIndexType` subclass has None for ID"""
        s = adapter.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)

    def test_proper_incrementing(self):
        """Test that proper incrementing with and without `new_obj=False/True`"""
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 2)
        s = adapter.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 3)
        s = adapter.SFFSegment(new_obj=True)
        self.assertEqual(s.id, 4)
        s = adapter.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 5)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segment_type(id=35))
        self.assertEqual(s.id, 35)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segment_type())
        self.assertIsNone(s.id)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 6)

    def test_with_gds_type(self):
        """Test that we can work with generateDS types"""
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segment_type())
        self.assertIsNone(s.id)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segment_type(id=37))
        self.assertIsNotNone(s.id)
        self.assertEqual(adapter.SFFSegment.segment_id, 1)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segment_type(id=38))
        self.assertEqual(adapter.SFFSegment.segment_id, 1)

    def test_reset_id(self):
        """Test that we can reset the ID"""
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 2)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 3)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 4)
        adapter.SFFSegment.reset_id()
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 2)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 3)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 4)

    def test_index_in_super(self):
        """Test that indexes work correctly in subclasses"""
        cone = adapter.SFFCone()
        cuboid = adapter.SFFCuboid()
        cylinder = adapter.SFFCylinder()
        ellipsoid = adapter.SFFEllipsoid()
        self.assertEqual(cone.shape_id, 0)
        self.assertEqual(cuboid.shape_id, 1)
        self.assertEqual(cylinder.shape_id, 2)
        self.assertEqual(ellipsoid.shape_id, 3)
        cone = adapter.SFFCone()
        cuboid = adapter.SFFCuboid()
        cylinder = adapter.SFFCylinder()
        ellipsoid = adapter.SFFEllipsoid()
        self.assertEqual(cone.shape_id, 4)
        self.assertEqual(cuboid.shape_id, 5)
        self.assertEqual(cylinder.shape_id, 6)
        self.assertEqual(ellipsoid.shape_id, 7)

    def test_index_in_super_error(self):
        """Test that we get an `AttributeError` when `update_counter` is missing"""

        class _Shape(base.SFFIndexType, base.SFFType):
            repr_string = "{} {}"
            repr_args = ('ref', 'id')
            shape_id = 0
            index_attr = 'shape_id'
            index_in_super = True

            # attributes
            id = base.SFFAttribute('id', help="the ID of this shape")
            transform_id = base.SFFAttribute(
                'transform_id',
                help="the transform applied to this shape to position it in the space"
            )
            attribute = base.SFFAttribute(
                'attribute',
                help="extra attribute information e.g. 'FOM'"
            )

        class _Cone(_Shape):
            gds_type = emdb_sff.cone
            ref = "cone"

        with self.assertRaisesRegex(AttributeError, r".*superclass does not have an 'update_counter' classmethod"):
            _cone = _Cone()

    def test_errors(self):
        """Test that we get the right exceptions"""

        class _Segment(adapter.SFFSegment):
            index_attr = ''

        with self.assertRaisesRegex(base.SFFTypeError, r".*subclasses must provide an index attribute"):
            _Segment()

        class _Segment(adapter.SFFSegment):
            index_attr = 'segment_index'

        with self.assertRaisesRegex(AttributeError, r".*is missing a class variable.*"):
            _Segment()

        class _Segment(adapter.SFFSegment):
            segment_id = 3.8

        with self.assertRaises(base.SFFTypeError):
            _Segment()


class TestSFFListType(Py23FixTestCase):
    """Test the iteration mixin class `SFFListType`"""

    def test_create_from_gds_type(self):
        """Test create from a gds_type"""
        # empty list
        _S = emdb_sff.segment_listType()
        S = adapter.SFFSegmentList.from_gds_type(_S)
        self.assertEqual(len(S), 0)
        # populated list; no segment IDS
        _T = emdb_sff.segment_listType()
        _no_items = _random_integer(start=2, stop=10)
        [_T.add_segment(emdb_sff.segment_type()) for _ in _xrange(_no_items)]
        T = adapter.SFFSegmentList.from_gds_type(_T)
        self.assertEqual(len(T), _no_items)
        # populated list; with segment IDS
        _U = emdb_sff.segment_listType()
        [_U.add_segment(emdb_sff.segment_type(id=i)) for i in _xrange(1, _no_items + 1)]
        U = adapter.SFFSegmentList.from_gds_type(_U)
        self.assertEqual(len(U), _no_items)
        self.assertEqual(len(U._id_dict), _no_items)
        # error
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            adapter.SFFSegmentList.from_gds_type([])

    # def test_create_from_list(self):
    #     """Test that we can create a `SFFListType` object from a literal list of contained objects"""
    #     # segments
    #     _no_items = _random_integer(start=2, stop=10)
    #     _S = [adapter.SFFSegment() for _ in _xrange(_no_items)]
    #     S = adapter.SFFSegmentList.from_list(_S)
    #     self.assertEqual(len(S), _no_items)
    #     self.assertEqual(len(S._id_dict), _no_items)
    #     self.assertIsInstance(S.get_by_id(1), adapter.SFFSegment)

    def test_length(self):
        """Test that we can evaluate length"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=1, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        self.assertEqual(len(S), _no_segments)
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        _no_shapes = _random_integer(start=1, stop=10)
        [Sh.append(adapter.SFFCone()) for _ in _xrange(_no_shapes)]
        [Sh.append(adapter.SFFCuboid()) for _ in _xrange(_no_shapes)]
        [Sh.append(adapter.SFFCylinder()) for _ in _xrange(_no_shapes)]
        [Sh.append(adapter.SFFEllipsoid()) for _ in _xrange(_no_shapes)]
        self.assertEqual(len(Sh), _no_shapes * 4)

    def test_reset_id(self):
        """Test that we can reset IDs"""
        adapter.SFFSegmentList()
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        adapter.SFFSegmentList()
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)

    def test_iterate(self):
        """Test that we can iterate"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=2, stop=10)
        for _ in _xrange(_no_segments):
            S.append(adapter.SFFSegment())
        for i, s in enumerate(S, start=1):
            self.assertIsInstance(s, adapter.SFFSegment)
            self.assertEqual(s.id, i)
        # software list
        Sw = adapter.SFFSoftwareList()
        _no_sw = _random_integer(start=2, stop=10)
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw)]
        self.assertEqual(next(iter(Sw)), Sw[0])

    def test_sibling_classes(self):
        """Test that the `sibling_classes` attribute works"""
        Sh = adapter.SFFShapePrimitiveList()
        _no_items = _random_integer(start=2, stop=10)
        [Sh.append(adapter.SFFCone(height=_random_float(), bottomRadius=_random_float())) for _ in _xrange(_no_items)]
        [Sh.append(adapter.SFFCuboid(x=_random_float(), y=_random_float(), z=_random_float())) for _ in
         _xrange(_no_items)]
        [Sh.append(adapter.SFFCylinder(height=_random_float(), diameter=_random_float())) for _ in _xrange(_no_items)]
        [Sh.append(adapter.SFFEllipsoid(x=_random_float(), y=_random_float(), z=_random_float())) for _ in
         _xrange(_no_items)]
        for i in _xrange(_no_items):
            self.assertIsInstance(Sh[i], adapter.SFFCone)
        for i in _xrange(i + 1, _no_items * 2):
            self.assertIsInstance(Sh[i], adapter.SFFCuboid)
        for i in _xrange(i + 1, _no_items * 3):
            self.assertIsInstance(Sh[i], adapter.SFFCylinder)
        for i in _xrange(i + 1, _no_items * 4):
            self.assertIsInstance(Sh[i], adapter.SFFEllipsoid)

        # exceptions
        class _Shapes(adapter.SFFShapePrimitiveList):
            sibling_classes = [
                (emdb_sff.cone, adapter.SFFCone),
                (emdb_sff.ellipsoid, adapter.SFFEllipsoid)
            ]

        _S = _Shapes()
        _S.append(adapter.SFFCylinder())
        with self.assertRaises(base.SFFTypeError):
            _S[0]

    def test_getitem(self):
        """Test that we use index syntax to retrieve an object"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=3, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        self.assertIsInstance(S[_no_segments - 1], adapter.SFFSegment)
        # software list
        Sw = adapter.SFFSoftwareList()
        _no_sw = _random_integer(start=3, stop=10)
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw)]
        self.assertIsInstance(Sw[_no_sw - 1], adapter.SFFSoftware)
        # do we get an IndexError?
        with self.assertRaises(IndexError):
            _ = S[_no_segments]
        with self.assertRaises(IndexError):
            _ = Sw[_no_sw]

    def test_setitem(self):
        """Test that we can use index syntax to set an object"""
        # segment
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        S[0] = adapter.SFFSegment()
        self.assertEqual(len(S), 1)
        # software
        Sw = adapter.SFFSoftwareList()
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        Sw[0] = adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())
        self.assertEqual(len(Sw), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S[0] = rw.random_word()
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S[0] = adapter.SFFSoftwareList()
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            Sw[0] = adapter.SFFSegment()

    def test_delitem(self):
        """Test that we can use index syntax for setting an item to the list"""
        # segments
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        del S[0]
        self.assertEqual(len(S), 0)
        # software list
        Sw = adapter.SFFSoftwareList()
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        del Sw[0]
        self.assertEqual(len(Sw), 0)

    def test_append(self):
        """Test that we can append to the end of the list"""
        # segments
        S = adapter.SFFSegmentList()
        self.assertEqual(len(S), 0)
        S.append(adapter.SFFSegment())
        self.assertEqual(len(S), 1)
        # software
        Sw = adapter.SFFSoftwareList()
        self.assertEqual(len(Sw), 0)
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        self.assertEqual(len(Sw), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.append(rw.random_word())
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.append(adapter.SFFSoftwareList())
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            Sw.append(adapter.SFFSegment())

    def test_clear(self):
        """Test that we can clear the list"""
        Sw = adapter.SFFSoftwareList()
        _no_sw = _random_integer(start=2, stop=10)
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw)]
        self.assertEqual(len(Sw), _no_sw)
        Sw.clear()
        self.assertEqual(len(Sw), 0)

    def test_copy(self):
        """Test that we can create a shallow copy"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        R = S
        self.assertEqual(id(S), id(R))
        R = S.copy()
        self.assertIsInstance(R, type(S))
        self.assertNotEqual(id(S), id(R))
        # software list
        C = adapter.SFFSoftwareList()
        _no_complexes = _random_integer(start=2, stop=10)
        [C.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_complexes)]
        D = C
        self.assertEqual(id(C), id(D))
        D = C.copy()
        self.assertIsInstance(D, type(C))
        self.assertNotEqual(id(C), id(D))
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        _no_shapes = 3
        Sh.append(adapter.SFFCone())
        Sh.append(adapter.SFFCuboid())
        Sh.append(adapter.SFFCylinder())
        Sh.append(adapter.SFFEllipsoid())
        Rh = Sh
        self.assertEqual(id(Sh), id(Rh))
        Rh = Sh.copy()
        self.assertIsInstance(Rh, type(Sh))
        self.assertNotEqual(id(Sh), id(Rh))

    def test_extend(self):
        """Test that we can extend a `SFFListType` subclass with another"""
        # segments
        S1 = adapter.SFFSegmentList()
        _no_segments1 = _random_integer(start=2, stop=10)
        [S1.append(adapter.SFFSegment()) for _ in _xrange(_no_segments1)]
        S2 = adapter.SFFSegmentList()
        _no_segments2 = _random_integer(start=2, stop=10)
        [S2.append(adapter.SFFSegment()) for _ in _xrange(_no_segments2)]
        self.assertEqual(len(S1), _no_segments1)
        self.assertEqual(len(S2), _no_segments2)
        S1.extend(S2)
        self.assertEqual(len(S1), _no_segments1 + _no_segments2)
        # software list
        Sw1 = adapter.SFFSoftwareList()
        _no_sw1 = _random_integer(start=2, stop=10)
        [Sw1.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw1)]
        Sw2 = adapter.SFFSoftwareList()
        _no_sw2 = _random_integer(start=2, stop=10)
        [Sw2.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw2)]
        self.assertEqual(len(Sw1), _no_sw1)
        self.assertEqual(len(Sw2), _no_sw2)
        Sw1.extend(Sw2)
        self.assertEqual(len(Sw1), _no_sw1 + _no_sw2)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S1.extend(Sw1)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            Sw1.extend(S1)

    def test_insert(self):
        """Test that we can perform an insert"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        self.assertEqual(len(S), _no_segments)
        s = adapter.SFFSegment()
        S.insert(1, s)
        self.assertEqual(len(S), _no_segments + 1)
        self.assertEqual(S[1].id, s.id)
        # software list
        Sw = adapter.SFFSoftwareList()
        _no_sw = _random_integer(start=2, stop=10)
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_sw)]
        self.assertEqual(len(Sw), _no_sw)
        sw = adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())
        Sw.insert(1, sw)
        self.assertEqual(len(Sw), _no_sw + 1)
        self.assertEqual(Sw[1], sw)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.insert(1, sw)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            Sw.insert(1, s)

    def test_pop(self):
        """Test that we can pop items off"""
        # segments
        S = adapter.SFFSegmentList()
        s0 = adapter.SFFSegment()
        S.append(s0)
        s1 = S.pop()
        self.assertEqual(len(S), 0)
        self.assertIsInstance(s1, adapter.SFFSegment)
        self.assertEqual(s0.id, s1.id)  # ensure we are not creating a new one
        # pop with index
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        s = S.pop(index=1)
        self.assertEqual(len(S), 2)
        self.assertIsInstance(s, adapter.SFFSegment)
        # software list
        Sw = adapter.SFFSoftwareList()
        sw0 = adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())
        Sw.append(sw0)
        sw1 = Sw.pop()
        self.assertEqual(len(Sw), 0)
        self.assertIsInstance(sw1, adapter.SFFSoftware)
        self.assertEqual(sw0, sw1)
        # pop with index
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word()))
        sw = Sw.pop(index=1)
        self.assertEqual(len(Sw), 2)
        self.assertIsInstance(sw, adapter.SFFSoftware)
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        sh00 = adapter.SFFCone()
        Sh.append(sh00)
        sh01 = adapter.SFFEllipsoid()
        Sh.append(sh01)
        sh11 = Sh.pop()
        sh10 = Sh.pop()
        self.assertEqual(len(Sh), 0)
        self.assertIsInstance(sh11, adapter.SFFEllipsoid)
        self.assertIsInstance(sh10, adapter.SFFCone)
        self.assertEqual(sh00.id, sh10.id)
        self.assertEqual(sh01.id, sh11.id)
        # pop with index
        Sh.append(adapter.SFFCylinder())
        Sh.append(adapter.SFFCylinder())
        Sh.append(adapter.SFFCuboid())
        sh = Sh.pop(index=1)
        self.assertEqual(len(Sh), 2)
        self.assertIsInstance(sh, adapter.SFFCylinder)

    def test_remove(self):
        """Test remove from list"""
        # segments
        S = adapter.SFFSegmentList()
        s = adapter.SFFSegment(id=1)
        S.append(s)
        self.assertEqual(len(S), 1)
        S.remove(s)
        self.assertEqual(len(S), 0)
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        sh = adapter.SFFCuboid(id=1)
        Sh.append(sh)
        self.assertEqual(len(Sh), 1)
        Sh.remove(sh)
        self.assertEqual(len(Sh), 0)
        # exceptions
        _sw = rw.random_word()
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.remove(_sw)

    def test_reverse(self):
        """Test that we can reverse the list"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=1, stop=10)
        [S.append(adapter.SFFSegment(id=i)) for i in _xrange(_no_segments)]
        _ids = list(map(lambda s: s.id, S))
        S.reverse()
        _rids = list(map(lambda s: s.id, S))
        self.assertEqual(_ids[::-1], _rids)
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        _no_shapes = _random_integer(start=1, stop=10)
        [Sh.append(adapter.SFFCone(id=i)) for i in _xrange(_no_shapes)]
        _ids = list(map(lambda sh: sh.id, Sh))
        Sh.reverse()
        _rids = list(map(lambda sh: sh.id, Sh))
        self.assertEqual(_ids[::-1], _rids)

    def test_errors(self):
        """Test that the right exceptions are raised"""

        class _Segments(adapter.SFFSegmentList):
            iter_attr = ()

        with self.assertRaises(ValueError):
            _Segments()

        class _Segments(adapter.SFFSegmentList):
            iter_attr = (1, adapter.SFFSegment)

        with self.assertRaises(base.SFFTypeError):
            _Segments()

        class _Segments(adapter.SFFSegmentList):
            iter_attr = ('segment', float)

        with self.assertRaises(base.SFFTypeError):
            _Segments()

    def test_get_ids(self):
        """Test that we can get IDs of contained objects"""
        # segments
        S = adapter.SFFSegmentList()
        _no_items = _random_integer(start=1, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_items)]
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # appending item from gds does not change length of ID list
        S.append(adapter.SFFSegment.from_gds_type(emdb_sff.segment_type()))
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # software list
        Sw = adapter.SFFSoftwareList()
        [Sw.append(adapter.SFFSoftware(name=rw.random_word(), version=rw.random_word())) for _ in _xrange(_no_items)]
        self.assertEqual(list(Sw.get_ids()), list(_xrange(_no_items)))
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        [Sh.append(adapter.SFFCone()) for _ in _xrange(_no_items)]
        [Sh.append(adapter.SFFCuboid()) for _ in _xrange(_no_items)]
        [Sh.append(adapter.SFFCylinder()) for _ in _xrange(_no_items)]
        [Sh.append(adapter.SFFEllipsoid()) for _ in _xrange(_no_items)]
        self.assertEqual(list(Sh.get_ids()), list(_xrange(_no_items * 4)))

    def test_get_by_id(self):
        """Test that we can get an item by ID"""
        # segments
        S = adapter.SFFSegmentList()
        s0 = adapter.SFFSegment(biologicalAnnotation=adapter.SFFBiologicalAnnotation())
        S.append(s0)
        s1 = S.get_by_id(1)
        self.assertEqual(s0.id, s1.id)
        # appending/setting/inserting a new item immediately makes it available on the dict
        s0 = adapter.SFFSegment(id=1000)
        S.append(s0)
        s1 = S.get_by_id(1000)
        self.assertEqual(s0.id, s1.id)
        with self.assertRaises(KeyError):
            S.get_by_id(1001)
        # popping/removing removes from the dict
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        s_id = S[-1].id
        s = S.pop()
        self.assertEqual(s.id, s_id)
        with self.assertRaises(KeyError):
            S.get_by_id(s_id)
        # clearing clears the dict
        S = adapter.SFFSegmentList()
        _no_items = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_items)]
        self.assertTrue(len(S) > 1)
        S.clear()
        with self.assertRaises(KeyError):
            S.get_by_id(1)
        # extending extends the dict
        S1 = adapter.SFFSegmentList()
        [S1.append(adapter.SFFSegment()) for _ in _xrange(_no_items)]
        S2 = adapter.SFFSegmentList()
        [S2.append(adapter.SFFSegment()) for _ in _xrange(_no_items * 2)]
        S2.extend(S1)
        s_id = random.choice(list(S2.get_ids()))
        self.assertIsInstance(S2.get_by_id(s_id), adapter.SFFSegment)
        self.assertEqual(len(S2), _no_items * 3)
        # reversing has no impact
        S = S2.copy()
        S.reverse()
        s_id = random.choice(list(S.get_ids()))
        self.assertEqual(S.get_by_id(s_id).id, S2.get_by_id(s_id).id)
        # exceptions
        # ID collisions
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        with self.assertRaisesRegex(KeyError, r"item with ID.*already present"):
            S.append(adapter.SFFSegment(id=1))
        # nothing with key 'None'

    def test_get_from_segmentation(self):
        """Test that we can get by ID from the top level

        - segmentation.
        """
        # create a segmentation
        S = adapter.SFFSegmentation(name='my segmentation')
        # set the segments attribute
        S.segments = adapter.SFFSegmentList()
        s = adapter.SFFSegment()
        # add a segment
        S.segments.append(s)
        s_get = S.segments.get_by_id(1)
        self.assertEqual(s.id, 1)
        self.assertEqual(s_get.id, 1)
        self.assertEqual(len(S.segments), 1)
        s_index = S.segments[0]
        self.assertEqual(s_index.id, 1)
        self.assertEqual(s_get.id, 1)
        self.assertEqual(len(S.segments), 1)

    def test_validation(self):
        """Test that the list-type passes validation

        Validation is based on the `min_length` attribute which is `0` by default

        If a list-type has `min_length>0` and the list is fewer than the minimum items then it
        should fail validation.

        An example of this is `SFFVertexList` which should have at least 3 vertices (for a triangle)
        """

        class T(base.SFFListType):
            gds_type = emdb_sff.transform_listType
            min_length = 1
            iter_attr = (u'transformation_matrix', adapter.SFFTransformationMatrix)
            repr_string = u"Transform({})"
            repr_args = (u'list()',)

        t = T()
        self.assertFalse(t._is_valid())
        [t.append(
            adapter.SFFTransformationMatrix(data=numpy.random.rand(5, 5))
        ) for _ in _xrange(_random_integer(start=3, stop=10))]
        _print(t)
        self.assertTrue(t._is_valid())


class TestSFFAttribute(Py23FixTestCase):
    """Test the attribute descriptor class"""

    def test_default(self):
        """Test default settings"""

        class _Colour(adapter.SFFType):
            gds_type = emdb_sff.rgba_type
            r = base.SFFAttribute('red', help='red colour')
            g = base.SFFAttribute('green', help='green colour')
            b = base.SFFAttribute('blue', help='blue colour')
            a = base.SFFAttribute('alpha', help='alpha colour')

        _r, _g, _b, _a = _random_floats(count=4)
        _c = _Colour(red=_r, green=_g, blue=_b, alpha=_a)
        self.assertEqual(_c.r, _r)
        self.assertEqual(_c.g, _g)
        self.assertEqual(_c.b, _b)
        self.assertEqual(_c.a, _a)
        # delete alpha
        del _c.a
        self.assertIsNone(_c.a)

    def test_list_attribute(self):
        """Test that an empty list attribute does not return 'None'"""

        class _BA(adapter.SFFType):
            gds_type = emdb_sff.biological_annotationType
            repr_string = """_BA(external_references={})"""
            repr_args = ('extref',)
            extref = base.SFFAttribute(
                'external_references',
                sff_type=adapter.SFFExternalReferenceList,
                help='the list of external reference objects'
            )

        ba = _BA()
        self.stderr(ba)
        self.assertIsInstance(ba.extref, adapter.SFFExternalReferenceList)
        self.assertEqual(len(ba.extref), 0)

    def test_error(self):
        """Test that we get an exception on setting wrong type"""

        class _Segmentation(adapter.SFFType):
            gds_type = emdb_sff.segmentation
            s = base.SFFAttribute('software', sff_type=adapter.SFFSoftware)

        _S = _Segmentation()
        with self.assertRaises(base.SFFTypeError):
            _S.s = adapter.SFFSegment()

    def test_default_value(self):
        """Test setting a default value to the attribute"""

        class _BA(adapter.SFFType):
            gds_type = emdb_sff.biological_annotationType
            no = base.SFFAttribute('number_of_instances', default=1)

        # explicit
        _b = _BA(number_of_instances=33)
        self.assertEqual(_b.no, 33)
        # default
        _b = _BA()
        # _print('_b.no', _b.no)
        self.assertEqual(_b.no, 1)

    def test_required_value(self):
        """Test setting a required attribute"""

        class _ER(adapter.SFFType):
            gds_type = emdb_sff.external_reference_type
            t = base.SFFAttribute('type', required=True)

        _e = _ER()
        self.assertFalse(_e._is_valid())
        _e.t = rw.random_word()
        self.assertTrue(_e._is_valid())
