# -*- coding: utf-8 -*-
# test_adapter.py
"""
Unit for schema adapter
"""
from __future__ import print_function

import importlib
import json
import os
import random
import re
import sys
import tempfile
import unittest

import h5py
import numpy
from random_words import RandomWords, LoremIpsum

rw = RandomWords()
li = LoremIpsum()

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase, _random_float, _random_integers
from ..core import _xrange, _str, _bytes, _decode, _print
from ..schema import base

EMDB_SFF_VERSION = u'0.7.0.dev0'

adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
adapter = importlib.import_module(adapter_name)

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
emdb_sff = importlib.import_module(emdb_sff_name)

__author__ = u"Paul K. Korir, PhD"
__email__ = u"pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = u"2017-02-20"


# todo: add ID within each test method
class TestSFFSegmentation(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        # empty segmentation object
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.name = rw.random_word()
        segmentation.version = EMDB_SFF_VERSION
        segmentation.primary_descriptor = u"threeDVolume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4),
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4)
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4)
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = adapter.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = adapter.SFFLatticeList()
        # lattice 1
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)]).reshape(20, 20, 20)
        lattice = adapter.SFFLattice(
            mode=u'uint32',
            endianness=u'little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        lattice2 = adapter.SFFLattice(
            mode=u'float32',
            endianness=u'big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.append(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment()
        vol1_value = 1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segment.colour = adapter.SFFRGBA(random_colour=True)
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment()
        vol2_value = 37.1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=1,
            value=vol2_value
        )
        segment.colour = adapter.SFFRGBA(random_colour=True)
        # add segment to segments
        segments.append(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        cls.segmentation = segmentation
        cls.shape_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test_shape_segmentation.sff')
        cls.volume_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test_3d_segmentation.sff')
        cls.mesh_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test_mesh_segmentation.sff')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.shape_file):
            os.remove(cls.shape_file)
        if os.path.exists(cls.volume_file):
            os.remove(cls.volume_file)
        if os.path.exists(cls.mesh_file):
            os.remove(cls.mesh_file)

    def tearDown(self):
        adapter.SFFPolygon.reset_id()

    def test_create_3D(self):
        """Create an SFFSegmentation object with 3D volume segmentation from scratch"""
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.name = rw.random_word()
        segmentation.version = EMDB_SFF_VERSION
        segmentation.primary_descriptor = u"threeDVolume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = adapter.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = adapter.SFFLatticeList()
        # lattice 1
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)]).reshape(20, 20, 20)
        lattice = adapter.SFFLattice(
            mode=u'uint32',
            endianness=u'little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        lattice2 = adapter.SFFLattice(
            mode=u'float32',
            endianness=u'big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.append(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment()
        vol1_value = 1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment()
        vol2_value = 37.1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=1,
            value=vol2_value
        )
        # add segment to segments
        segments.append(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        # export
        segmentation.export(self.volume_file)
        # assertions
        self.assertEqual(segmentation.primary_descriptor, u"threeDVolume")
        self.assertEqual(segmentation.bounding_box.xmin, 0)
        self.assertEqual(segmentation.bounding_box.xmax, xmax)
        self.assertEqual(segmentation.bounding_box.ymin, 0)
        self.assertEqual(segmentation.bounding_box.ymax, ymax)
        self.assertEqual(segmentation.bounding_box.zmin, 0)
        self.assertEqual(segmentation.bounding_box.zmax, zmax)
        # test the number of transforms
        self.assertEqual(len(segmentation.transforms), 3)
        # test the transform IDs
        t_ids = map(lambda t: t.id, segmentation.transforms)
        self.assertCountEqual(t_ids, range(3))
        # segments
        self.assertEqual(len(segmentation.segments), 2)
        # segment one
        segment = segmentation.segments[0]
        # volume
        self.assertEqual(segment.volume.lattice_id, 0)
        self.assertEqual(segment.volume.value, vol1_value)
        # segment two
        segment = segmentation.segments.get_by_id(2)
        # volume
        self.assertEqual(segment.volume.lattice_id, 1)
        self.assertEqual(segment.volume.value, vol2_value)
        # lattices
        lattices = segmentation.lattices
        self.assertEqual(len(lattices), 2)
        # lattice one
        lattice1 = lattices.get_by_id(0)
        self.assertEqual(lattice1.mode, u'uint32')
        self.assertEqual(lattice1.endianness, u'little')
        self.assertCountEqual(lattice1.size.value, (20, 20, 20))
        self.assertCountEqual(lattice1.start.value, (0, 0, 0))
        # lattice two
        self.assertEqual(lattice2.mode, u'float32')
        self.assertEqual(lattice2.endianness, u'big')
        self.assertCountEqual(lattice2.size.value, (30, 40, 50))
        self.assertCountEqual(lattice2.start.value, (-50, -40, 100))

    def test_create_shapes(self):
        """Test that we can create a segmentation of shapes programmatically"""
        segmentation = adapter.SFFSegmentation()
        segmentation.name = rw.random_word()
        segmentation.version = EMDB_SFF_VERSION
        segmentation.software = adapter.SFFSoftware(
            name=rw.random_word(),
            version=rw.random_word(),
            processingDetails=li.get_sentence(),
        )
        segmentation.primary_descriptor = u"shapePrimitiveList"
        transforms = adapter.SFFTransformList()
        segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.append(cylinder)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        ellipsoid = adapter.SFFEllipsoid(
            x=_random_float() * 100,
            y=_random_float() * 100,
            z=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.append(ellipsoid)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        shapes.append(ellipsoid2)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        segment.shapes = shapes
        segments.append(segment)
        # more shapes
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCylinder(
                height=_random_float() * 100,
                diameter=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        segment.shapes = shapes
        segments.append(segment)
        segmentation.segments = segments
        segmentation.transforms = transforms
        # export
        segmentation.export(self.shape_file)
        # assertions
        self.assertEqual(len(segment.shapes), 9)
        self.assertEqual(segment.shapes.num_cones, 4)
        self.assertEqual(segment.shapes.num_cylinders, 1)
        self.assertEqual(segment.shapes.num_cuboids, 2)
        self.assertEqual(segment.shapes.num_ellipsoids, 2)

    def test_create_meshes(self):
        """Test that we can create a segmentation of meshes programmatically"""
        segmentation = adapter.SFFSegmentation()
        segmentation.name = rw.random_word()
        segmentation.version = EMDB_SFF_VERSION
        segmentation.primary_descriptor = u"meshList"
        segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        # meshes
        meshes = adapter.SFFMeshList()
        # mesh 1
        mesh = adapter.SFFMesh()
        # mesh 2
        mesh2 = adapter.SFFMesh()
        vertices1 = adapter.SFFVertexList()
        no_vertices1 = _random_integer(stop=100)
        for i in _xrange(no_vertices1):
            vertex = adapter.SFFVertex()
            vertex.point = tuple(
                map(float, (
                    _random_integer(1, 1000),
                    _random_integer(1, 1000),
                    _random_integer(1, 1000)
                ))
            )
            vertices1.append(vertex)
        polygons1 = adapter.SFFPolygonList()
        no_polygons1 = _random_integer(stop=100)
        for i in _xrange(no_polygons1):
            polygon = adapter.SFFPolygon()
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygons1.append(polygon)
        mesh.vertices = vertices1
        mesh.polygons = polygons1
        vertices2 = adapter.SFFVertexList()
        no_vertices2 = _random_integer(stop=100)
        for i in _xrange(no_vertices2):
            vertex = adapter.SFFVertex()
            vertex.point = tuple(map(float, (
                _random_integer(1, 1000), _random_integer(1, 1000), _random_integer(1, 1000))))
            vertices2.append(vertex)
        polygons2 = adapter.SFFPolygonList()
        no_polygons2 = _random_integer(stop=100)
        for i in _xrange(no_polygons2):
            polygon = adapter.SFFPolygon()
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygons2.append(polygon)
        mesh2.vertices = vertices2
        mesh2.polygons = polygons2
        meshes.append(mesh)
        meshes.append(mesh2)
        segment.meshes = meshes
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment()
        # mesh
        meshes = adapter.SFFMeshList()
        mesh = adapter.SFFMesh()
        vertices3 = adapter.SFFVertexList()
        no_vertices3 = _random_integer(stop=100)
        for i in _xrange(no_vertices3):
            vertex = adapter.SFFVertex()
            vertex.point = tuple(
                map(float, (
                    _random_integer(1, 1000),
                    _random_integer(1, 1000),
                    _random_integer(1, 1000)
                ))
            )
            vertices3.append(vertex)
        polygons3 = adapter.SFFPolygonList()
        no_polygons3 = _random_integer(stop=100)
        for i in _xrange(no_polygons3):
            polygon = adapter.SFFPolygon()
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygon.append(random.choice(range(_random_integer())))
            polygons3.append(polygon)
        mesh.vertices = vertices3
        mesh.polygons = polygons3
        meshes.append(mesh)
        segment.meshes = meshes
        segments.append(segment)
        segmentation.segments = segments
        # export
        segmentation.export(self.mesh_file)
        # assertions
        # segment one
        segment1 = segmentation.segments.get_by_id(1)
        self.assertEqual(len(segment1.meshes), 2)
        mesh1, mesh2 = segment1.meshes
        self.assertEqual(len(mesh1.vertices), no_vertices1)
        self.assertEqual(len(mesh1.polygons), no_polygons1)
        self.assertEqual(len(mesh2.vertices), no_vertices2)
        self.assertEqual(len(mesh2.polygons), no_polygons2)
        # segment two
        segment2 = segmentation.segments.get_by_id(2)
        mesh = segment2.meshes[0]
        self.assertEqual(len(segment2.meshes), 1)
        self.assertEqual(len(mesh.polygons), no_polygons3)
        self.assertEqual(len(mesh.vertices), no_vertices3)

    def test_create_annotations(self):
        """Test that we can add annotations programmatically"""
        segmentation = adapter.SFFSegmentation()  # annotation
        segmentation.name = u"name"
        segmentation.version = EMDB_SFF_VERSION
        segmentation.software = adapter.SFFSoftware(
            name=u"Software",
            version=u"1.0.9",
            processingDetails=u"Processing details"
        )
        segmentation.details = u"Details"
        # global external references
        segmentation.global_external_references = adapter.SFFGlobalExternalReferenceList()
        segmentation.global_external_references.append(
            adapter.SFFExternalReference(
                type=u'one',
                otherType=u'two',
                value=u'three'
            )
        )
        segmentation.global_external_references.append(
            adapter.SFFExternalReference(
                type=u'four',
                otherType=u'five',
                value=u'six'
            )
        )
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        biol_ann = adapter.SFFBiologicalAnnotation()
        biol_ann.name = u"Segment1"
        biol_ann.description = u"Some description"
        # external refs
        biol_ann.external_references = adapter.SFFExternalReferenceList()
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                type=u"sldjflj",
                value=u"doieaik"
            )
        )
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                type=u"sljd;f",
                value=u"20ijalf"
            )
        )
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                type=u"lsdjlsd",
                otherType=u"lsjfd;sd",
                value=u"23ijlsdjf"
            )
        )
        biol_ann.number_of_instances = 30
        segment.biological_annotation = biol_ann
        # complexes and macromolecules
        # complexes
        comp_mac = adapter.SFFComplexesAndMacromolecules()
        comp = adapter.SFFComplexList()
        comp.append(_str(_random_integer(1, 1000)))
        comp.append(_str(_random_integer(1, 1000)))
        comp.append(_str(_random_integer(1, 1000)))
        comp.append(_str(_random_integer(1, 1000)))
        comp.append(_str(_random_integer(1, 1000)))
        # macromolecules
        macr = adapter.SFFMacromoleculeList()
        macr.append(_str(_random_integer(1, 1000)))
        macr.append(_str(_random_integer(1, 1000)))
        macr.append(_str(_random_integer(1, 1000)))
        macr.append(_str(_random_integer(1, 1000)))
        macr.append(_str(_random_integer(1, 1000)))
        macr.append(_str(_random_integer(1, 1000)))
        comp_mac.complexes = comp
        comp_mac.macromolecules = macr
        segment.complexes_and_macromolecules = comp_mac
        # colour
        segment.colour = adapter.SFFRGBA(
            red=1,
            green=0,
            blue=1,
            alpha=0
        )
        segmentation.segments.append(segment)
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test_annotated_segmentation.sff'))
        # assertions
        self.assertEqual(segmentation.name, u'name')
        self.assertEqual(segmentation.version, segmentation._local.schemaVersion)  # automatically set
        self.assertEqual(segmentation.software.name, u"Software")
        self.assertEqual(segmentation.software.version, u"1.0.9")
        self.assertEqual(segmentation.software.processing_details, u"Processing details")
        self.assertEqual(segmentation.details, u"Details")
        # global external references
        self.assertEqual(segmentation.global_external_references[0].type, u'one')
        self.assertEqual(segmentation.global_external_references[0].other_type, u'two')
        self.assertEqual(segmentation.global_external_references[0].value, u'three')
        self.assertEqual(segmentation.global_external_references[1].type, u'four')
        self.assertEqual(segmentation.global_external_references[1].other_type, u'five')
        self.assertEqual(segmentation.global_external_references[1].value, u'six')
        # segment: biological_annotation
        self.assertEqual(segment.biological_annotation.name, u"Segment1")
        self.assertEqual(segment.biological_annotation.description, u"Some description")
        self.assertEqual(len(segment.biological_annotation.external_references), 3)
        self.assertEqual(segment.biological_annotation.external_references[0].type, u"sldjflj")
        self.assertEqual(segment.biological_annotation.external_references[0].value, u"doieaik")
        self.assertEqual(segment.biological_annotation.external_references[1].type, u"sljd;f")
        self.assertEqual(segment.biological_annotation.external_references[1].value, u"20ijalf")
        self.assertEqual(segment.biological_annotation.external_references[2].type, u"lsdjlsd")
        self.assertEqual(segment.biological_annotation.external_references[2].other_type, u"lsjfd;sd")
        self.assertEqual(segment.biological_annotation.external_references[2].value, u"23ijlsdjf")
        self.assertEqual(segment.biological_annotation.number_of_instances, 30)
        # segment: complexes_and_macromolecules
        # complexes
        self.assertEqual(len(segment.complexes_and_macromolecules.complexes), 5)
        complexes_bool = map(lambda c: isinstance(c, _str), segment.complexes_and_macromolecules.complexes)
        self.assertTrue(all(complexes_bool))
        # macromolecules
        self.assertEqual(len(segment.complexes_and_macromolecules.macromolecules), 6)
        macromolecules_bool = map(lambda c: isinstance(c, _str), segment.complexes_and_macromolecules.macromolecules)
        self.assertTrue(all(macromolecules_bool))
        # colour
        self.assertEqual(segment.colour.value, (1, 0, 1, 0))

    def test_segment_ids(self):
        """to ensure IDs are correctly reset"""
        # segmentation one
        segmentation = adapter.SFFSegmentation()
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        segmentation.segments.append(segment)
        # segmentation two
        segmentation2 = adapter.SFFSegmentation()
        segmentation2.segments = adapter.SFFSegmentList()
        segmentation2.segments.append(adapter.SFFSegment())
        # assertions
        self.assertEqual(segmentation.segments[0].id, segmentation2.segments[0].id)
        # segment two :: mainly to test that ids of mesh, contour, polygon, segment, shape, vertex reset
        # segment = segmentation.segments.get_by_id(1)
        # # mesh
        # self.assertEqual(segment.meshes[0].id, 0)
        # # polygon
        # self.assertEqual(segment.meshes[0].polygons[0].PID, 0)
        # # vertex
        # self.assertEqual(segment.meshes[0].vertices[0].vID, 0)
        # # shape
        # self.assertEqual(segment.shapes[0].id, 0)

    def test_transform_ids(self):
        """Test that transform ids work correctly"""
        transforms = adapter.SFFTransformList()
        matrix = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(_str, range(9))))
        transforms.append(matrix)

        transforms2 = adapter.SFFTransformList()
        matrix2 = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(_str, range(9))))
        transforms2.append(matrix2)

        self.assertIsNotNone(transforms[0].id)
        self.assertEqual(transforms[0].id, transforms2[0].id)

    def test_read_sff(self):
        """Read from XML (.sff) file"""
        sff_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'emd_1547.sff')
        segmentation = adapter.SFFSegmentation.from_file(sff_file)
        transform = segmentation.transforms[1]
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(segmentation.software.version, u"1.9.7")
        self.assertEqual(
            segmentation.software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")
        self.assertEqual(transform.rows, 3)
        self.assertEqual(transform.cols, 4)
        self.assertEqual(transform.data,
                         u"2.8 0.0 0.0 -226.8 0.0 2.8 0.0 -226.8 0.0 0.0 2.8 -226.8")

    def test_read_hff(self):
        """Read from HDF5 (.hff) file"""
        hff_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'emd_1547.hff')
        segmentation = adapter.SFFSegmentation.from_file(hff_file)
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(segmentation.software.version, u"1.9.7")
        self.assertEqual(
            segmentation.software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")
        self.assertEqual(segmentation.primary_descriptor, u"threeDVolume")

    def test_read_json(self):
        """Read from JSON (.json) file"""
        json_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'emd_1547.json')
        segmentation = adapter.SFFSegmentation.from_file(json_file)
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(segmentation.software.version, u"1.9.7")
        self.assertEqual(
            segmentation.software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")

    def test_export_sff(self):
        """Export to an XML (.sff) file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + u'.sff')
        # assertions
        with open(temp_file.name + u'.sff') as f:
            self.assertEqual(f.readline(), u'<?xml version="1.0" encoding="UTF-8"?>\n')

    def test_export_hff(self):
        """Export to an HDF5 file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + u'.hff')
        # assertions
        with open(temp_file.name + u'.hff', u'rb') as f:
            find = f.readline().find(b'HDF')
            self.assertGreaterEqual(find, 0)

    def test_export_json(self):
        """Export to a JSON file"""
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name += u'.json'
        self.segmentation.export(temp_file.name)
        # assertions
        with open(temp_file.name) as f:
            J = json.load(f)
            self.assertEqual(J[u'primaryDescriptor'], u"threeDVolume")


