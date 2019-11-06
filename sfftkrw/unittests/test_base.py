# -*- coding: utf-8 -*-
# test_adapter.py
"""
Unit for schema adapter
"""
from __future__ import print_function

import os
import random
import sys
import tempfile

import numpy
from random_words import RandomWords, LoremIpsum

from . import _random_integer, Py23FixTestCase, _random_float, _random_floats
from ..core import _xrange, _str
from ..schema import adapter, base, emdb_sff

rw = RandomWords()
li = LoremIpsum()


class TestSFFTypeError(Py23FixTestCase):
    """Tests for the exception"""

    def test_default(self):
        """Test default operation"""
        c = adapter.SFFComplexesAndMacromolecules()
        with self.assertRaisesRegex(base.SFFTypeError, r".*?is not object of type.*?"):
            c.complexes = 'complexes'

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
        # from None returns None
        r = adapter.SFFRGBA.from_gds_type()
        self.assertIsNone(r)

    def test_create_from_gds_type_raises_error(self):
        """Test that we get an exception when the `SFFType` subclass object's `gds_type` attribute is not the same
        as the one provided"""
        _r = emdb_sff.biologicalAnnotationType()
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
        c = adapter.SFFComplexList()
        c.id = rw.random_words(count=10)
        self.assertRegex(_str(c), r"SFFComplexList\(\[.*\]\)")
        # plain string: prints the plain string
        v = adapter.SFFThreeDVolume()
        self.assertRegex(_str(v), r"""SFFThreeDVolume\(latticeId=None, value=None, transformId=None\)""")
        # len() works
        class _Complexes(adapter.SFFComplexList):
            repr_string = u'complex list of length {}'
            repr_args = (u'len()',)
        C = _Complexes()
        no_cpx = _random_integer(start=2, stop=10)
        [C.append(rw.random_word()) for _ in _xrange(no_cpx)]
        self.assertRegex(_str(C), r".*{}.*".format(no_cpx))
        # using index syntax
        class _Lattice(adapter.SFFLattice):
            repr_string = u"{}"
            repr_args = (u"data[:20]", )
        L = _Lattice.from_array(numpy.random.randint(0, 10, size=(5, 5, 5)), size=adapter.SFFVolumeStructure(rows=5, cols=5, sections=5))
        self.assertRegex(_str(L), r"\".*\.\.\.\"")
        # no repr_args
        class _Complexes(adapter.SFFComplexList):
            repr_string = u"complexes"
            repr_args = ()
        C = _Complexes()
        self.assertEqual(_str(C), u"complexes")
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
        S.global_external_references = adapter.SFFGlobalExternalReferenceList()
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
        S.global_external_references = adapter.SFFGlobalExternalReferenceList()
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

    def test_export_stderr(self):
        """Test that we can export to stderr"""
        S = adapter.SFFSegmentation()
        # we check that everything was OK
        self.assertEqual(S.export(sys.stderr), os.EX_OK)

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

        with self.assertRaises(NotImplementedError):
            _S.from_hff('test')

        with self.assertRaises(NotImplementedError):
            _S.from_json('test')

        with self.assertRaises(NotImplementedError):
            _S == _S


