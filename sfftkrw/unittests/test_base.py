# -*- coding: utf-8 -*-
# test_adapter.py
"""
Unit for schema adapter
"""
from __future__ import print_function

import os
import tempfile

from random_words import RandomWords, LoremIpsum

from . import _random_integer, Py23FixTestCase, _random_float
from ..core import _xrange, _str
from ..schema import adapter, base, emdb_sff

rw = RandomWords()
li = LoremIpsum()


class TestSFFTypeError(Py23FixTestCase):
    """Tests for the exception"""

    def test_default(self):
        """Test default operation"""
        c = adapter.SFFComplexes()
        with self.assertRaisesRegex(base.SFFTypeError, r".*?list.*?"):
            c.set_complexes('complexes')

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
        self.assertEqual(S.version, _S.schemaVersion)

    def test_gds_type_missing(self):
        """Test for presence of `gds_type` attribute"""

        class _SomeEntity(base.SFFType):
            """Empty entity"""

        with self.assertRaisesRegex(ValueError, r'.*gds_type.*'):
            _s = _SomeEntity()

    def test_create_from_gds_type(self):
        """Test creating an `SFFType` subclass object from a `gds_type' object"""
        # we will try with SFFRGBA and rgbaType
        red = _random_float()
        green = _random_float()
        blue = _random_float()
        _r = emdb_sff.rgbaType(
            red=red, green=green, blue=blue,
        )
        r = adapter.SFFRGBA.from_gds_type(_r)
        self.assertIsInstance(r, adapter.SFFRGBA)
        self.assertEqual(r.red, red)
        self.assertEqual(r.green, green)
        self.assertEqual(r.blue, blue)

    def test_create_from_gds_type_raises_error(self):
        """Test that we get an exception when the `SFFType` subclass object's `gds_type` attribute is not the same
        as the one provided"""
        _r = emdb_sff.biologicalAnnotationType()
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            r = adapter.SFFRGBA.from_gds_type(_r)

    def test_ref_attr(self):
        """Test the `ref` attribute"""
        c = adapter.SFFRGBA(
            red=1, green=1, blue=0, alpha=0.5
        )
        r = repr(c)
        self.assertRegex(r, r"\(.*\d+,.*\)")

    def test_repr_string_repr_args(self):
        """Test the string representation using `repr_string` and `repr_args`"""
        # correct rendering for colour: prints out repr_string filled with repr_args
        c = adapter.SFFRGBA(random_colour=True)
        self.assertRegex(str(c), r"SFFRGBA\(red=\d\.\d+.*\)")
        # correct assessment of length: prints out a string with the correct len() value
        c = adapter.SFFComplexes()
        c.set_complexes(rw.random_words(count=10))
        self.assertRegex(str(c), ".*10.*")
        # plain string: prints the plain string
        v = adapter.SFFThreeDVolume()
        self.assertEqual(str(v), "3D formatted segment")

        # repr_str is missing: prints out the output of type
        class _RGBA(adapter.SFFRGBA):
            repr_string = ""

        _c = _RGBA(random_colour=True)
        self.assertRegex(str(_c), r".class.*_RGBA.*")

        # unmatched repr_args (it should be a tuple of four values)
        class _RGBA(adapter.SFFRGBA):
            repr_args = ('red', 'green')

        _c = _RGBA(random_colour=True)
        with self.assertRaisesRegex(ValueError, r'Unmatched number.*'):
            str(_c)

    def test_export_xml(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = 'test segmentation'
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.sff'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S.version, _S.version)
        self.assertEqual(S.name, _S.name)
        self.assertEqual(S.details, _S.details)

    def test_export_hdf5(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = 'test segmentation'
        S.primary_descriptor = 'meshList'
        S.software = adapter.SFFSoftware()
        S.transforms = adapter.SFFTransformList()
        S.bounding_box = adapter.SFFBoundingBox()
        S.global_external_references = adapter.SFFGlobalExternalReferences()
        S.segments = adapter.SFFSegmentList()
        S.lattices = adapter.SFFLatticeList()
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.hff'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S.version, _S.version)
        self.assertEqual(S.name, _S.name)
        self.assertEqual(S.details, _S.details)

    def test_export_json(self):
        """Test that we can export a segmentation as XML"""
        S = adapter.SFFSegmentation()
        S.name = 'test segmentation'
        S.primary_descriptor = 'meshList'
        S.software = adapter.SFFSoftware()
        S.transforms = adapter.SFFTransformList()
        S.bounding_box = adapter.SFFBoundingBox()
        S.global_external_references = adapter.SFFGlobalExternalReferences()
        S.segments = adapter.SFFSegmentList()
        S.lattices = adapter.SFFLatticeList()
        S.details = li.get_sentences(sentences=10)
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.json'
        S.export(tf.name)
        _S = adapter.SFFSegmentation.from_file(tf.name)
        self.assertEqual(S.version, _S.version)
        self.assertEqual(S.name, _S.name)
        self.assertEqual(S.details, _S.details)

    def test_export_errors(self):
        """Test that we catch all export errors"""
        tf = tempfile.NamedTemporaryFile()
        tf.name += '.invalid'
        self.assertEqual(os.EX_DATAERR, adapter.SFFSegmentation().export(tf.name))

    def test_format_method_missing(self):
        """Test that we get `NotImplementedError`s"""

        class _SomeEntity(base.SFFType):
            """Empty entity"""
            gds_type = emdb_sff.segmentation

        _S = _SomeEntity()
        with self.assertRaises(NotImplementedError):
            _S.as_hff('test')

        with self.assertRaises(NotImplementedError):
            _S.as_json('test')


class TestSFFIndexType(Py23FixTestCase):
    """Test the indexing mixin class `SFFIndexType"""

    def setUp(self):
        """Reset ids"""
        adapter.SFFSegment.segment_id = 1  # reset ID informarly
        adapter.SFFShape.shape_id = 0
        adapter.SFFVertex.vertex_id = 0
        adapter.SFFPolygon.polygon_id = 0

    def test_explicit_set_id(self):
        """Test that we can explicitly set ID apart from incrementing"""
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        s = adapter.SFFSegment(id=999)
        self.assertEqual(s.id, 999)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1000)

    def test_vertex_ids(self):
        """Test that vID works as expected"""
        v = adapter.SFFVertex()
        self.assertEqual(v.vID, 0)
        v = adapter.SFFVertex(vID=999)
        self.assertEqual(v.vID, 999)
        v = adapter.SFFVertex()
        self.assertEqual(v.vID, 1000)

    def test_polygon_ids(self):
        """Test that PID works as expected"""
        p = adapter.SFFPolygon()
        self.assertEqual(p.PID, 0)
        p = adapter.SFFPolygon(PID=999)
        self.assertEqual(p.PID, 999)
        p = adapter.SFFPolygon()
        self.assertEqual(p.PID, 1000)

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
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segmentType(id=35))
        self.assertEqual(s.id, 35)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segmentType())
        self.assertIsNone(s.id)
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 6)

    def test_with_gds_type(self):
        """Test that we can work with generateDS types"""
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segmentType())
        self.assertIsNone(s.id)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segmentType(id=37))
        self.assertIsNotNone(s.id)

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
                'transformId',
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

    def test_length(self):
        """Test that we can evaluate length"""
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=1)
        for _ in _xrange(_no_segments):
            S.add_segment(adapter.SFFSegment())
        self.assertEqual(len(S), _no_segments)

    def test_reset_id(self):
        """Test that we can reset IDs"""
        S = adapter.SFFSegmentList()
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)
        S = adapter.SFFSegmentList()
        s = adapter.SFFSegment()
        self.assertEqual(s.id, 1)

    def test_iterate(self):
        """Test that we can iterate"""
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=2)
        for _ in _xrange(_no_segments):
            S.add_segment(adapter.SFFSegment())
        for i, s in enumerate(S, start=1):
            self.assertIsInstance(s, adapter.SFFSegment)
            self.assertEqual(s.id, i)
        # complexes
        c = adapter.SFFComplexes()
        words = rw.random_words(count=3)
        c.set_complexes(words)
        self.assertEqual(next(iter(c)), words[0])

    def test_getitem(self):
        """Test that we use index syntax to retrieve an object"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=3)
        [S.add_segment(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        self.assertIsInstance(S[_no_segments - 1], adapter.SFFSegment)
        # complexes
        C = adapter.SFFComplexes()
        _no_complexes = _random_integer(start=3)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertIsInstance(C[_no_complexes - 1], _str)
        # do we get an IndexError?
        with self.assertRaises(IndexError):
            _ = S[_no_segments]
        with self.assertRaises(IndexError):
            _ = C[_no_complexes]

    def test_setitem(self):
        """Test that we can use index syntax to set an object"""
        # segment
        S = adapter.SFFSegmentList()
        S.add_segment(adapter.SFFSegment())
        S[0] = adapter.SFFSegment()
        self.assertEqual(len(S), 1)
        # complex
        C = adapter.SFFComplexes()
        C.add_complex(rw.random_word())
        C[0] = rw.random_word()
        self.assertEqual(len(C), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S[0] = rw.random_word()
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S[0] = adapter.SFFComplexes()
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            C[0] = adapter.SFFSegment()

    def test_delitem(self):
        """Test that we can use index syntax for setting an item to the list"""
        S = adapter.SFFSegmentList()
        S.add_segment(adapter.SFFSegment())
        del S[0]
        self.assertEqual(len(S), 0)

    def test_append(self):
        """Test that we can append to the end of the list"""
        # segments
        S = adapter.SFFSegmentList()
        self.assertEqual(len(S), 0)
        S.append(adapter.SFFSegment())
        self.assertEqual(len(S), 1)
        # complexes
        C = adapter.SFFComplexes()
        self.assertEqual(len(C), 0)
        C.append(rw.random_word())
        self.assertEqual(len(C), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S.append(rw.random_word())
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S.append(adapter.SFFComplexes())
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            C.append(adapter.SFFSegment())

    def test_clear(self):
        """Test that we can clear the list"""
        C = adapter.SFFComplexes()
        _no_complexes = _random_integer(start=2)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertEqual(len(C), _no_complexes)
        C.clear()
        self.assertEqual(len(C), 0)

    def test_copy(self):
        """"""

    def test_extend(self):
        """Test that we can extend a `SFFListType` subclass with another"""
        # segments
        S1 = adapter.SFFSegmentList()
        _no_segments1 = _random_integer(start=2)
        [S1.append(adapter.SFFSegment()) for _ in _xrange(_no_segments1)]
        S2 = adapter.SFFSegmentList()
        _no_segments2 = _random_integer(start=2)
        [S2.append(adapter.SFFSegment()) for _ in _xrange(_no_segments2)]
        self.assertEqual(len(S1), _no_segments1)
        self.assertEqual(len(S2), _no_segments2)
        S1.extend(S2)
        self.assertEqual(len(S1), _no_segments1 + _no_segments2)
        # complexes
        C1 = adapter.SFFComplexes()
        _no_complexes1 = _random_integer(start=2)
        [C1.append(rw.random_word()) for _ in _xrange(_no_complexes1)]
        C2 = adapter.SFFComplexes()
        _no_complexes2 = _random_integer(start=2)
        [C2.append(rw.random_word()) for _ in _xrange(_no_complexes2)]
        self.assertEqual(len(C1), _no_complexes1)
        self.assertEqual(len(C2), _no_complexes2)
        C1.extend(C2)
        self.assertEqual(len(C1), _no_complexes1 + _no_complexes2)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S1.extend(C1)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            C1.extend(S1)

    def test_insert(self):
        """Test that we can perform an insert"""
        # segments
        S = adapter.SFFSegmentList()
        _no_segments = _random_integer(start=2)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_segments)]
        self.assertEqual(len(S), _no_segments)
        s = adapter.SFFSegment()
        S.insert(1, s)
        self.assertEqual(len(S), _no_segments + 1)
        self.assertEqual(S[1].id, s.id)
        # complexes
        C = adapter.SFFComplexes()
        _no_complexes = _random_integer(start=2)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertEqual(len(C), _no_complexes)
        c = rw.random_word()
        C.insert(1, c)
        self.assertEqual(len(C), _no_complexes + 1)
        self.assertEqual(C[1], c)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.insert(1, c)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            C.insert(1, s)

    def test_pop(self):
        """Test that we can pop items off"""
        S = adapter.SFFSegmentList()
        s0 = adapter.SFFSegment()
        S.append(s0)
        s1 = S.pop()
        self.assertEqual(len(S), 0)
        self.assertIsInstance(s1, adapter.SFFSegment)
        self.assertEqual(s0.id, s1.id) # ensure we are not creating a new one
        # pop with index
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        s = S.pop(index=1)
        self.assertEqual(len(S), 2)
        self.assertIsInstance(s, adapter.SFFSegment)

    def test_remove(self):
        """"""

    def test_reverse(self):
        """"""

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
        # S = adapter.SFFSegmentList()
        # _no_segments = _random_integer(start=1)
        # for _ in _xrange(_no_segments):
        #     S.add_segment(adapter.SFFSegment())
        # self.assertEqual(S.get_ids(), list(_xrange(1, _no_segments + 1)))



class TestSFFDictType(Py23FixTestCase):
    """Test the direct-access mixin class `SFFDictType`"""

    # applies to List

    def test_get_ids(self):
        """Test that get_ids() returns a list of IDs"""
        self.assertTrue(False)

    def test_get_by_id(self):
        """Test that we can get by ID"""
        self.assertTrue(False)

    # def test_iter_dict(self):
    #     """Test the convenience dict for quick access to items by ID"""
    #     S = adapter.SFFSegmentList()
    #     ids = _random_integers(count=10)
    #     segment_dict = _dict()
    #     for i in ids:
    #         s = adapter.SFFSegment(id=i)
    #         S.add_segment(s)
    #         segment_dict[i] = s
    # print('segment_dict:', id(list(_dict_iter_values(segment_dict))[0]), file=sys.stderr)
    # print('S.iter_dict:', id(list(_dict_iter_values(S.iter_dict))[0]), file=sys.stderr)
    #
    # print(dir(s), file=sys.stderr)
    # for attr in dir(s):
    #     print(attr, getattr(s, attr), type(getattr(s, attr)), file=sys.stderr)
    #     if isinstance(attr, adapter.SFFAttribute):
    #         print(getattr(s, attr), file=sys.stderr)
    # self.assertDictEqual(segment_dict, S.iter_dict)

    # add complex
    # word = rw.random_word()
    # c.add_complex(word)
    # p[word] = word
    # self.assertDictEqual(p, c.iter_dict)


class TestSFFAttribute(Py23FixTestCase):
    """Test the attribute descriptor class"""

    def test_default(self):
        """Test default settings"""
        self.assertTrue(False)