class TestSFFRGBA(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_hdf5_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test.hdf5')

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.test_hdf5_fn)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.red = random.random()
        self.green = random.random()
        self.blue = random.random()
        self.alpha = random.random()

    def test_default(self):
        """Test default colour"""
        colour = adapter.SFFRGBA()
        colour.red = self.red
        colour.green = self.green
        colour.blue = self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, 1.0)

    def test_kwarg_colour(self):
        """Test colour using kwargs"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_get_value(self):
        """Test colour.value"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        red, green, blue, alpha = colour.value
        self.assertEqual(colour.red, red)
        self.assertEqual(colour.green, green)
        self.assertEqual(colour.blue, blue)
        self.assertEqual(colour.alpha, alpha)

    def test_set_value(self):
        """Test colour.value = rgb(a)"""
        # rgb
        colour = adapter.SFFRGBA()
        colour.value = self.red, self.green, self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        # rgba
        colour.value = self.red, self.green, self.blue, self.alpha
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_as_hff(self):
        """Test convert to HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)

    def test_from_hff(self):
        """Test create from HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)
            colour2 = adapter.SFFRGBA.from_hff(h[u'container'])
            self.assertCountEqual(colour.value, colour2.value)

    def test_native_random_colour(self):
        """Test that using a kwarg random_colour will set random colours"""
        colour = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(0 <= colour.red <= 1)
        self.assertTrue(0 <= colour.green <= 1)
        self.assertTrue(0 <= colour.blue <= 1)
        self.assertTrue(0 <= colour.alpha <= 1)

    def test_validation(self):
        """Test that validation works"""
        c = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(c._is_valid())
        c = adapter.SFFRGBA()
        self.assertFalse(c._is_valid())

    def test_as_json(self):
        """Test export to JSON"""
        # empty
        c = adapter.SFFRGBA()
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            c.export(sys.stderr)
        # populated
        c = adapter.SFFRGBA(random_colour=True)
        c_json = c.as_json()
        # _print(c_json)
        self.assertEqual(c_json[u'colour'], c.value)

    def test_from_json(self):
        """Test import from JSON"""
        c_json = {'colour': (0.8000087483646712, 0.017170600210644427, 0.5992636068532492, 1.0)}
        c = adapter.SFFRGBA.from_json(c_json)
        # _print(c)
        self.assertEqual(c.value, c_json[u'colour'])


class TestSFFComplexList(Py23FixTestCase):
    """Tests for SFFComplexList class"""

    def test_default(self):
        """Test default settings"""
        c = adapter.SFFComplexList()
        self.assertEqual(c.gds_type, emdb_sff.complexType)
        self.assertRegex(_str(c), r"SFFComplexList\(\[.*\]\)")
        with self.assertRaises(StopIteration):  # because it's empty
            next(iter(c))
        c.append(rw.random_word())
        self.assertEqual(len(c), 1)
        c.append(rw.random_word())
        self.assertEqual(len(c), 2)
        c.clear()
        self.assertEqual(len(c), 0)


class TestSFFMacromoleculeList(Py23FixTestCase):
    def test_default(self):
        """Test default settings"""
        m = adapter.SFFMacromoleculeList()
        self.assertRegex(_str(m), r"SFFMacromoleculeList\(\[.*\]\)")
        with self.assertRaises(StopIteration):
            next(iter(m))
        m.append(rw.random_word())
        self.assertEqual(len(m), 1)
        m.append(rw.random_word())
        self.assertEqual(len(m), 2)
        m.clear()
        self.assertEqual(len(m), 0)