class TestSFFIndexType(Py23FixTestCase):
    """Test the indexing mixin class `SFFIndexType"""

    def setUp(self):
        """Reset ids"""
        adapter.SFFSegment.segment_id = 1  # reset ID informarly
        adapter.SFFShape.shape_id = 0
        adapter.SFFVertex.vertex_id = 0
        adapter.SFFPolygon.polygon_id = 0

    def test_create_from_gds_type(self):
        """Test creating an `SFFIndexType` subclass object from a gds type"""
        # segment
        _s = emdb_sff.segmentType()
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        _t = emdb_sff.segmentType(id=10)
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

    def test_vertex_ids(self):
        """Test that vID works as expected"""
        v = adapter.SFFVertex()
        self.assertEqual(v.id, 0)
        v = adapter.SFFVertex(vID=999)
        self.assertEqual(v.id, 999)
        v = adapter.SFFVertex()
        self.assertEqual(v.id, 1000)

    def test_polygon_ids(self):
        """Test that PID works as expected"""
        p = adapter.SFFPolygon()
        self.assertEqual(p.id, 0)
        p = adapter.SFFPolygon(PID=999)
        self.assertEqual(p.id, 999)
        p = adapter.SFFPolygon()
        self.assertEqual(p.id, 1000)

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
        self.assertEqual(adapter.SFFSegment.segment_id, 1)
        s = adapter.SFFSegment.from_gds_type(emdb_sff.segmentType(id=38))
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

    def test_create_from_gds_type(self):
        """Test create from a gds_type"""
        # empty list
        _S = emdb_sff.segmentListType()
        S = adapter.SFFSegmentList.from_gds_type(_S)
        self.assertEqual(len(S), 0)
        # populated list; no segment IDS
        _T = emdb_sff.segmentListType()
        _no_items = _random_integer(start=2, stop=10)
        [_T.add_segment(emdb_sff.segmentType()) for _ in _xrange(_no_items)]
        T = adapter.SFFSegmentList.from_gds_type(_T)
        self.assertEqual(len(T), _no_items)
        # populated list; with segment IDS
        _U = emdb_sff.segmentListType()
        [_U.add_segment(emdb_sff.segmentType(id=i)) for i in _xrange(1, _no_items + 1)]
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
        # complexes
        c = adapter.SFFComplexList()
        words = rw.random_words(count=3)
        c.ids = words
        self.assertEqual(next(iter(c)), words[0])
        # vertices
        V = adapter.SFFVertexList()
        _no_vertices = _random_integer(start=2, stop=10)
        [V.append(adapter.SFFVertex()) for _ in _xrange(_no_vertices)]
        for i, v in enumerate(V):
            self.assertIsInstance(v, adapter.SFFVertex)
            self.assertEqual(v.id, i)
        # polygons
        P = adapter.SFFPolygonList()
        _no_polygons = _random_integer(start=2, stop=10)
        [P.append(adapter.SFFPolygon()) for _ in _xrange(_no_polygons)]
        for i, P in enumerate(P):
            self.assertIsInstance(P, adapter.SFFPolygon)
            self.assertEqual(P.id, i)

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
        # complexes
        C = adapter.SFFComplexList()
        _no_complexes = _random_integer(start=3, stop=10)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertIsInstance(C[_no_complexes - 1], _str)
        # vertices
        V = adapter.SFFVertexList()
        _no_vertexs = _random_integer(start=3, stop=10)
        [V.append(adapter.SFFVertex()) for _ in _xrange(_no_vertexs)]
        self.assertIsInstance(V[_no_vertexs - 1], adapter.SFFVertex)
        # polygons
        P = adapter.SFFPolygonList()
        _no_polygons = _random_integer(start=3, stop=10)
        [P.append(adapter.SFFPolygon()) for _ in _xrange(_no_polygons)]
        self.assertIsInstance(P[_no_polygons - 1], adapter.SFFPolygon)
        # do we get an IndexError?
        with self.assertRaises(IndexError):
            _ = S[_no_segments]
        with self.assertRaises(IndexError):
            _ = C[_no_complexes]

    def test_setitem(self):
        """Test that we can use index syntax to set an object"""
        # segment
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        S[0] = adapter.SFFSegment()
        self.assertEqual(len(S), 1)
        # complex
        C = adapter.SFFComplexList()
        C.append(rw.random_word())
        C[0] = rw.random_word()
        self.assertEqual(len(C), 1)
        # vertices
        V = adapter.SFFVertexList()
        V.append(adapter.SFFVertex())
        V[0] = adapter.SFFVertex()
        self.assertEqual(len(V), 1)
        # polygons
        P = adapter.SFFPolygonList()
        P.append(adapter.SFFPolygon())
        P[0] = adapter.SFFPolygon()
        self.assertEqual(len(P), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S[0] = rw.random_word()
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S[0] = adapter.SFFComplexList()
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            C[0] = adapter.SFFSegment()

    def test_delitem(self):
        """Test that we can use index syntax for setting an item to the list"""
        # segments
        S = adapter.SFFSegmentList()
        S.append(adapter.SFFSegment())
        del S[0]
        self.assertEqual(len(S), 0)
        # complexes
        C = adapter.SFFComplexList()
        C.append(rw.random_word())
        del C[0]
        self.assertEqual(len(C), 0)
        # vertices
        V = adapter.SFFVertexList()
        V.append(adapter.SFFVertex())
        del V[0]
        self.assertEqual(len(V), 0)
        # polygons
        P = adapter.SFFPolygonList()
        P.append(adapter.SFFPolygon())
        del P[0]
        self.assertEqual(len(P), 0)

    def test_append(self):
        """Test that we can append to the end of the list"""
        # segments
        S = adapter.SFFSegmentList()
        self.assertEqual(len(S), 0)
        S.append(adapter.SFFSegment())
        self.assertEqual(len(S), 1)
        # complexes
        C = adapter.SFFComplexList()
        self.assertEqual(len(C), 0)
        C.append(rw.random_word())
        self.assertEqual(len(C), 1)
        # vertices
        V = adapter.SFFVertexList()
        self.assertEqual(len(V), 0)
        V.append(adapter.SFFVertex())
        self.assertEqual(len(V), 1)
        # segments
        P = adapter.SFFPolygonList()
        self.assertEqual(len(P), 0)
        P.append(adapter.SFFPolygon())
        self.assertEqual(len(P), 1)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S.append(rw.random_word())
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S.append(adapter.SFFComplexList())
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            C.append(adapter.SFFSegment())

    def test_clear(self):
        """Test that we can clear the list"""
        C = adapter.SFFComplexList()
        _no_complexes = _random_integer(start=2, stop=10)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertEqual(len(C), _no_complexes)
        C.clear()
        self.assertEqual(len(C), 0)

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
        # complexes
        C = adapter.SFFComplexList()
        _no_complexes = _random_integer(start=2, stop=10)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
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
        # complexes
        C1 = adapter.SFFComplexList()
        _no_complexes1 = _random_integer(start=2, stop=10)
        [C1.append(rw.random_word()) for _ in _xrange(_no_complexes1)]
        C2 = adapter.SFFComplexList()
        _no_complexes2 = _random_integer(start=2, stop=10)
        [C2.append(rw.random_word()) for _ in _xrange(_no_complexes2)]
        self.assertEqual(len(C1), _no_complexes1)
        self.assertEqual(len(C2), _no_complexes2)
        C1.extend(C2)
        self.assertEqual(len(C1), _no_complexes1 + _no_complexes2)
        # vertices
        V1 = adapter.SFFVertexList()
        _no_vertices1 = _random_integer(start=2, stop=10)
        [V1.append(adapter.SFFVertex()) for _ in _xrange(_no_vertices1)]
        V2 = adapter.SFFVertexList()
        _no_vertices2 = _random_integer(start=2, stop=10)
        [V2.append(adapter.SFFVertex()) for _ in _xrange(_no_vertices2)]
        self.assertEqual(len(V1), _no_vertices1)
        self.assertEqual(len(V2), _no_vertices2)
        V1.extend(V2)
        self.assertEqual(len(V1), _no_vertices1 + _no_vertices2)
        # polygons
        P1 = adapter.SFFPolygonList()
        _no_polygons1 = _random_integer(start=2, stop=10)
        [P1.append(adapter.SFFPolygon()) for _ in _xrange(_no_polygons1)]
        P2 = adapter.SFFPolygonList()
        _no_polygons2 = _random_integer(start=2, stop=10)
        [P2.append(adapter.SFFPolygon()) for _ in _xrange(_no_polygons2)]
        self.assertEqual(len(P1), _no_polygons1)
        self.assertEqual(len(P2), _no_polygons2)
        P1.extend(P2)
        self.assertEqual(len(P1), _no_polygons1 + _no_polygons2)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S1.extend(C1)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            C1.extend(S1)

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
        # complexes
        C = adapter.SFFComplexList()
        _no_complexes = _random_integer(start=2, stop=10)
        [C.append(rw.random_word()) for _ in _xrange(_no_complexes)]
        self.assertEqual(len(C), _no_complexes)
        c = rw.random_word()
        C.insert(1, c)
        self.assertEqual(len(C), _no_complexes + 1)
        self.assertEqual(C[1], c)
        # vertices
        V = adapter.SFFVertexList()
        _no_vertices = _random_integer(start=2, stop=10)
        [V.append(adapter.SFFVertex()) for _ in _xrange(_no_vertices)]
        self.assertEqual(len(V), _no_vertices)
        v = adapter.SFFVertex()
        V.insert(1, v)
        self.assertEqual(len(V), _no_vertices + 1)
        self.assertEqual(V[1].id, v.id)
        # segments
        P = adapter.SFFPolygonList()
        _no_polygons = _random_integer(start=2, stop=10)
        [P.append(adapter.SFFPolygon()) for _ in _xrange(_no_polygons)]
        self.assertEqual(len(P), _no_polygons)
        p = adapter.SFFPolygon()
        P.insert(1, p)
        self.assertEqual(len(P), _no_polygons + 1)
        self.assertEqual(P[1].id, p.id)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            S.insert(1, c)
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            C.insert(1, s)

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
        # complexes
        C = adapter.SFFComplexList()
        c0 = rw.random_word()
        C.append(c0)
        c1 = C.pop()
        self.assertEqual(len(C), 0)
        self.assertIsInstance(c1, _str)
        self.assertEqual(c0, c1)
        # pop with index
        C.append(rw.random_word())
        C.append(rw.random_word())
        C.append(rw.random_word())
        c = C.pop(index=1)
        self.assertEqual(len(C), 2)
        self.assertIsInstance(c, _str)
        # vertices
        V = adapter.SFFVertexList()
        v0 = adapter.SFFVertex()
        V.append(v0)
        v1 = V.pop()
        self.assertEqual(len(V), 0)
        self.assertIsInstance(v1, adapter.SFFVertex)
        self.assertEqual(v0.id, v1.id)  # ensure we are not creating a new one
        # pop with index
        V.append(adapter.SFFVertex())
        V.append(adapter.SFFVertex())
        V.append(adapter.SFFVertex())
        s = V.pop(index=1)
        self.assertEqual(len(V), 2)
        self.assertIsInstance(s, adapter.SFFVertex)
        # polygons
        P = adapter.SFFPolygonList()
        p0 = adapter.SFFPolygon()
        P.append(p0)
        p1 = P.pop()
        self.assertEqual(len(P), 0)
        self.assertIsInstance(p1, adapter.SFFPolygon)
        self.assertEqual(p0.id, p1.id)  # ensure we are not creating a new one
        # pop with index
        P.append(adapter.SFFPolygon())
        P.append(adapter.SFFPolygon())
        P.append(adapter.SFFPolygon())
        s = P.pop(index=1)
        self.assertEqual(len(P), 2)
        self.assertIsInstance(s, adapter.SFFPolygon)
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
        # complexes
        C = adapter.SFFComplexList()
        _no_complexes = _random_integer(start=3, stop=10)
        _word = rw.random_word()
        [C.append(_word) for _ in _xrange(_no_complexes)]
        self.assertEqual(len(C), _no_complexes)
        C.remove(_word)
        self.assertEqual(len(C), _no_complexes - 1)
        C.remove(_word)
        self.assertEqual(len(C), _no_complexes - 2)
        # vertices
        V = adapter.SFFVertexList()
        v = adapter.SFFVertex(vID=1)
        V.append(v)
        self.assertEqual(len(V), 1)
        V.remove(v)
        self.assertEqual(len(V), 0)
        # polygons
        P = adapter.SFFPolygonList()
        p = adapter.SFFPolygon(PID=1)
        P.append(p)
        self.assertEqual(len(P), 1)
        P.remove(p)
        self.assertEqual(len(P), 0)
        # shapes
        Sh = adapter.SFFShapePrimitiveList()
        sh = adapter.SFFCuboid(id=1)
        Sh.append(sh)
        self.assertEqual(len(Sh), 1)
        Sh.remove(sh)
        self.assertEqual(len(Sh), 0)
        # exceptions
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            S.remove(_word)
        with self.assertRaisesRegex(base.SFFTypeError, r".*or int or str"):
            C.remove(adapter.SFFSegment())

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
        # vertices
        V = adapter.SFFVertexList()
        _no_verticess = _random_integer(start=1, stop=10)
        [V.append(adapter.SFFVertex(vID=i)) for i in _xrange(_no_verticess)]
        _ids = list(map(lambda v: v.id, V))
        V.reverse()
        _rids = list(map(lambda v: v.id, V))
        self.assertEqual(_ids[::-1], _rids)
        # polygon
        P = adapter.SFFPolygonList()
        _no_polygons = _random_integer(start=1, stop=10)
        [P.append(adapter.SFFPolygon(PID=i)) for i in _xrange(_no_polygons)]
        _ids = list(map(lambda p: p.id, P))
        P.reverse()
        _rids = list(map(lambda p: p.id, P))
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
        S.append(adapter.SFFSegment.from_gds_type(emdb_sff.segmentType()))
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # complexes
        C = adapter.SFFComplexList()
        [C.append(rw.random_word()) for _ in _xrange(_no_items)]
        self.assertEqual(list(C.get_ids()), list())
        # vertices
        V = adapter.SFFVertexList()
        [V.append(adapter.SFFVertex()) for _ in _xrange(_no_items)]
        self.assertEqual(list(V.get_ids()), list(_xrange(_no_items)))
        # polygons
        P = adapter.SFFPolygonList()
        [P.append(adapter.SFFPolygon()) for _ in _xrange(_no_items)]
        self.assertEqual(list(P.get_ids()), list(_xrange(_no_items)))
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


class TestSFFAttribute(Py23FixTestCase):
    """Test the attribute descriptor class"""

    def test_default(self):
        """Test default settings"""

        class _Colour(adapter.SFFType):
            gds_type = emdb_sff.rgbaType
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

    def test_error(self):
        """Test that we get an exception on setting wrong type"""

        class _Segmentation(adapter.SFFType):
            gds_type = emdb_sff.segmentation
            s = base.SFFAttribute('software', sff_type=adapter.SFFSoftware)

        _S = _Segmentation()
        with self.assertRaises(base.SFFTypeError):
            _S.s = adapter.SFFSegment()