class TestSFFComplexesAndMacromolecules(Py23FixTestCase):
    def test_default(self):
        """Test default settings"""
        C = adapter.SFFComplexesAndMacromolecules()
        self.assertEqual(len(C.complexes), 0)
        self.assertEqual(len(C.macromolecules), 0)
        self.assertRegex(
            _str(C),
            r"SFFComplexesAndMacromolecules\(complexes=SFFComplexList\(\[.*\]\), macromolecules=SFFMacromoleculeList\(\[.*\]\)\)"
        )
        c = adapter.SFFComplexList()
        _no_items = _random_integer(start=2, stop=10)
        [c.append(rw.random_word()) for _ in _xrange(_no_items)]
        C.complexes = c
        m = adapter.SFFMacromoleculeList()
        [m.append(rw.random_word()) for _ in _xrange(_no_items)]
        C.macromolecules = m
        self.assertEqual(len(C.complexes), _no_items)
        self.assertEqual(len(C.macromolecules), _no_items)
        self.assertRegex(
            _str(C),
            r"SFFComplexesAndMacromolecules\(complexes=SFFComplexList\(.*\), macromolecules=SFFMacromoleculeList\(.*\)\)"
        )


class TestSFFExternalReference(Py23FixTestCase):
    def setUp(self):
        self.i = _random_integer()
        self.t = rw.random_word()
        self.o = rw.random_word()
        self.v = rw.random_word()
        self.l = u" ".join(rw.random_words(count=3))
        self.d = li.get_sentence()

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        e = adapter.SFFExternalReference(
            type=self.t,
            otherType=self.o,
            value=self.v,
            label=self.l,
            description=self.d
        )
        self.assertEqual(e.id, 0)
        self.assertEqual(e.type, self.t)
        self.assertEqual(e.other_type, self.o)
        self.assertEqual(e.value, self.v)
        self.assertEqual(e.label, self.l)
        self.assertEqual(e.description, self.d)
        self.assertEqual(
            _str(e),
            u"""SFFExternalReference(id={}, type="{}", otherType="{}", value="{}", label="{}", description="{}")""".format(
                0, self.t, self.o, self.v, self.l, self.d
            )
        )

    def test_from_gds_type(self):
        """Test that we can instantiate from gds_type"""
        _e = emdb_sff.externalReferenceType(
            id=self.i,
            type_=self.t,
            otherType=self.o,
            value=self.v,
            label=self.l,
            description=self.d,
        )
        e = adapter.SFFExternalReference.from_gds_type(_e)
        self.assertEqual(e.id, self.i)
        self.assertEqual(e.type, self.t)
        self.assertEqual(e.other_type, self.o)
        self.assertEqual(e.value, self.v)
        self.assertEqual(e.label, self.l)
        self.assertEqual(e.description, self.d)
        self.assertEqual(
            _str(e),
            u"""SFFExternalReference(id={}, type="{}", otherType="{}", value="{}", label="{}", description="{}")""".format(
                self.i, self.t, self.o, self.v, self.l, self.d
            )
        )

    def test_as_json(self):
        """Test that we can output as JSON"""
        e = adapter.SFFExternalReference(
            type=self.t,
            otherType=self.o,
            value=self.v,
            label=self.l,
            description=self.d,
        )
        e_json = e.as_json()
        self.assertEqual(e_json[u'id'], e.id)
        self.assertEqual(e_json[u'type'], e.type)
        self.assertEqual(e_json[u'otherType'], e.other_type)
        self.assertEqual(e_json[u'value'], e.value)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertEqual(e_json[u'description'], e.description)
        # missing mandatory
        e = adapter.SFFExternalReference(
            # type=self.t,
            # otherType=self.o,
            # value=self.v,
            label=self.l,
            description=self.d,
        )
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            e.export(sys.stderr)
        # missing non-mandatory
        e = adapter.SFFExternalReference(
            type=self.t,
            otherType=self.o,
            value=self.v,
            # label=self.l,
            # description=self.d,
        )
        self.assertEqual(e_json[u'type'], e.type)
        self.assertEqual(e_json[u'otherType'], e.other_type)
        self.assertEqual(e_json[u'value'], e.value)

    def test_from_json(self):
        """Test that we can recreate from JSON"""
        e_json = {'id': 0, 'type': 'symptom', 'otherType': 'thin', 'value': 'definitions',
                  'label': 'chairpersons swabs pools',
                  'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
                                 'semper semvestibulum curae lacusnulla.'}
        e = adapter.SFFExternalReference.from_json(e_json)
        self.assertEqual(e_json[u'id'], e.id)
        self.assertEqual(e_json[u'type'], e.type)
        self.assertEqual(e_json[u'otherType'], e.other_type)
        self.assertEqual(e_json[u'value'], e.value)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertEqual(e_json[u'description'], e.description)
        # missing mandatory
        e_json = {'id': 0, 'otherType': 'thin', 'value': 'definitions',
                  'label': 'chairpersons swabs pools',
                  'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
                                 'semper semvestibulum curae lacusnulla.'}
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            e = adapter.SFFExternalReference.from_json(e_json)
            e.export(sys.stderr)
        # missing non-mandatory
        e_json = {'type': 'symptom', 'otherType': 'thin', 'value': 'definitions',
                  'label': 'chairpersons swabs pools'}
        e = adapter.SFFExternalReference.from_json(e_json)
        self.assertIsNone(e.id)
        self.assertEqual(e_json[u'type'], e.type)
        self.assertEqual(e_json[u'otherType'], e.other_type)
        self.assertEqual(e_json[u'value'], e.value)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertIsNone(e.description)


class TestSFFExternalReferenceList(Py23FixTestCase):
    def setUp(self):
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.tt = [rw.random_word() for _ in _xrange(self._no_items)]
        self.oo = [rw.random_word() for _ in _xrange(self._no_items)]
        self.vv = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        ee = [adapter.SFFExternalReference(
            type=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in ee]
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(E), self._no_items)
        # get
        e = E[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.type, self.tt[self._no_items - 1])
        self.assertEqual(e.other_type, self.oo[self._no_items - 1])
        self.assertEqual(e.value, self.vv[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = E.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = E.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.type, self.tt[e_id])
        self.assertEqual(e.other_type, self.oo[e_id])
        self.assertEqual(e.value, self.vv[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _ee = [emdb_sff.externalReferenceType(
            id=self.ii[i],
            type_=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        _E = emdb_sff.externalReferencesType()
        _E.set_ref(_ee)
        E = adapter.SFFExternalReferenceList.from_gds_type(_E)
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(E), self._no_items)
        # get
        e = E[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.type, self.tt[self._no_items - 1])
        self.assertEqual(e.other_type, self.oo[self._no_items - 1])
        self.assertEqual(e.value, self.vv[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = E.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = E.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.type, self.tt[e_id])
        self.assertEqual(e.other_type, self.oo[e_id])
        self.assertEqual(e.value, self.vv[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_as_json(self):
        """Test that we can export to JSON"""
        ee = [adapter.SFFExternalReference(
            type=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in ee]
        E_json = E.as_json()
        # _print(E_json)
        for i in _xrange(self._no_items):
            self.assertEqual(E[i].id, E_json[i][u'id'])
            self.assertEqual(E[i].type, E_json[i][u'type'])
            self.assertEqual(E[i].other_type, E_json[i][u'otherType'])
            self.assertEqual(E[i].value, E_json[i][u'value'])
            self.assertEqual(E[i].label, E_json[i][u'label'])
            self.assertEqual(E[i].description, E_json[i][u'description'])
        # empty
        E = adapter.SFFExternalReferenceList()
        E_json = E.as_json()
        self.assertEqual(len(E), len(E_json))

    def test_from_json(self):
        """Test that we can import from JSON"""
        E_json = [{'id': 0, 'type': 'projectiles', 'otherType': 'blast', 'value': 'injector',
                   'label': 'bricks breaches crawl',
                   'description': 'Est facilisicurabitur morbi dapibus volutpat, vestibulumnulla consecteturpraesent velit sempermorbi diaminteger taciti risusdonec accusam.'},
                  {'id': 1, 'type': 'signals', 'otherType': 'wines', 'value': 'experience',
                   'label': 'alibi defaults showers',
                   'description': 'Auctor habitasse amet temporsuspendisse, integer hendrerit nullasuspendisse.'},
                  {'id': 2, 'type': 'openings', 'otherType': 'pack', 'value': 'augmentations',
                   'label': 'outing rings tilling',
                   'description': 'Liberoduis esse nobis semvestibulum bibendumin non, sagittis eget eum massapellentesque eratproin nonummy massaphasellus.'},
                  {'id': 3, 'type': 'blaze', 'otherType': 'contract', 'value': 'diagrams',
                   'label': 'sewers weddings telecommunications',
                   'description': 'Ipsum no luctus ultricies enimsed antesuspendisse.'},
                  {'id': 4, 'type': 'terms', 'otherType': 'blackboard', 'value': 'nothing',
                   'label': 'depot trades strikers', 'description': 'Elitr hendrerit tortorvestibulum exerci.'},
                  {'id': 5, 'type': 'carriage', 'otherType': 'screens', 'value': 'apprehension',
                   'label': 'signalers hunk wagon', 'description': 'Consequatduis muspellentesque.'},
                  {'id': 6, 'type': 'lot', 'otherType': 'gums', 'value': 'rim', 'label': 'chatter north clearances',
                   'description': 'Nostra felis.'},
                  {'id': 7, 'type': 'outlet', 'otherType': 'actions', 'value': 'twists',
                   'label': 'compromises additives mirrors',
                   'description': 'Diaminteger phasellus mi sollicitudin laoreetphasellus possim, himenaeos semvestibulum egestasmauris clita elitnunc suscipit pulvinar.'},
                  {'id': 8, 'type': 'shears', 'otherType': 'user', 'value': 'view', 'label': 'cable diagram churns',
                   'description': 'Dolor laoreet adipiscing takimata neque dignissim velit enimaliquam, lobortisetiam mazim nunccurabitur aliquip praesent blandit.'},
                  {'id': 9, 'type': 'jurisdiction', 'otherType': 'plug', 'value': 'calibrations',
                   'label': 'oscillation baby males', 'description': 'Iusto aliquam quod orci, aaenean justo luctus.'}]
        E = adapter.SFFExternalReferenceList.from_json(E_json)
        # _print(E)
        for i, extref in enumerate(E_json):
            self.assertEqual(E[i].id, extref[u'id'])
            self.assertEqual(E[i].type, extref[u'type'])
            self.assertEqual(E[i].other_type, extref[u'otherType'])
            self.assertEqual(E[i].value, extref[u'value'])
            self.assertEqual(E[i].label, extref[u'label'])
            self.assertEqual(E[i].description, extref[u'description'])
        # invalid
        E_json = "sldjfl"  # iterable but invalid
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            e = adapter.SFFExternalReferenceList.from_json(E_json)
            self.stderr(e)
            e.export(sys.stderr)


class TestSFFBiologicalAnnotation(Py23FixTestCase):
    def setUp(self):
        self.name = " ".join(rw.random_words(count=3))
        self.description = li.get_sentence()
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.tt = [rw.random_word() for _ in _xrange(self._no_items)]
        self.oo = [rw.random_word() for _ in _xrange(self._no_items)]
        self.vv = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]
        self.ee = [adapter.SFFExternalReference(
            type=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        self._ee = [emdb_sff.externalReferenceType(
            type_=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in self.ee]
        _E = emdb_sff.externalReferencesType()
        _E.set_ref(self._ee)
        self.external_references = E
        self._external_references = _E
        self.no = _random_integer()

    def test_default(self):
        """Test default settings"""
        b = adapter.SFFBiologicalAnnotation(
            name=self.name,
            description=self.description,
            externalReferences=self.external_references,
            numberOfInstances=self.no,
        )
        self.assertRegex(
            _str(b),
            r"""SFFBiologicalAnnotation\(""" \
            r"""name="{}", description="{}", """ \
            r"""numberOfInstances={}, """ \
            r"""externalReferences=SFFExternalReferenceList\(\[.*\]\)\)""".format(
                self.name,
                self.description,
                self.no
            )
        )
        self.assertEqual(b.name, self.name)
        self.assertEqual(b.description, self.description)
        self.assertEqual(b.number_of_instances, self.no)
        self.assertEqual(b.external_references, self.external_references)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _b = emdb_sff.biologicalAnnotationType(
            name=self.name,
            description=self.description,
            numberOfInstances=self.no,
            externalReferences=self._external_references
        )
        b = adapter.SFFBiologicalAnnotation.from_gds_type(_b)
        self.assertRegex(
            _str(b),
            r"""SFFBiologicalAnnotation\(""" \
            r"""name="{}", description="{}", """ \
            r"""numberOfInstances={}, """ \
            r"""externalReferences=SFFExternalReferenceList\(\[.*\]\)\)""".format(
                self.name,
                self.description,
                self.no
            )
        )
        self.assertEqual(b.name, self.name)
        self.assertEqual(b.description, self.description)
        self.assertEqual(b.number_of_instances, self.no)
        self.assertEqual(b.external_references, self.external_references)

    def test_hff(self):
        """Test conversion to and from HDF5"""
        # empty case
        b_empty = adapter.SFFBiologicalAnnotation()
        # _print(b_empty)
        hff_f = tempfile.NamedTemporaryFile()
        hff_f.name += '.hff'
        with h5py.File(hff_f.name, 'w') as h:
            group = h.create_group(u'test')
            group = b_empty.as_hff(group)

            b2_empty = adapter.SFFBiologicalAnnotation.from_hff(group[u'biologicalAnnotation'])
            # _print(b2_empty)

            self.assertEqual(b_empty.name, b2_empty.name)
            self.assertEqual(b_empty.name, b2_empty.name)
            self.assertEqual(b_empty.description, b2_empty.description)
            self.assertEqual(b_empty.number_of_instances, b2_empty.number_of_instances)
            self.assertEqual(b_empty.external_references, b2_empty.external_references)
        # get rid of the file
        os.remove(hff_f.name)

        # non-empty case
        b_full = adapter.SFFBiologicalAnnotation()
        b_full.name = ' '.join(rw.random_words(count=2))
        b_full.description = li.get_sentence()
        es = adapter.SFFExternalReferenceList()
        no_es = _random_integer(2, 10)
        for _ in _xrange(no_es):
            e = adapter.SFFExternalReference()
            e.type = rw.random_word()
            e.other_type = rw.random_word()
            e.value = rw.random_word()
            e.label = ' '.join(rw.random_words(count=3))
            e.description = li.get_sentence()
            es.append(e)
        b_full.external_references = es
        hff_f = tempfile.NamedTemporaryFile()
        hff_f.name += '.hff'
        # _print(b_full)
        with h5py.File(hff_f.name, 'w') as h:
            group = h.create_group(u'test')
            group = b_full.as_hff(group)

            b2_full = adapter.SFFBiologicalAnnotation.from_hff(group[u'biologicalAnnotation'])
            # _print(b2_full)

            self.assertEqual(b_full.name, b2_full.name)
            self.assertEqual(b_full.name, b2_full.name)
            self.assertEqual(b_full.description, b2_full.description)
            self.assertEqual(b_full.number_of_instances, b2_full.number_of_instances)
            self.assertEqual(b_full.external_references, b2_full.external_references)
        # get rid of the file
        os.remove(hff_f.name)

    def test_json(self):
        """Test conversion to and from JSON"""
        # empty case
        b_empty = adapter.SFFBiologicalAnnotation()
        # # _print(b_empty)
        b_json = b_empty.as_json()
        # _print(b_json)
        b2_empty = adapter.SFFBiologicalAnnotation.from_json(b_json)
        # _print(b2_empty)
        self.assertEqual(b_empty, b2_empty)
        # non-empty case
        b_full = adapter.SFFBiologicalAnnotation()
        b_full.name = ' '.join(rw.random_words(count=2))
        b_full.description = li.get_sentence()
        es = adapter.SFFExternalReferenceList()
        no_es = _random_integer(2, 10)
        for _ in _xrange(no_es):
            e = adapter.SFFExternalReference()
            e.type = rw.random_word()
            e.other_type = rw.random_word()
            e.value = rw.random_word()
            e.label = ' '.join(rw.random_words(count=3))
            e.description = li.get_sentence()
            es.append(e)
        b_full.external_references = es
        b_json = b_full.as_json()
        # _print(b_json)
        b2_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
        # _print(b2_full)
        self.assertEqual(b_full, b2_full)

    def test_from_json(self):
        """Test that we can import from JSON"""
        b_json = {'name': 'returns agent', 'description': 'Lacus leopraesent risusdonec tempus congue.',
                  'externalReferences': [{'id': 0, 'type': 'listing', 'otherType': 'antennas', 'value': 'weddings',
                                          'label': 'times selection deployment',
                                          'description': 'Facilisicurabitur mi sanctus fames dignissim autem.'},
                                         {'id': 1, 'type': 'basis', 'otherType': 'leaks', 'value': 'cups',
                                          'label': 'yaw workloads house', 'description': 'Nequeetiam habitasse.'},
                                         {'id': 2, 'type': 'chance', 'otherType': 'theory', 'value': 'allegation',
                                          'label': 'maps chairwomen flashes',
                                          'description': 'Suscipit eos pulvinar zzril doming dolores.'}]}
        b_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
        # _print(b_full)
        self.assertEqual(b_full.name, b_json[u'name'])
        self.assertEqual(b_full.description, b_json[u'description'])
        try:
            self.assertEqual(b_full.number_of_instances, b_json[u'numberOfInstances'])
        except KeyError:
            self.assertEqual(b_full.number_of_instances, 1)
        for i, extref in enumerate(b_json[u'externalReferences']):
            self.assertEqual(b_full.external_references[i].id, extref[u'id'])
            self.assertEqual(b_full.external_references[i].type, extref[u'type'])
            self.assertEqual(b_full.external_references[i].other_type, extref[u'otherType'])
            self.assertEqual(b_full.external_references[i].value, extref[u'value'])
            self.assertEqual(b_full.external_references[i].label, extref[u'label'])
            self.assertEqual(b_full.external_references[i].description, extref[u'description'])


class TestSFFThreeDVolume(Py23FixTestCase):
    def setUp(self):
        self.lattice_id = _random_integer()
        self.value = _random_integer()
        self.transform_id = _random_integer()

    def test_default(self):
        """Test default settings"""
        v = adapter.SFFThreeDVolume(
            latticeId=self.lattice_id,
            value=self.value,
            transformId=self.transform_id,
        )
        self.assertEqual(
            _str(v),
            """SFFThreeDVolume(latticeId={}, value={}, transformId={})""".format(
                self.lattice_id,
                self.value,
                self.transform_id
            )
        )
        self.assertEqual(v.lattice_id, self.lattice_id)
        self.assertEqual(v.value, self.value)
        self.assertEqual(v.transform_id, self.transform_id)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _v = emdb_sff.threeDVolumeType(
            latticeId=self.lattice_id,
            value=self.value,
            transformId=self.transform_id
        )
        v = adapter.SFFThreeDVolume.from_gds_type(_v)
        self.assertEqual(
            _str(v),
            """SFFThreeDVolume(latticeId={}, value={}, transformId={})""".format(
                self.lattice_id,
                self.value,
                self.transform_id
            )
        )
        self.assertEqual(v.lattice_id, self.lattice_id)
        self.assertEqual(v.value, self.value)
        self.assertEqual(v.transform_id, self.transform_id)


class TestSFFVolumeStructure(Py23FixTestCase):
    def setUp(self):
        self.cols = _random_integer()
        self.rows = _random_integer()
        self.sections = _random_integer()

    def test_default(self):
        """Test default settings"""
        vs = adapter.SFFVolumeStructure(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertRegex(_str(vs), r"SFFVolumeStructure\(cols.*rows.*sections.*\)")
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.voxel_count, self.cols * self.rows * self.sections)

    def test_get_set_value(self):
        """Test the .value attribute"""
        vs = adapter.SFFVolumeStructure(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.value, (self.cols, self.rows, self.sections))
        _c, _r, _s = _random_integer(), _random_integer(), _random_integer()
        vs.value = _c, _r, _s
        self.assertEqual(vs.value, (_c, _r, _s))
        self.assertEqual(vs.cols, _c)
        self.assertEqual(vs.rows, _r)
        self.assertEqual(vs.sections, _s)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _vs = emdb_sff.volumeStructureType(cols=self.cols, rows=self.rows, sections=self.sections)
        vs = adapter.SFFVolumeStructure.from_gds_type(_vs)
        self.assertRegex(_str(vs), r"SFFVolumeStructure\(cols.*rows.*sections.*\)")
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.voxel_count, self.cols * self.rows * self.sections)


class TestSFFVolumeIndex(Py23FixTestCase):
    def setUp(self):
        self.cols = _random_integer()
        self.rows = _random_integer()
        self.sections = _random_integer()

    def test_default(self):
        """Test default settings"""
        vi = adapter.SFFVolumeIndex(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(cols.*rows.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _vi = emdb_sff.volumeIndexType(cols=self.cols, rows=self.rows, sections=self.sections)
        vi = adapter.SFFVolumeIndex.from_gds_type(_vi)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(cols.*rows.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)


class TestSFFLattice(Py23FixTestCase):
    def setUp(self):
        adapter.SFFLattice.reset_id()
        self.r, self.c, self.s = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10), _random_integer(
            start=2, stop=10)
        self.l_mode = u'float64'
        self.l_endian = u'little'
        self.l_size = adapter.SFFVolumeStructure(rows=self.r, cols=self.c, sections=self.s)
        self.l_start = adapter.SFFVolumeIndex(rows=0, cols=0, sections=0)
        self.l_data = numpy.random.rand(self.r, self.c, self.s)
        self.l_bytes = adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian)
        self.l_unicode = self.l_bytes.decode(u'utf-8')

    def tearDown(self):
        adapter.SFFLattice.reset_id()

    def test_create_init_array(self):
        """Test that we can create from a numpy array using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_data
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
        )

    def test_create_init_bytes(self):
        """Test that we can create from bytes using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_bytes
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8"),
            )
        )

    def test_create_init_unicode(self):
        """Test that we can create from unicode using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_unicode
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
        )

    def test_create_classmethod_array(self):
        """Test that we can create an object using the classmethod"""
        l = adapter.SFFLattice.from_array(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_data
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8"),
            )
        )

    def test_create_classmethod_bytes(self):
        """Test that we can create an object using the classmethod"""
        l = adapter.SFFLattice.from_bytes(
            self.l_bytes,
            self.l_size,
            mode=self.l_mode,
            endianness=self.l_endian,
            start=self.l_start,
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
        )
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            l = adapter.SFFLattice.from_bytes(
                self.l_bytes,
                (self.r, self.c, self.s),
                mode=self.l_mode,
                endianness=self.l_endian,
                start=self.l_start,
            )

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        r, c, s = _random_integer(start=3, stop=10), _random_integer(start=3, stop=10), _random_integer(start=3,
                                                                                                        stop=10)
        _data = numpy.random.randint(low=0, high=100, size=(r, c, s))
        mode_ = u'uint8'
        _bytes = adapter.SFFLattice._encode(_data, endianness=u'big', mode=mode_)
        _l = emdb_sff.latticeType(
            mode=mode_,
            endianness=u'big',
            size=emdb_sff.volumeStructureType(cols=c, rows=r, sections=s),
            start=emdb_sff.volumeIndexType(cols=0, rows=0, sections=0),
            data=_bytes
        )
        l = adapter.SFFLattice.from_gds_type(_l)
        self.assertTrue(hasattr(l, u'data_array'))


class TestSFFMesh(Py23FixTestCase):
    """Test the SFFMesh class"""

    def setUp(self):
        adapter.SFFMesh.reset_id()
        adapter.SFFPolygon.reset_id()
        adapter.SFFVertex.reset_id()
        self._no_vertices = _random_integer(start=2, stop=20)
        self._no_polygons = _random_integer(start=2, stop=20)
        self._vertices = emdb_sff.vertexListType()
        self._vertices.set_v([
            emdb_sff.vertexType(
                vID=i,
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for i in _xrange(self._no_vertices)
        ])
        self.vertices = adapter.SFFVertexList.from_gds_type(self._vertices)
        self._polygons = emdb_sff.polygonListType()
        self._polygons.set_P([
            emdb_sff.polygonType(
                PID=i,
                v=[
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                ]
            ) for i in _xrange(self._no_polygons)])
        self.polygons = adapter.SFFPolygonList.from_gds_type(self._polygons)

    def tearDown(self):
        adapter.SFFMesh.reset_id()
        adapter.SFFPolygon.reset_id()
        adapter.SFFVertex.reset_id()

    def test_default(self):
        """Test default settings"""
        m = adapter.SFFMesh(vertexList=self.vertices, polygonList=self.polygons)
        self.assertRegex(
            _str(m),
            r"""SFFMesh\(id=(\d+|None), vertexList=SFFVertexList\(\[.*\]\), polygonList=SFFPolygonList\(\[.*\]\)\)"""
        )
        self.assertEqual(m.id, 0)
        self.assertEqual(m.vertices, self.vertices)
        self.assertEqual(m.polygons, self.polygons)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _m = emdb_sff.meshType(vertexList=self._vertices, polygonList=self._polygons)
        m = adapter.SFFMesh.from_gds_type(_m)
        self.assertRegex(
            _str(m),
            r"""SFFMesh\(id=(\d+|None), vertexList=SFFVertexList\(\[.*\]\), polygonList=SFFPolygonList\(\[.*\]\)\)"""
        )
        self.assertIsNone(m.id)
        self.assertEqual(m.vertices, self.vertices)
        self.assertEqual(m.polygons, self.polygons)


class TestSFFMeshList(Py23FixTestCase):
    """Test the SFFMeshList class"""

    def tearDown(self):
        adapter.SFFMesh.reset_id()
        adapter.SFFPolygon.reset_id()
        adapter.SFFVertex.reset_id()

    @staticmethod
    def generate_sff_data(no_verts=_random_integer(start=2, stop=20), no_polys=_random_integer(start=2, stop=20)):
        vertices = adapter.SFFVertexList()
        [vertices.append(
            adapter.SFFVertex(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ) for _ in _xrange(no_verts)]
        polygons = adapter.SFFPolygonList()
        [polygons.append(
            adapter.SFFPolygon(
                v=[
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20)
                ]
            )
        ) for _ in _xrange(no_polys)]
        return vertices, polygons

    @staticmethod
    def generate_gds_data(no_verts=_random_integer(start=2, stop=20), no_polys=_random_integer(start=2, stop=20)):
        vertices = emdb_sff.vertexListType()
        vertices.set_v([
            emdb_sff.vertexType(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_verts)]
        )
        polygons = emdb_sff.polygonListType()
        polygons.set_P([
            emdb_sff.polygonType(
                v=[
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20)
                ]
            ) for _ in _xrange(no_polys)]
        )
        return vertices, polygons

    def test_default(self):
        """Test default settings"""
        _no_items = _random_integer(start=2, stop=10)
        M = adapter.SFFMeshList()
        for _ in _xrange(_no_items):
            vs, ps = TestSFFMeshList.generate_sff_data()
            M.append(adapter.SFFMesh(vertexList=vs, polygonList=ps))
        self.assertRegex(
            _str(M),
            r"""SFFMeshList\(\[.*\]\)"""
        )
        self.assertEqual(len(M), _no_items)
        self.assertEqual(list(M.get_ids()), list(_xrange(_no_items)))
        m_id = random.choice(list(M.get_ids()))
        m = M.get_by_id(m_id)
        self.assertIsInstance(m, adapter.SFFMesh)
        self.assertEqual(m.id, m_id)
        self.assertTrue(len(m.vertices) > 0)
        self.assertTrue(len(m.polygons) > 0)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _no_items = _random_integer(start=2, stop=10)
        _M = emdb_sff.meshListType()
        for i in _xrange(_no_items):
            vs, ps = TestSFFMeshList.generate_gds_data()
            _M.add_mesh(emdb_sff.meshType(id=i, vertexList=vs, polygonList=ps))
        M = adapter.SFFMeshList.from_gds_type(_M)
        self.assertRegex(
            _str(M),
            r"""SFFMeshList\(\[.*\]\)"""
        )
        self.assertEqual(len(M), _no_items)
        self.assertEqual(list(M.get_ids()), list(_xrange(_no_items)))
        m_id = random.choice(list(M.get_ids()))
        m = M.get_by_id(m_id)
        self.assertIsInstance(m, adapter.SFFMesh)
        self.assertEqual(m.id, m_id)
        self.assertTrue(len(m.vertices) > 0)
        self.assertTrue(len(m.polygons) > 0)


class TestSFFBoundingBox(Py23FixTestCase):
    """Test the SFFBoundingBox class"""

    def test_default(self):
        """Test default settings"""
        B = adapter.SFFBoundingBox()
        self.assertRegex(
            _str(B),
            r"""SFFBoundingBox\(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={}\)""".format(
                B.xmin, B.xmax,
                B.ymin, B.ymax,
                B.zmin, B.zmax,
            )
        )
        self.assertEqual(B.xmin, 0)
        self.assertIsNone(B.xmax)
        self.assertEqual(B.ymin, 0)
        self.assertIsNone(B.ymax)
        self.assertEqual(B.zmin, 0)
        self.assertIsNone(B.zmax)
        _xmin = _random_float(1)
        _xmax = _random_float(1000)
        _ymin = _random_float(1)
        _ymax = _random_float(1000)
        _zmin = _random_float(1)
        _zmax = _random_float(1000)
        B = adapter.SFFBoundingBox(
            xmin=_xmin,
            xmax=_xmax,
            ymin=_ymin,
            ymax=_ymax,
            zmin=_zmin,
            zmax=_zmax,
        )
        self.assertEqual(B.xmin, _xmin)
        self.assertEqual(B.xmax, _xmax)
        self.assertEqual(B.ymin, _ymin)
        self.assertEqual(B.ymax, _ymax)
        self.assertEqual(B.zmin, _zmin)
        self.assertEqual(B.zmax, _zmax)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _B = emdb_sff.boundingBoxType()
        B = adapter.SFFBoundingBox.from_gds_type(_B)
        self.assertRegex(
            _str(B),
            r"""SFFBoundingBox\(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={}\)""".format(
                B.xmin, B.xmax,
                B.ymin, B.ymax,
                B.zmin, B.zmax,
            )
        )
        self.assertEqual(B.xmin, 0)
        self.assertIsNone(B.xmax)
        self.assertEqual(B.ymin, 0)
        self.assertIsNone(B.ymax)
        self.assertEqual(B.zmin, 0)
        self.assertIsNone(B.zmax)
        _xmin = _random_float(1)
        _xmax = _random_float(1000)
        _ymin = _random_float(1)
        _ymax = _random_float(1000)
        _zmin = _random_float(1)
        _zmax = _random_float(1000)
        _B = emdb_sff.boundingBoxType(
            xmin=_xmin,
            xmax=_xmax,
            ymin=_ymin,
            ymax=_ymax,
            zmin=_zmin,
            zmax=_zmax,
        )
        B = adapter.SFFBoundingBox.from_gds_type(_B)
        self.assertEqual(B.xmin, _xmin)
        self.assertEqual(B.xmax, _xmax)
        self.assertEqual(B.ymin, _ymin)
        self.assertEqual(B.ymax, _ymax)
        self.assertEqual(B.zmin, _zmin)
        self.assertEqual(B.zmax, _zmax)

    def test_as_json(self):
        """Test export to JSON"""
        # full
        x0, x1, y0, y1, z0, z1 = _random_integers(count=6)
        bb = adapter.SFFBoundingBox(
            xmin=x0, xmax=x1,
            ymin=y0, ymax=y1,
            zmin=z0, zmax=z1
        )
        _print(bb)
        bb_json = bb.as_json()
        _print(bb_json)
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertEqual(bb.xmax, bb_json[u'xmax'])
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertEqual(bb.ymax, bb_json[u'ymax'])
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertEqual(bb.zmax, bb_json[u'zmax'])
        # empty
        bb = adapter.SFFBoundingBox()
        bb_json = bb.as_json()
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertIsNone(bb.xmax)
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertIsNone(bb.ymax)
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertIsNone(bb.zmax)

    def test_from_json(self):
        """Test import from JSON"""
        # full
        bb_json = {'xmin': 640.0, 'xmax': 348.0, 'ymin': 401.0, 'ymax': 176.0, 'zmin': 491.0, 'zmax': 349.0}
        bb = adapter.SFFBoundingBox.from_json(bb_json)
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertEqual(bb.xmax, bb_json[u'xmax'])
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertEqual(bb.ymax, bb_json[u'ymax'])
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertEqual(bb.zmax, bb_json[u'zmax'])
        # empty
        bb_json = {}
        bb = adapter.SFFBoundingBox.from_json(bb_json)
        self.assertEqual(bb.xmin, 0)
        self.assertIsNone(bb.xmax)
        self.assertEqual(bb.ymin, 0)
        self.assertIsNone(bb.ymax)
        self.assertEqual(bb.zmin, 0)
        self.assertIsNone(bb.zmax)


class TestSFFCone(Py23FixTestCase):
    """Test the SFFCone class"""

    def setUp(self):
        adapter.SFFShape.reset_id()

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCone()
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottomRadius={}, transformId={}\)""".format(
                0, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        C = adapter.SFFCone(
            height=_height, bottomRadius=_bottom_radius, transformId=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottomRadius={}, transformId={}\)""".format(
                1, _height, _bottom_radius, _transform_id
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.height, _height)
        self.assertEqual(C.bottom_radius, _bottom_radius)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cone()
        C = adapter.SFFCone.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottomRadius={}, transformId={}\)""".format(
                None, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cone(
            height=_height, bottomRadius=_bottom_radius, transformId=_transform_id
        )
        C = adapter.SFFCone.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottomRadius={}, transformId={}\)""".format(
                None, _height, _bottom_radius, _transform_id
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.bottom_radius, _bottom_radius)


class TestSFFCuboid(Py23FixTestCase):
    """Test the SFFCuboid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCuboid()
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                0, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCuboid(x=_x, y=_y, z=_z, transformId=_transform_id)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                1, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cuboid()
        C = adapter.SFFCuboid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.cuboid(x=_x, y=_y, z=_z, transformId=_transform_id)
        C = adapter.SFFCuboid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                None, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)


class TestSFFCylinder(Py23FixTestCase):
    """Test the SFFCylinder class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCylinder()
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transformId={}\)""".format(
                0, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCylinder(
            height=_height, diameter=_diameter, transformId=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transformId={}\)""".format(
                1, _height, _diameter, _transform_id
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.height, _height)
        self.assertEqual(C.diameter, _diameter)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cylinder()
        C = adapter.SFFCylinder.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transformId={}\)""".format(
                None, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cylinder(
            height=_height, diameter=_diameter, transformId=_transform_id
        )
        C = adapter.SFFCylinder.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transformId={}\)""".format(
                None, _height, _diameter, _transform_id
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.diameter, _diameter)


class TestSFFEllipsoid(Py23FixTestCase):
    """Test the SFFEllipsoid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        E = adapter.SFFEllipsoid()
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                0, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        E = adapter.SFFEllipsoid(x=_x, y=_y, z=_z, transformId=_transform_id)
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                1, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(E.id, 1)  # the second one we have created
        self.assertEqual(E.x, _x)
        self.assertEqual(E.y, _y)
        self.assertEqual(E.z, _z)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.ellipsoid()
        C = adapter.SFFEllipsoid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.ellipsoid(x=_x, y=_y, z=_z, transformId=_transform_id)
        C = adapter.SFFEllipsoid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transformId={}\)""".format(
                None, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)


class TestSFFGlobalExternalReferenceList(Py23FixTestCase):
    """Test the SFFGlobalExternalReferenceList class"""

    def setUp(self):
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.tt = [rw.random_word() for _ in _xrange(self._no_items)]
        self.oo = [rw.random_word() for _ in _xrange(self._no_items)]
        self.vv = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        ee = [adapter.SFFExternalReference(
            type=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        G = adapter.SFFGlobalExternalReferenceList()
        [G.append(e) for e in ee]
        # str
        self.assertRegex(
            _str(G),
            r"""SFFGlobalExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(G), self._no_items)
        # get
        e = G[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.type, self.tt[self._no_items - 1])
        self.assertEqual(e.other_type, self.oo[self._no_items - 1])
        self.assertEqual(e.value, self.vv[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = G.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = G.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.type, self.tt[e_id])
        self.assertEqual(e.other_type, self.oo[e_id])
        self.assertEqual(e.value, self.vv[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _ee = [emdb_sff.externalReferenceType(
            id=self.ii[i],
            type_=self.tt[i],
            otherType=self.oo[i],
            value=self.vv[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        _G = emdb_sff.globalExternalReferencesType()
        _G.set_ref(_ee)
        G = adapter.SFFGlobalExternalReferenceList.from_gds_type(_G)
        # str
        self.assertRegex(
            _str(G),
            r"""SFFGlobalExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(G), self._no_items)
        # get
        e = G[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.type, self.tt[self._no_items - 1])
        self.assertEqual(e.other_type, self.oo[self._no_items - 1])
        self.assertEqual(e.value, self.vv[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = G.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = G.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.type, self.tt[e_id])
        self.assertEqual(e.other_type, self.oo[e_id])
        self.assertEqual(e.value, self.vv[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])


class TestSFFLatticeList(Py23FixTestCase):
    """Test the SFFLatticeList class"""

    @staticmethod
    def generate_sff_data(
            rows=_random_integer(start=10, stop=20),
            cols=_random_integer(start=10, stop=20),
            sections=_random_integer(start=10, stop=20)
    ):
        mode = random.choice(list(adapter.FORMAT_CHARS.keys()))
        endianness = random.choice(list(adapter.ENDIANNESS.keys()))
        size = adapter.SFFVolumeStructure(rows=rows, cols=cols, sections=sections)
        start = adapter.SFFVolumeIndex(rows=0, cols=0, sections=0)
        if re.match(r".*int.*", mode):
            data = numpy.random.randint(0, 100, size=(rows, cols, sections))
        elif re.match(r".*float.*", mode):
            data = numpy.random.rand(rows, cols, sections)
        return mode, endianness, size, start, data

    @staticmethod
    def generate_gds_data(
            rows=_random_integer(start=10, stop=20),
            cols=_random_integer(start=10, stop=20),
            sections=_random_integer(start=10, stop=20)
    ):
        mode = random.choice(list(adapter.FORMAT_CHARS.keys()))
        endianness = random.choice(list(adapter.ENDIANNESS.keys()))
        size = emdb_sff.volumeStructureType(rows=rows, cols=cols, sections=sections)
        start = emdb_sff.volumeIndexType(rows=0, cols=0, sections=0)
        if re.match(r".*int.*", mode):
            _data = numpy.random.randint(0, 100, size=(rows, cols, sections))
        elif re.match(r".*float.*", mode):
            _data = numpy.random.rand(rows, cols, sections)
        data = adapter.SFFLattice._encode(_data, mode=mode, endianness=endianness)
        return mode, endianness, size, start, data

    def test_default(self):
        """Test default settings"""
        L = adapter.SFFLatticeList()
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[.*\]\)"""
        )
        self.assertEqual(len(L), 0)
        _no_items = _random_integer(start=2, stop=5)
        for _ in _xrange(_no_items):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_sff_data()
            L.append(
                adapter.SFFLattice(
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[SFFLattice\(.*\]\)"""
        )
        self.assertEqual(len(L), _no_items)
        self.assertEqual(list(L.get_ids()), list(_xrange(_no_items)))
        l_id = random.choice(list(L.get_ids()))
        l = L.get_by_id(l_id)
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, l_id)
        self.assertIn(l.mode, list(adapter.FORMAT_CHARS.keys()))
        self.assertIn(l.endianness, list(adapter.ENDIANNESS.keys()))
        self.assertIsInstance(l.size, adapter.SFFVolumeStructure)
        self.assertIsInstance(l.start, adapter.SFFVolumeIndex)
        self.assertIsInstance(l.data, _bytes)
        self.assertIsInstance(l.data_array, numpy.ndarray)
        self.assertTrue(len(l.data) > 0)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _L = emdb_sff.latticeListType()
        _no_items = _random_integer(start=2, stop=5)
        _l = list()
        for i in _xrange(_no_items):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_gds_data()
            _l.append(
                emdb_sff.latticeType(
                    id=i,
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        _L.set_lattice(_l)
        L = adapter.SFFLatticeList.from_gds_type(_L)
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[SFFLattice\(.*\]\)"""
        )
        self.assertEqual(len(L), _no_items)
        self.assertEqual(list(L.get_ids()), list(_xrange(_no_items)))
        l_id = random.choice(list(L.get_ids()))
        l = L.get_by_id(l_id)
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, l_id)
        self.assertIn(l.mode, list(adapter.FORMAT_CHARS.keys()))
        self.assertIn(l.endianness, list(adapter.ENDIANNESS.keys()))
        self.assertIsInstance(l.size, adapter.SFFVolumeStructure)
        self.assertIsInstance(l.start, adapter.SFFVolumeIndex)
        self.assertIsInstance(l.data, _bytes)
        self.assertIsInstance(l.data_array, numpy.ndarray)
        self.assertTrue(len(l.data) > 0)


class TestSFFPolygon(Py23FixTestCase):
    """Test the SFFPolygon class"""

    def tearDown(self):
        adapter.SFFPolygon.reset_id()

    def test_default(self):
        """Test default settings"""
        p = adapter.SFFPolygon()
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[\]\)""".format(
                0, None
            )
        )
        self.assertEqual(len(p), 0)
        self.assertEqual(p.id, 0)
        self.assertEqual(p.vertices, list())
        # set in constructor
        _v = [
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
        ]
        p = adapter.SFFPolygon(
            v=_v
        )
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[.*\]\)""".format(1)
        )
        self.assertEqual(p.id, 1)
        self.assertEqual(p.vertices, _v)
        # direct setting
        p = adapter.SFFPolygon()
        _v = [
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
        ]
        p.vertices = _v
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[.*\]\)""".format(2)
        )
        self.assertEqual(p.id, 2)
        self.assertEqual(p.vertices, _v)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _p = emdb_sff.polygonType()
        p = adapter.SFFPolygon.from_gds_type(_p)
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[\]\)""".format(None)
        )
        self.assertEqual(len(p), 0)
        self.assertIsNone(p.id)
        self.assertEqual(p.vertices, list())
        # set in constructor
        _v = [
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
        ]
        _PID = _random_integer()
        _p = emdb_sff.polygonType(
            PID=_PID,
            v=_v
        )
        p = adapter.SFFPolygon.from_gds_type(_p)
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[.*\]\)""".format(_PID)
        )
        self.assertEqual(p.id, _PID)
        self.assertEqual(p.vertices, _v)
        # direct setting
        p = adapter.SFFPolygon()
        _v = [
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
            _random_integer(start=2, stop=20),
        ]
        p.vertices = _v
        self.assertRegex(
            _str(p),
            r"""SFFPolygon\(PID={}, v=\[.*\]\)""".format(0)
        )
        self.assertEqual(p.id, 0)
        self.assertEqual(p.vertices, _v)


class TestSFFPolygonList(Py23FixTestCase):
    """Test the SFFPolygonList class"""

    def tearDown(self):
        adapter.SFFPolygon.reset_id()

    def test_default(self):
        """Test default settings"""
        # empty list
        P = adapter.SFFPolygonList()
        self.assertRegex(
            _str(P),
            r"""SFFPolygonList\(\[\]\)"""
        )
        self.assertEqual(len(P), 0)
        self.assertEqual(list(P.get_ids()), list())
        # populated
        _no_items = _random_integer(start=2, stop=10)
        P = adapter.SFFPolygonList()
        for _ in _xrange(_no_items):
            P.append(adapter.SFFPolygon(v=[
                _random_integer(start=2, stop=20),
                _random_integer(start=2, stop=20),
                _random_integer(start=2, stop=20),
            ])
            )
        self.assertRegex(
            _str(P),
            r"""SFFPolygonList\(\[.*\]\)"""
        )
        self.assertEqual(len(P), _no_items)
        self.assertEqual(list(P.get_ids()), list(_xrange(_no_items)))
        p_id = random.choice(list(P.get_ids()))
        p = P.get_by_id(p_id)
        self.assertIsInstance(p, adapter.SFFPolygon)
        self.assertEqual(p.id, p_id)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        # empty list
        _P = emdb_sff.polygonListType()
        P = adapter.SFFPolygonList.from_gds_type(_P)
        self.assertRegex(
            _str(P),
            r"""SFFPolygonList\(\[\]\)"""
        )
        self.assertEqual(len(P), 0)
        self.assertEqual(list(P.get_ids()), list())
        # populated
        _no_items = _random_integer(start=2, stop=10)
        _P = emdb_sff.polygonListType()
        _P.set_P([
            emdb_sff.polygonType(
                PID=i,
                v=[
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                    _random_integer(start=2, stop=20),
                ]
            ) for i in _xrange(_no_items)]
        )
        P = adapter.SFFPolygonList.from_gds_type(_P)
        self.assertRegex(
            _str(P),
            r"""SFFPolygonList\(\[.*\]\)"""
        )
        self.assertEqual(len(P), _no_items)
        self.assertEqual(list(P.get_ids()), list(_xrange(_no_items)))
        p_id = random.choice(list(P.get_ids()))
        p = P.get_by_id(p_id)
        self.assertIsInstance(p, adapter.SFFPolygon)
        self.assertEqual(p.id, p_id)


class TestSFFSegment(Py23FixTestCase):
    """Test the SFFSegment class"""

    def tearDown(self):
        adapter.SFFSegment.reset_id()

    def test_default(self):
        """Test default settings"""
        s = adapter.SFFSegment()
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=1, parentID=0, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)"""
        )
        # change ID
        _id = _random_integer()
        s = adapter.SFFSegment(id=_id)
        self.assertEqual(s.id, _id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID=0, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id)
        )
        # change parent_id
        _parent_id = _random_integer()
        s = adapter.SFFSegment(parentID=_parent_id)
        self.assertEqual(s.id, _id + 1)  # we have an increment from the previous set value
        self.assertEqual(s.parent_id, _parent_id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 1,
                _parent_id
            )
        )
        # change biological_annotation
        B = adapter.SFFBiologicalAnnotation(
            name=" ".join(rw.random_words(count=3)),
            description=li.get_sentence(),
        )
        s = adapter.SFFSegment(biologicalAnnotation=B)
        self.assertEqual(s.id, _id + 2)  # we have an increment from the previous set value
        self.assertEqual(s.biological_annotation, B)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation={}, colour=None, """
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 2,
                0,
                _str(B).replace(r"(", r"\(").replace(r")", r"\)").replace(r"[", r"\[").replace(r"]", r"\]")
            )
        )
        # change colour
        R = adapter.SFFRGBA(random_colour=True)
        s = adapter.SFFSegment(colour=R)
        self.assertEqual(s.id, _id + 3)  # we have an increment from the previous set value
        self.assertEqual(s.colour, R)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour={}, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 3,
                0,
                _str(R).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # 3D volume
        _l = _random_integer(start=0)
        _v = _random_integer()
        _t = _random_integer(start=0)
        V = adapter.SFFThreeDVolume(
            latticeId=_l,
            value=_v,
            transformId=_t
        )
        s = adapter.SFFSegment(threeDVolume=V)
        self.assertEqual(s.id, _id + 4)
        self.assertEqual(s.volume, V)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume={}, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 4,
                0,
                _str(V).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # meshes
        M = adapter.SFFMeshList()
        s = adapter.SFFSegment(meshList=M)
        self.assertEqual(s.id, _id + 5)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 5,
                0,
            )
        )
        # shapes
        S = adapter.SFFShapePrimitiveList()
        s = adapter.SFFSegment(shapePrimitiveList=S)
        self.assertEqual(s.id, _id + 6)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id + 6,
                0,
            )
        )

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _s = emdb_sff.segmentType()
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)"""
        )
        # change ID
        _id = _random_integer()
        _s = emdb_sff.segmentType(id=_id)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertEqual(s.id, _id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID=\d+, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _id)
        )
        # change parent_id
        _parent_id = _random_integer()
        _s = emdb_sff.segmentType(parentID=_parent_id)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.parent_id, _parent_id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parentID={}, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                None,
                _parent_id
            )
        )
        # change biological_annotation
        _B = emdb_sff.biologicalAnnotationType(
            name=" ".join(rw.random_words(count=3)),
            description=li.get_sentence(),
        )
        _s = emdb_sff.segmentType(biologicalAnnotation=_B)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        B = adapter.SFFBiologicalAnnotation.from_gds_type(_B)
        self.assertEqual(s.biological_annotation, B)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation={}, colour=None, """
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _str(B).replace(r"(", r"\(").replace(r")", r"\)").replace(r"[", r"\[").replace(r"]", r"\]")
            )
        )
        # change colour
        _R = emdb_sff.rgbaType(red=_random_float(), green=_random_float(), blue=_random_float())
        R = adapter.SFFRGBA.from_gds_type(_R)
        _s = emdb_sff.segmentType(colour=_R)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.colour, R)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation=None, colour={}, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _str(R).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # 3D volume
        _l = _random_integer(start=0)
        _v = _random_integer()
        _t = _random_integer(start=0)
        _V = emdb_sff.threeDVolumeType(
            latticeId=_l,
            value=_v,
            transformId=_t
        )
        V = adapter.SFFThreeDVolume.from_gds_type(_V)
        _s = emdb_sff.segmentType(threeDVolume=_V)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.volume, V)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume={}, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)""".format(
                _str(V).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # meshes
        _M = emdb_sff.meshListType()
        M = adapter.SFFMeshList.from_gds_type(_M)
        _s = emdb_sff.segmentType(meshList=_M)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[.*\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[\]\)\)"""
        )
        # shapes
        _S = emdb_sff.shapePrimitiveListType()
        S = adapter.SFFShapePrimitiveList.from_gds_type(_S)
        _s = emdb_sff.segmentType(shapePrimitiveList=_S)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parentID=\d+, biologicalAnnotation=None, colour=None, """ \
            r"""threeDVolume=None, meshList=SFFMeshList\(\[\]\), shapePrimitiveList=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
            )
        )

    def test_as_json(self):
        """Test that we can export as JSON"""
        # empty fails validation
        s = adapter.SFFSegment()
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            s.export(sys.stderr)
        # at least colour needed
        s = adapter.SFFSegment()
        s.colour = adapter.SFFRGBA(random_colour=True)
        s_json = s.as_json()
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parentID'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        # _print(s_json)
        # self.assertTrue(False)
        # with annotation
        s = adapter.SFFSegment(
            biologicalAnnotation=adapter.SFFBiologicalAnnotation(
                name=rw.random_word(),
                description=li.get_sentence(),
            )
        )
        s.colour = adapter.SFFRGBA(random_colour=True)
        s_json = s.as_json()
        # _print(s_json)
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parentID'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        self.assertEqual(s_json[u'biologicalAnnotation'][u'name'], s.biological_annotation.name)
        self.assertEqual(s_json[u'biologicalAnnotation'][u'description'], s.biological_annotation.description)

    def test_from_json(self):
        """Test that we can import from JSON"""
        # minimal
        s_json = {'id': 2, 'parentID': 0, 'colour': (0.3480471169539232, 0.9354618836165659, 0.7017431484633613, 1.0)}
        s = adapter.SFFSegment.from_json(s_json)
        self.assertEqual(s.id, s_json[u'id'])
        self.assertEqual(s.parent_id, s_json[u'parentID'])
        self.assertEqual(s.colour.value, s_json[u'colour'])
        # more
        s_json = {'id': 3, 'parentID': 0, 'biologicalAnnotation': {'name': 'preserver',
                                                                   'description': 'Dictumstvivamus proin purusvestibulum turpis sociis assum.',
                                                                   'numberOfInstances': 1},
                  'colour': (0.3284280279067431, 0.8229825614708411, 0.07590219333941295, 1.0)}
        s = adapter.SFFSegment.from_json(s_json)
        _print(s)
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parentID'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        self.assertEqual(s_json[u'biologicalAnnotation'][u'name'], s.biological_annotation.name)
        self.assertEqual(s_json[u'biologicalAnnotation'][u'description'], s.biological_annotation.description)
        self.assertEqual(s_json[u'biologicalAnnotation'][u'numberOfInstances'],
                         s.biological_annotation.number_of_instances)


class TestSFFSegmentList(Py23FixTestCase):
    """Test the SFFSegmentList class"""

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFSegmentList()
        _no_items = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_items)]
        self.assertRegex(
            _str(S),
            r"""SFFSegmentList\(\[SFFSegment\(.*\)\]\)"""
        )
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # adding a segment without ID does not change the number of IDs (because it has ID=None)
        S.append(adapter.SFFSegment.from_gds_type(
            emdb_sff.segmentType()
        ))
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # exception when trying to overwrite an ID in `_id_dict`
        with self.assertRaisesRegex(KeyError, r".*already present.*"):
            S.append(adapter.SFFSegment.from_gds_type((
                emdb_sff.segmentType(id=1)
            )))

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.segmentListType()
        _no_items = _random_integer(start=2, stop=10)
        _S.set_segment([
            emdb_sff.segmentType(
                id=i,
            ) for i in _xrange(1, _no_items + 1)]
        )
        S = adapter.SFFSegmentList.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSegmentList\(\[SFFSegment\(.*\)\]\)"""
        )
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))


class TestSFFShapePrimitiveList(Py23FixTestCase):
    """Test the SFFShapePrimitiveList class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    @staticmethod
    def get_sff_shapes(counts=_random_integers(count=4, start=2, stop=10)):
        no_cones, no_cuboids, no_cylinders, no_ellipsoids = counts
        cones = [adapter.SFFCone(
            height=_random_float(10),
            bottomRadius=_random_float(10),
        ) for _ in _xrange(no_cones)]
        cuboids = [
            adapter.SFFCuboid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_cuboids)]
        cylinders = [
            adapter.SFFCylinder(
                height=_random_float(10),
                diameter=_random_float(10),
            ) for _ in _xrange(no_cylinders)]
        ellipsoids = [
            adapter.SFFEllipsoid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ]
        return cones, cuboids, cylinders, ellipsoids

    @staticmethod
    def get_gds_shapes(counts=_random_integers(count=4, start=2, stop=10)):
        no_cones, no_cuboids, no_cylinders, no_ellipsoids = counts
        cones = [emdb_sff.cone(
            height=_random_float(10),
            bottomRadius=_random_float(10),
        ) for _ in _xrange(no_cones)]
        cuboids = [
            emdb_sff.cuboid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_cuboids)]
        cylinders = [
            emdb_sff.cylinder(
                height=_random_float(10),
                diameter=_random_float(10),
            ) for _ in _xrange(no_cylinders)]
        ellipsoids = [
            emdb_sff.ellipsoid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ]
        return cones, cuboids, cylinders, ellipsoids

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFShapePrimitiveList()
        cones, cuboids, cylinders, ellipsoids = TestSFFShapePrimitiveList.get_sff_shapes()
        [S.append(c) for c in cones]
        [S.append(c) for c in cuboids]
        [S.append(c) for c in cylinders]
        [S.append(c) for c in ellipsoids]
        self.assertRegex(
            _str(S),
            r"""SFFShapePrimitiveList\(\[.*\]\)"""
        )
        total_shapes = len(cones) + len(cuboids) + len(cylinders) + len(ellipsoids)
        self.assertEqual(len(S), total_shapes)
        self.assertEqual(list(S.get_ids()), list(_xrange(total_shapes)))
        s_id = random.choice(list(_xrange(total_shapes)))
        s = S.get_by_id(s_id)
        self.assertIsInstance(s, (adapter.SFFCone, adapter.SFFCuboid, adapter.SFFCylinder, adapter.SFFEllipsoid))

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.shapePrimitiveListType()
        cones, cuboids, cylinders, ellipsoids = TestSFFShapePrimitiveList.get_gds_shapes()
        [_S.add_shapePrimitive(c) for c in cones]
        [_S.add_shapePrimitive(c) for c in cuboids]
        [_S.add_shapePrimitive(c) for c in cylinders]
        [_S.add_shapePrimitive(c) for c in ellipsoids]
        S = adapter.SFFShapePrimitiveList.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFShapePrimitiveList\(\[.*\]\)"""
        )
        total_shapes = len(cones) + len(cuboids) + len(cylinders) + len(ellipsoids)
        self.assertEqual(len(S), total_shapes)
        self.assertEqual(list(S.get_ids()), list())
        s_id = random.choice(list(_xrange(total_shapes)))
        s = S[s_id]
        self.assertIsInstance(s, (adapter.SFFCone, adapter.SFFCuboid, adapter.SFFCylinder, adapter.SFFEllipsoid))


class TestSFFSoftware(Py23FixTestCase):
    """Test the SFFSoftware class"""

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFSoftware()
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(name={}, version={}, processingDetails={}\)""".format(
                None, None, None
            )
        )
        self.assertIsNone(S.name)
        self.assertIsNone(S.version)
        self.assertIsNone(S.processing_details)
        name = rw.random_word()
        version = rw.random_word()
        processing_details = li.get_sentences(sentences=_random_integer(start=2, stop=5))
        S = adapter.SFFSoftware(
            name=name,
            version=version,
            processingDetails=processing_details
        )
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(name=".+", version=".+", processingDetails=".+"\)"""
        )
        self.assertEqual(S.name, name)
        self.assertEqual(S.version, version)
        self.assertEqual(S.processing_details, processing_details)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.softwareType()
        S = adapter.SFFSoftware.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(name={}, version={}, processingDetails={}\)""".format(
                None, None, None
            )
        )
        self.assertIsNone(S.name)
        self.assertIsNone(S.version)
        self.assertIsNone(S.processing_details)
        name = rw.random_word()
        version = rw.random_word()
        processing_details = li.get_sentences(sentences=_random_integer(start=2, stop=5))
        _S = emdb_sff.softwareType(
            name=name,
            version=version,
            processingDetails=processing_details
        )
        S = adapter.SFFSoftware.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(name=".+", version=".+", processingDetails=".+"\)"""
        )
        self.assertEqual(S.name, name)
        self.assertEqual(S.version, version)
        self.assertEqual(S.processing_details, processing_details)


class TestSFFTransformationMatrix(Py23FixTestCase):
    """Test the SFFTransformationMatrix class"""

    def test_create_init(self):
        """Test creating from __init__"""
        r, c = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10)
        _d = numpy.random.randint(0, 100, size=(r, c))
        d = u" ".join(list(map(_str, _d.flatten().tolist())))
        T = adapter.SFFTransformationMatrix(
            rows=r,
            cols=c,
            data=d
        )
        self.assertEqual(T.rows, r)
        self.assertEqual(T.cols, c)
        self.assertEqual(T.data, d)
        self.assertEqual(T.data_array.flatten().tolist(), _d.flatten().tolist())

    def test_create_classmethod(self):
        """Test default settings"""
        r, c = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10)
        t = numpy.random.rand(r, c)
        d = t.flatten().tolist()
        T = adapter.SFFTransformationMatrix.from_array(t)
        self.assertEqual(T.rows, r)
        self.assertEqual(T.cols, c)
        self.assertEqual(T.data, " ".join(list(map(_str, d))))
        self.assertEqual(T.data_array.flatten().tolist(), d)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        r, c = _random_integer(start=3, stop=10), _random_integer(start=3, stop=10)
        _data = numpy.random.rand(r, c)
        __data = " ".join(map(_str, _data.flatten().tolist()))
        self.assertIsInstance(__data, _str)
        _t = emdb_sff.transformationMatrixType(
            id=0,
            rows=r, cols=c,
            data=__data
        )
        t = adapter.SFFTransformationMatrix.from_gds_type(_t)
        self.assertTrue(hasattr(t, u'data_array'))


class TestSFFVertex(Py23FixTestCase):
    """Test the SFFVertex class"""

    def tearDown(self):
        adapter.SFFVertex.reset_id()

    def test_default(self):
        """Test default settings"""
        v = adapter.SFFVertex()
        self.assertRegex(
            _str(v),
            r"""SFFVertex\(vID=0, designation="surface", x=None, y=None, z=None\)"""
        )
        self.assertEqual(v.id, 0)
        self.assertEqual(v.designation, u"surface")
        self.assertIsNone(v.x)
        self.assertIsNone(v.y)
        self.assertIsNone(v.z)
        self.assertEqual(v.point, (None, None, None))
        # with values
        x = _random_float(10)
        y = _random_float(10)
        z = _random_float(10)
        v = adapter.SFFVertex(designation=u"normal", x=x, y=y, z=z)
        self.assertRegex(
            _str(v),
            r"""SFFVertex\(vID=1, designation="normal", x={}, y={}, z={}\)""".format(
                x, y, z
            )
        )
        self.assertEqual(v.id, 1)
        self.assertEqual(v.designation, u"normal")
        self.assertEqual(v.x, x)
        self.assertEqual(v.y, y)
        self.assertEqual(v.z, z)
        self.assertEqual(v.point, (x, y, z))
        # set point directly
        x = _random_float(10)
        y = _random_float(10)
        z = _random_float(10)
        v.point = x, y, z
        self.assertEqual(v.x, x)
        self.assertEqual(v.y, y)
        self.assertEqual(v.z, z)
        self.assertEqual(v.point, (x, y, z))

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _v = emdb_sff.vertexType()
        v = adapter.SFFVertex.from_gds_type(_v)
        self.assertRegex(
            _str(v),
            r"""SFFVertex\(vID=None, designation="surface", x=None, y=None, z=None\)"""
        )
        self.assertIsNone(v.id)
        self.assertEqual(v.designation, u"surface")
        self.assertIsNone(v.x)
        self.assertIsNone(v.y)
        self.assertIsNone(v.z)
        self.assertEqual(v.point, (None, None, None))
        # with values
        x = _random_float(10)
        y = _random_float(10)
        z = _random_float(10)
        _v = emdb_sff.vertexType(designation=u"normal", x=x, y=y, z=z)
        v = adapter.SFFVertex.from_gds_type(_v)
        self.assertRegex(
            _str(v),
            r"""SFFVertex\(vID=None, designation="normal", x={}, y={}, z={}\)""".format(
                x, y, z
            )
        )
        self.assertIsNone(v.id)
        self.assertEqual(v.designation, u"normal")
        self.assertEqual(v.x, x)
        self.assertEqual(v.y, y)
        self.assertEqual(v.z, z)
        self.assertEqual(v.point, (x, y, z))


class TestSFFVertexList(Py23FixTestCase):
    """Test the SFFVertexList class"""

    def test_default(self):
        """Test default settings"""
        V = adapter.SFFVertexList()
        self.assertRegex(
            _str(V),
            r"""SFFVertexList\(\[.*\]\)"""
        )
        self.assertEqual(len(V), 0)
        self.assertEqual(list(V.get_ids()), list())
        no_items = _random_integer(start=2, stop=10)
        [V.append(
            adapter.SFFVertex(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ) for _ in _xrange(no_items)]
        self.assertEqual(len(V), no_items)
        self.assertEqual(list(V.get_ids()), list(_xrange(no_items)))
        v_id = random.choice(list(_xrange(no_items)))
        v = V.get_by_id(v_id)
        self.assertIsInstance(v, adapter.SFFVertex)
        self.assertEqual(v.id, v_id)
        self.assertIsNotNone(v.x)
        self.assertIsNotNone(v.y)
        self.assertIsNotNone(v.z)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _V = emdb_sff.vertexListType()
        V = adapter.SFFVertexList.from_gds_type(_V)
        self.assertRegex(
            _str(V),
            r"""SFFVertexList\(\[.*\]\)"""
        )
        self.assertEqual(len(V), 0)
        self.assertEqual(list(V.get_ids()), list())
        no_items = _random_integer(start=2, stop=10)
        _V.set_v([
            emdb_sff.vertexType(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_items)])
        V = adapter.SFFVertexList.from_gds_type(_V)
        self.assertEqual(len(V), no_items)
        self.assertEqual(list(V.get_ids()), list())
        v_id = random.choice(list(_xrange(no_items)))
        v = V[v_id]
        self.assertIsInstance(v, adapter.SFFVertex)
        self.assertIsNone(v.id)
        self.assertIsNotNone(v.x)
        self.assertIsNotNone(v.y)
        self.assertIsNotNone(v.z)


if __name__ == u"__main__":
    unittest.main()
