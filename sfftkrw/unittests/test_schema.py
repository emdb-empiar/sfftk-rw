# -*- coding: utf-8 -*-
# test_schema.py
"""
Unit for schema adapter
"""
from __future__ import print_function

import json
import os
import random
import sys
import tempfile
import unittest

import h5py
import numpy
from random_words import RandomWords, LoremIpsum

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase, _random_float, _random_integers
from .. import schema
from ..core import _xrange, _dict, _str

rw = RandomWords()
li = LoremIpsum()

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-02-20"


# todo: add ID within each test method

class TestSFFSegmentation(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        # empty segmentation object
        segmentation = schema.SFFSegmentation()  # 3D volume
        segmentation.primary_descriptor = "threeDVolume"
        # transforms
        transforms = schema.SFFTransformList()
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = schema.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = schema.SFFLatticeList()
        # lattice 1
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)])
        lattice = schema.SFFLattice(
            mode='uint32',
            endianness='little',
            size=schema.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=schema.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.add_lattice(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)])
        lattice2 = schema.SFFLattice(
            mode='float32',
            endianness='big',
            size=schema.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=schema.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.add_lattice(lattice2)
        # segments
        segments = schema.SFFSegmentList()
        # segment one
        segment = schema.SFFSegment()
        vol1_value = 1
        segment.volume = schema.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segment.colour = schema.SFFRGBA(
            red=random.random(),
            green=random.random(),
            blue=random.random(),
            alpha=random.random()
        )
        segments.add_segment(segment)
        # segment two
        segment = schema.SFFSegment()
        vol2_value = 37.1
        segment.volume = schema.SFFThreeDVolume(
            latticeId=1,
            value=vol2_value
        )
        segment.colour = schema.SFFRGBA(
            red=random.random(),
            green=random.random(),
            blue=random.random(),
            alpha=random.random()
        )
        # add segment to segments
        segments.add_segment(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        cls.segmentation = segmentation

    def test_create_3D(self):
        """Create an SFFSegmentation object with 3D volume segmentation from scratch"""
        segmentation = schema.SFFSegmentation()  # 3D volume
        segmentation.primary_descriptor = "threeDVolume"
        # transforms
        transforms = schema.SFFTransformList()
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            schema.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = schema.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = schema.SFFLatticeList()
        # lattice 1
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)])
        lattice = schema.SFFLattice(
            mode='uint32',
            endianness='little',
            size=schema.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=schema.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.add_lattice(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)])
        lattice2 = schema.SFFLattice(
            mode='float32',
            endianness='big',
            size=schema.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=schema.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.add_lattice(lattice2)
        # segments
        segments = schema.SFFSegmentList()
        # segment one
        segment = schema.SFFSegment()
        vol1_value = 1
        segment.volume = schema.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segments.add_segment(segment)
        # segment two
        segment = schema.SFFSegment()
        vol2_value = 37.1
        segment.volume = schema.SFFThreeDVolume(
            latticeId=1,
            value=vol2_value
        )
        # add segment to segments
        segments.add_segment(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test_3d_segmentation.sff'))
        # assertions
        self.assertEqual(segmentation.primary_descriptor, "threeDVolume")
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
        self.assertEqual(lattice1.mode, 'uint32')
        self.assertEqual(lattice1.endianness, 'little')
        self.assertCountEqual(lattice1.size.value, (20, 20, 20))
        self.assertCountEqual(lattice1.start.value, (0, 0, 0))
        # lattice two
        self.assertEqual(lattice2.mode, 'float32')
        self.assertEqual(lattice2.endianness, 'big')
        self.assertCountEqual(lattice2.size.value, (30, 40, 50))
        self.assertCountEqual(lattice2.start.value, (-50, -40, 100))

    def test_create_shapes(self):
        """Test that we can create a segmentation of shapes programmatically"""
        segmentation = schema.SFFSegmentation()
        segmentation.primary_descriptor = "shapePrimitiveList"
        transforms = schema.SFFTransformList()
        segments = schema.SFFSegmentList()
        segment = schema.SFFSegment()
        # shapes
        shapes = schema.SFFShapePrimitiveList()
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCylinder(
                height=_random_float() * 100,
                diameter=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        segment.shapes = shapes
        segments.add_segment(segment)
        # more shapes
        segment = schema.SFFSegment()
        # shapes
        shapes = schema.SFFShapePrimitiveList()
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCylinder(
                height=_random_float() * 100,
                diameter=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = schema.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            schema.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        segment.shapes = shapes
        segments.add_segment(segment)
        segmentation.segments = segments
        segmentation.transforms = transforms
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test_shape_segmentation.sff'))
        # assertions
        self.assertEqual(len(segment.shapes), 9)
        self.assertEqual(segment.shapes.num_cones, 4)
        self.assertEqual(segment.shapes.num_cylinders, 1)
        self.assertEqual(segment.shapes.num_cuboids, 2)
        self.assertEqual(segment.shapes.num_ellipsoids, 2)

    def test_create_meshes(self):
        """Test that we can create a segmentation of meshes programmatically"""
        segmentation = schema.SFFSegmentation()
        segmentation.primary_descriptor = "meshList"
        segments = schema.SFFSegmentList()
        segment = schema.SFFSegment()
        # meshes
        meshes = schema.SFFMeshList()
        # mesh 1
        mesh = schema.SFFMesh()
        # mesh 2
        mesh2 = schema.SFFMesh()
        vertices1 = schema.SFFVertexList()
        no_vertices1 = _random_integer(stop=100)
        for i in _xrange(no_vertices1):
            vertex = schema.SFFVertex()
            vertex.point = tuple(
                map(float, (
                    _random_integer(1, 1000),
                    _random_integer(1, 1000),
                    _random_integer(1, 1000)
                ))
            )
            vertices1.add_vertex(vertex)
        polygons1 = schema.SFFPolygonList()
        no_polygons1 = _random_integer(stop=100)
        for i in _xrange(no_polygons1):
            polygon = schema.SFFPolygon()
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygons1.add_polygon(polygon)
        mesh.vertices = vertices1
        mesh.polygons = polygons1
        vertices2 = schema.SFFVertexList()
        no_vertices2 = _random_integer(stop=100)
        for i in _xrange(no_vertices2):
            vertex = schema.SFFVertex()
            vertex.point = tuple(map(float, (
                _random_integer(1, 1000), _random_integer(1, 1000), _random_integer(1, 1000))))
            vertices2.add_vertex(vertex)
        polygons2 = schema.SFFPolygonList()
        no_polygons2 = _random_integer(stop=100)
        for i in _xrange(no_polygons2):
            polygon = schema.SFFPolygon()
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygons2.add_polygon(polygon)
        mesh2.vertices = vertices2
        mesh2.polygons = polygons2
        meshes.add_mesh(mesh)
        meshes.add_mesh(mesh2)
        segment.meshes = meshes
        segments.add_segment(segment)
        # segment two
        segment = schema.SFFSegment()
        # mesh
        meshes = schema.SFFMeshList()
        mesh = schema.SFFMesh()
        vertices3 = schema.SFFVertexList()
        no_vertices3 = _random_integer(stop=100)
        for i in _xrange(no_vertices3):
            vertex = schema.SFFVertex()
            vertex.point = tuple(
                map(float, (
                    _random_integer(1, 1000),
                    _random_integer(1, 1000),
                    _random_integer(1, 1000)
                ))
            )
            vertices3.add_vertex(vertex)
        polygons3 = schema.SFFPolygonList()
        no_polygons3 = _random_integer(stop=100)
        for i in _xrange(no_polygons3):
            polygon = schema.SFFPolygon()
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygons3.add_polygon(polygon)
        mesh.vertices = vertices3
        mesh.polygons = polygons3
        meshes.add_mesh(mesh)
        segment.meshes = meshes
        segments.add_segment(segment)
        segmentation.segments = segments
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test_mesh_segmentation.sff'))
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
        segmentation = schema.SFFSegmentation()  # annotation
        segmentation.name = "name"
        segmentation.software = schema.SFFSoftware(
            name="Software",
            version="1.0.9",
            processingDetails="Processing details"
        )
        segmentation.details = "Details"
        # global external references
        segmentation.global_external_references = schema.SFFGlobalExternalReferences()
        segmentation.global_external_references.add_external_reference(
            schema.SFFExternalReference(
                type='one',
                otherType='two',
                value='three'
            )
        )
        segmentation.global_external_references.add_external_reference(
            schema.SFFExternalReference(
                type='four',
                otherType='five',
                value='six'
            )
        )
        segmentation.segments = schema.SFFSegmentList()
        segment = schema.SFFSegment()
        biol_ann = schema.SFFBiologicalAnnotation()
        biol_ann.name = "Segment1"
        biol_ann.description = "Some description"
        # external refs
        biol_ann.external_references = schema.SFFExternalReferences()
        biol_ann.external_references.add_external_reference(
            schema.SFFExternalReference(
                type="sldjflj",
                value="doieaik"
            )
        )
        biol_ann.external_references.add_external_reference(
            schema.SFFExternalReference(
                type="sljd;f",
                value="20ijalf"
            )
        )
        biol_ann.external_references.add_external_reference(
            schema.SFFExternalReference(
                type="lsdjlsd",
                otherType="lsjfd;sd",
                value="23ijlsdjf"
            )
        )
        biol_ann.number_of_instances = 30
        segment.biological_annotation = biol_ann
        # complexes and macromolecules
        # complexes
        comp_mac = schema.SFFComplexesAndMacromolecules()
        comp = schema.SFFComplexes()
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        # macromolecules
        macr = schema.SFFMacromolecules()
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        macr.add_macromolecule(str(_random_integer(1, 1000)))
        comp_mac.complexes = comp
        comp_mac.macromolecules = macr
        segment.complexes_and_macromolecules = comp_mac
        # colour
        segment.colour = schema.SFFRGBA(
            red=1,
            green=0,
            blue=1,
            alpha=0
        )
        segmentation.segments.add_segment(segment)
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test_annotated_segmentation.sff'))
        # assertions
        self.assertEqual(segmentation.name, 'name')
        self.assertEqual(segmentation.version, segmentation._local.schemaVersion)  # automatically set
        self.assertEqual(segmentation.software.name, "Software")
        self.assertEqual(segmentation.software.version, "1.0.9")
        self.assertEqual(segmentation.software.processing_details, "Processing details")
        self.assertEqual(segmentation.details, "Details")
        # global external references
        self.assertEqual(segmentation.global_external_references[0].type, 'one')
        self.assertEqual(segmentation.global_external_references[0].other_type, 'two')
        self.assertEqual(segmentation.global_external_references[0].value, 'three')
        self.assertEqual(segmentation.global_external_references[1].type, 'four')
        self.assertEqual(segmentation.global_external_references[1].other_type, 'five')
        self.assertEqual(segmentation.global_external_references[1].value, 'six')
        # segment: biological_annotation
        self.assertEqual(segment.biological_annotation.name, "Segment1")
        self.assertEqual(segment.biological_annotation.description, "Some description")
        self.assertEqual(len(segment.biological_annotation.external_references), 3)
        self.assertEqual(segment.biological_annotation.external_references[0].type, "sldjflj")
        self.assertEqual(segment.biological_annotation.external_references[0].value, "doieaik")
        self.assertEqual(segment.biological_annotation.external_references[1].type, "sljd;f")
        self.assertEqual(segment.biological_annotation.external_references[1].value, "20ijalf")
        self.assertEqual(segment.biological_annotation.external_references[2].type, "lsdjlsd")
        self.assertEqual(segment.biological_annotation.external_references[2].other_type, "lsjfd;sd")
        self.assertEqual(segment.biological_annotation.external_references[2].value, "23ijlsdjf")
        self.assertEqual(segment.biological_annotation.number_of_instances, 30)
        # segment: complexes_and_macromolecules
        # complexes
        self.assertEqual(len(segment.complexes_and_macromolecules.complexes), 5)
        complexes_bool = map(lambda c: isinstance(c, str), segment.complexes_and_macromolecules.complexes)
        self.assertTrue(all(complexes_bool))
        # macromolecules
        self.assertEqual(len(segment.complexes_and_macromolecules.macromolecules), 6)
        macromolecules_bool = map(lambda c: isinstance(c, str), segment.complexes_and_macromolecules.macromolecules)
        self.assertTrue(all(macromolecules_bool))
        # colour
        self.assertEqual(segment.colour.value, (1, 0, 1, 0))

    def test_segment_ids(self):
        """to ensure IDs are correctly reset"""
        # segmentation one
        segmentation = schema.SFFSegmentation()
        segmentation.segments = schema.SFFSegmentList()
        segment = schema.SFFSegment()
        segmentation.segments.add_segment(segment)
        # segmentation two
        segmentation2 = schema.SFFSegmentation()
        segmentation2.segments = schema.SFFSegmentList()
        segmentation2.segments.add_segment(schema.SFFSegment())
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
        transforms = schema.SFFTransformList()
        matrix = schema.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms.add_transform(matrix)

        transforms2 = schema.SFFTransformList()
        matrix2 = schema.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms2.add_transform(matrix2)

        self.assertIsNotNone(transforms[0].id)
        self.assertEqual(transforms[0].id, transforms2[0].id)

    def test_read_sff(self):
        """Read from XML (.sff) file"""
        sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        segmentation = schema.SFFSegmentation.from_file(sff_file)
        transform = segmentation.transforms[1]
        # assertions
        self.assertEqual(segmentation.name, "Segger Segmentation")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, "segger")
        self.assertEqual(segmentation.software.version, "2")
        self.assertEqual(segmentation.software.processing_details, None)
        self.assertEqual(segmentation.primary_descriptor, "threeDVolume")
        self.assertEqual(transform.rows, 3)
        self.assertEqual(transform.cols, 4)
        self.assertEqual(transform.data,
                         "3.3900001049 0.0 0.0 -430.529998779 0.0 3.3900001049 0.0 -430.529998779 0.0 0.0 3.3900001049 -430.529998779")

    def test_read_hff(self):
        """Read from HDF5 (.hff) file"""
        hff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')
        segmentation = schema.SFFSegmentation(hff_file)
        # assertions
        self.assertEqual(segmentation.name, "Segger Segmentation")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, "segger")
        self.assertEqual(segmentation.software.version, "2")
        self.assertEqual(segmentation.software.processing_details, None)
        self.assertEqual(segmentation.primary_descriptor, "threeDVolume")

    def test_read_json(self):
        """Read from JSON (.json) file"""
        json_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.json')
        segmentation = schema.SFFSegmentation(json_file)
        # assertions
        self.assertEqual(segmentation.name, "Segger Segmentation")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.software.name, "segger")
        self.assertEqual(segmentation.software.version, "2")
        self.assertEqual(segmentation.software.processing_details, None)
        self.assertEqual(segmentation.primary_descriptor, "threeDVolume")

    def test_export_sff(self):
        """Export to an XML (.sff) file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + '.sff')
        # assertions
        with open(temp_file.name + '.sff') as f:
            self.assertEqual(f.readline(), '<?xml version="1.0" encoding="UTF-8"?>\n')

    def test_export_hff(self):
        """Export to an HDF5 file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + '.hff')
        # assertions
        with open(temp_file.name + '.hff', 'rb') as f:
            find = f.readline().find(b'HDF')
            self.assertGreaterEqual(find, 0)

    def test_export_json(self):
        """Export to a JSON file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + '.json')
        # assertions
        with open(temp_file.name + '.json') as f:
            J = json.load(f)
            self.assertEqual(J['primaryDescriptor'], u"threeDVolume")


class TestSFFRGBA(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_hdf5_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test.hdf5')

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
        colour = schema.SFFRGBA()
        colour.red = self.red
        colour.green = self.green
        colour.blue = self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, 1.0)

    def test_kwarg_colour(self):
        """Test colour using kwargs"""
        colour = schema.SFFRGBA(
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
        colour = schema.SFFRGBA(
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
        colour = schema.SFFRGBA()
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
        colour = schema.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, 'w') as h:
            group = h.create_group("container")
            group = colour.as_hff(group)
            self.assertIn("colour", group)
            self.assertCountEqual(group['colour'][()], colour.value)

    def test_from_hff(self):
        """Test create from HDF5 group"""
        colour = schema.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, 'w') as h:
            group = h.create_group("container")
            group = colour.as_hff(group)
            self.assertIn("colour", group)
            self.assertCountEqual(group['colour'][()], colour.value)
            colour2 = schema.SFFRGBA.from_hff(h['container'])
            self.assertCountEqual(colour.value, colour2.value)

    def test_native_random_colour(self):
        """Test that using a kwarg random_colour will set random colours"""
        colour = schema.SFFRGBA(random_colour=True)
        self.assertTrue(0 <= colour.red <= 1)
        self.assertTrue(0 <= colour.green <= 1)
        self.assertTrue(0 <= colour.blue <= 1)
        self.assertTrue(0 <= colour.alpha <= 1)


class TestSFFComplexes(Py23FixTestCase):
    """Tests for SFFComplexes class"""

    def test_default(self):
        """Test default settings"""
        c = schema.SFFComplexes()
        self.assertEqual(c.gds_type, schema.emdb_sff.complexType)
        self.assertEqual(c.ref, "Complexes")
        self.assertEqual(str(c), "Complex list of length 0")
        with self.assertRaises(StopIteration):  # because it's empty
            next(iter(c))

    def test_set_complexes(self):
        """Test that we can set complexes"""

    # test_set_complexes
    # test_add_complexe
    # test_insert_complex_at
    # test_replace_complex_at
    # test_delete_complex_at


# class TestSFFMacromolecules(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFComplexesAndMacromolecules(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFExternalReference(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFExternalReferences(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFBiologicalAnnotation(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFThreeDVolume(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFVolume(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
class TestSFFVolumeStructure(Py23FixTestCase):
    def test_default(self):
        """Test default settings"""
        vs = schema.SFFVolumeStructure(cols=10, rows=20, sections=30)
        self.assertRegex(_str(vs), r"SFFVolumeStructure\(cols.*rows.*sections.*\)")
        self.assertEqual(vs.cols, 10)
        self.assertEqual(vs.rows, 20)
        self.assertEqual(vs.sections, 30)
        self.assertEqual(vs.voxel_count, 10 * 20 * 30)

#
# class TestSFFVolumeIndex(Py23FixTestCase):
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)


class TestSFFLattice(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.lattice_size = schema.SFFVolumeStructure(
            cols=10, rows=10, sections=10,
        )
        cls.lattice_endianness = 'little'
        cls.lattice_mode = 'uint32'
        cls.lattice_start = schema.SFFVolumeIndex(cols=0, rows=0, sections=0)
        data_ = numpy.array(range(1000), dtype=numpy.uint32).reshape((10, 10, 10))  # data
        numpy.random.shuffle(data_)  # shuffle in place
        cls.lattice_data = data_
        lattices = schema.SFFLatticeList()  # to reset lattice_id
        cls.lattice = schema.SFFLattice(
            mode=cls.lattice_mode,
            endianness=cls.lattice_endianness,
            size=cls.lattice_size,
            start=cls.lattice_start,
            data=cls.lattice_data
        )

    def test_create(self):
        """Test creation of a lattice object"""
        self.assertEqual(self.lattice.ref, "3D lattice")
        self.assertEqual(
            _str(self.lattice),
            "SFFLattice(mode={}, endianness={}, size={}, start={}, data=<numpy.ndarray>)".format(
                self.lattice_mode,
                self.lattice_endianness,
                self.lattice_size,
                self.lattice_start,
            )
        )
        self.assertEqual(self.lattice.id, 0)
        self.assertEqual(self.lattice.mode, self.lattice_mode)
        self.assertEqual(self.lattice.endianness, self.lattice_endianness)
        self.assertCountEqual(self.lattice.size.value, self.lattice_data.shape)
        self.assertCountEqual(self.lattice.start.value, self.lattice_start.value)
        self.assertTrue(self.lattice.is_encoded)

    def test_decode(self):
        """Test that we can decode a lattice"""
        self.lattice.decode()
        self.assertCountEqual(self.lattice.data.flatten(), self.lattice_data.flatten())
        self.assertFalse(self.lattice.is_encoded)


class TestSFFTypeError(Py23FixTestCase):
    """Tests for the exception"""

    def test_default(self):
        """Test default operation"""
        c = schema.SFFComplexes()
        with self.assertRaisesRegex(schema.SFFTypeError, r".*?list.*?"):
            c.set_complexes('complexes')

    def test_message(self):
        """Test error raised with message"""
        v = schema.SFFVolumeStructure()
        with self.assertRaisesRegex(schema.SFFTypeError, r"should be of length 3"):
            v.value = (1, 2)


class TestSFFType(Py23FixTestCase):
    """Tests for the main base class"""

    def test_gds_type_missing(self):
        """Test for presence of `gds_type` attribute"""

        class _SomeEntity(schema.SFFType):
            """Empty entity"""

        with self.assertRaisesRegex(ValueError, r'.*gds_type.*'):
            _s = _SomeEntity()

    def test_create_from_gds_type(self):
        """Test creating an `SFFType` subclass object from a `gds_type' object"""
        # we will try with SFFRGBA and rgbaType
        red = _random_float()
        green = _random_float()
        blue = _random_float()
        _r = schema.emdb_sff.rgbaType(
            red=red, green=green, blue=blue,
        )
        r = schema.SFFRGBA.from_gds_type(_r)
        self.assertIsInstance(r, schema.SFFRGBA)
        self.assertEqual(r.red, red)
        self.assertEqual(r.green, green)
        self.assertEqual(r.blue, blue)

    def test_create_from_gds_type_raises_error(self):
        """Test that we get an exception when the `SFFType` subclass object's `gds_type` attribute is not the same
        as the one provided"""
        _r = schema.emdb_sff.biologicalAnnotationType()
        with self.assertRaisesRegex(schema.SFFTypeError, r".*is not of type.*"):
            r = schema.SFFRGBA.from_gds_type(_r)

    def test_ref_attr(self):
        """Test the `ref` attribute"""
        c = schema.SFFRGBA(
            red=1, green=1, blue=0, alpha=0.5
        )
        r = repr(c)
        self.assertRegex(r, r"\(.*\d+,.*\)")

    def test_repr_string_repr_args(self):
        """Test the string representation using `repr_string` and `repr_args`"""
        # correct rendering for colour: prints out repr_string filled with repr_args
        c = schema.SFFRGBA(random_colour=True)
        self.assertRegex(str(c), r"\(\d\.\d+,.*\)")
        # correct assessment of length: prints out a string with the correct len() value
        c = schema.SFFComplexes()
        c.set_complexes(rw.random_words(count=10))
        self.assertRegex(str(c), ".*10.*")
        # plain string: prints the plain string
        v = schema.SFFThreeDVolume()
        self.assertEqual(str(v), "3D formatted segment")

        # repr_str is missing: prints out the output of type
        class _RGBA(schema.SFFRGBA):
            repr_string = ""

        _c = _RGBA(random_colour=True)
        self.assertRegex(str(_c), r".class.*_RGBA.*")

        # unmatched repr_args (it should be a tuple of four values)
        class _RGBA(schema.SFFRGBA):
            repr_args = ('red', 'green')

        _c = _RGBA(random_colour=True)
        with self.assertRaisesRegex(ValueError, r'Unmatched number.*'):
            str(_c)

    def test_ids(self):
        """Test that IDs work correctly

        - When a blank object is created, ID should start from 0/1
        - When ID is specified as a kwarg then the ID counter should be set to that value so the next will increment from there
        - When an object is instantiated using the `from_gds_type` classmethod then we should set the ID counter to the value of the gds_type ID
        - Where a object container exists e.g. `SFFSegmentList` for `SFFSegment` then every new instantiation of the container resets the ID
        - That we can manually reset IDs
        -
        """

        self.assertTrue(False)

    def test_iter_attr(self):
        """Test use of `iter_attr`"""
        # first we should be able to get items from the objects using next(iter(...))
        c = schema.SFFComplexes()
        words = rw.random_words(count=3)
        c.set_complexes(words)
        self.assertEqual(next(iter(c)), words[0])
        # next, let's see this fail for a non-iterable class
        c = schema.SFFRGBA(random_colour=True)
        with self.assertRaisesRegex(TypeError, r".*object is not iterable"):
            iter(c)
        # iter_attr is useful for evaluating length
        c = schema.SFFComplexes()
        _len = _random_integer(start=2)
        c.set_complexes(rw.random_words(count=_len))
        self.assertEqual(len(c), _len)
        # some classes have no length
        c = schema.SFFRGBA(random_colour=True)
        with self.assertRaisesRegex(TypeError, r"object of type.*has no len\(\)"):
            len(c)
        # iter_attr also allows us to delete
        c = schema.SFFComplexes()
        c.add_complex(rw.random_word())
        self.assertEqual(len(c), 1)
        del c[0]
        self.assertEqual(len(c), 0)

    def test_iter_attr_ids(self):
        """Test that iter_attrs have correct IDs"""
        S = schema.SFFSegmentList()
        ss = [schema.SFFSegment(
            biologicalAnnotation=schema.SFFBiologicalAnnotation(
                name=rw.random_word(),
                description=li.get_sentence(),
            ),
            colour=schema.SFFRGBA(random_colour=True),
        ) for _ in _xrange(10)]
        [S.add_segment(s) for s in ss]
        print(S, file=sys.stderr)
        print(list(map(lambda s: s.id, ss)), file=sys.stderr)
        for s in S:
            print(s, file=sys.stderr)
        sy = schema.SFFSegment()
        print('sy.id:', sy.id, file=sys.stderr)
        self.assertEqual(sy.id, 11)

    def test_iter_dict(self):
        """Test the convenience dict for quick access to items by ID"""
        S = schema.SFFSegmentList()
        ids = _random_integers(count=10)
        segment_dict = _dict()
        for i in ids:
            s = schema.SFFSegment(id=i)
            S.add_segment(s)
            segment_dict[i] = s
        # print('segment_dict:', id(list(_dict_iter_values(segment_dict))[0]), file=sys.stderr)
        # print('S.iter_dict:', id(list(_dict_iter_values(S.iter_dict))[0]), file=sys.stderr)
        #
        # print(dir(s), file=sys.stderr)
        # for attr in dir(s):
        #     print(attr, getattr(s, attr), type(getattr(s, attr)), file=sys.stderr)
        #     if isinstance(attr, schema.SFFAttribute):
        #         print(getattr(s, attr), file=sys.stderr)
        self.assertDictEqual(segment_dict, S.iter_dict)

        # add complex
        # word = rw.random_word()
        # c.add_complex(word)
        # p[word] = word
        # self.assertDictEqual(p, c.iter_dict)


#     def test_get_ids(self):
#         """Test that get_ids() returns a list of IDs"""
#         self.assertTrue(False)
#
#     def test_get_by_id(self):
#         """Test that we can get by ID"""
#         self.assertTrue(False)
#


class TestSFFIndexType(Py23FixTestCase):
    """Test the indexing mixin class `SFFIndexType"""

    def setUp(self):
        """Reset ids"""
        schema.SFFSegment.segment_id = 1 # we test resetting formerly

    def test_new_obj_True(self):
        """Test that an empty `SFFIndexType` subclass has correct indexes"""
        s = schema.SFFSegment()
        self.assertEqual(s.id, 1)
        s = schema.SFFSegment(new_obj=True) # verbose: `new_obj=True` by default
        self.assertEqual(s.id, 2)

    def test_new_obj_False(self):
        """Test that `new_obj=False` for empty `SFFIndexType` subclass has None for ID"""
        s = schema.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)

    def test_proper_incrementing(self):
        """Test that proper incrementing with and without `new_obj=False/True`"""
        s = schema.SFFSegment()
        self.assertEqual(s.id, 1)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 2)
        s = schema.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 3)
        s = schema.SFFSegment(new_obj=True)
        self.assertEqual(s.id, 4)
        s = schema.SFFSegment(new_obj=False)
        self.assertIsNone(s.id)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 5)
        s = schema.SFFSegment.from_gds_type(schema.emdb_sff.segmentType(id=35))
        self.assertEqual(s.id, 35)
        s = schema.SFFSegment.from_gds_type(schema.emdb_sff.segmentType())
        self.assertIsNone(s.id)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 6)

    def test_with_gds_type(self):
        """Test that we can work with generateDS types"""
        s = schema.SFFSegment.from_gds_type(schema.emdb_sff.segmentType())
        self.assertIsNone(s.id)
        s = schema.SFFSegment.from_gds_type(schema.emdb_sff.segmentType(id=37))
        self.assertIsNotNone(s.id)

    def test_reset_id(self):
        """Test that we can reset the ID"""
        s = schema.SFFSegment()
        self.assertEqual(s.id, 1)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 2)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 3)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 4)
        schema.SFFSegment.reset_id()
        s = schema.SFFSegment()
        self.assertEqual(s.id, 1)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 2)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 3)
        s = schema.SFFSegment()
        self.assertEqual(s.id, 4)

    def test_errors(self):
        """Test that we get the right exceptions"""
        class _Segment(schema.SFFSegment):
            index_attr = ''

        with self.assertRaisesRegex(schema.SFFTypeError, r".*subclasses must provide an index attribute"):
            _Segment()

        class _Segment(schema.SFFSegment):
            index_attr = 'segment_index'

        with self.assertRaisesRegex(AttributeError, r".*is missing a class variable.*"):
            _Segment()

        class _Segment(schema.SFFSegment):
            segment_id = 3.8

        with self.assertRaises(schema.SFFTypeError):
            _Segment()


#
# class TestSFFAttribute(Py23FixTestCase):
#     """Test the main attribute class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
# class TestSFFMesh(Py23FixTestCase):
#     """Test the SFFMesh class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFMeshList(Py23FixTestCase):
#     """Test the SFFMeshList class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFBoundingBox(Py23FixTestCase):
#     """Test the SFFBoundingBox class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFCone(Py23FixTestCase):
#     """Test the SFFCone class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFCuboid(Py23FixTestCase):
#     """Test the SFFCuboid class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFCylinder(Py23FixTestCase):
#     """Test the SFFCylinder class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFEllipsoid(Py23FixTestCase):
#     """Test the SFFEllipsoid class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFGlobalExternalReferences(Py23FixTestCase):
#     """Test the SFFGlobalExternalReferences class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFLatticeList(Py23FixTestCase):
#     """Test the SFFLatticeList class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFPolygon(Py23FixTestCase):
#     """Test the SFFPolygon class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFPolygonList(Py23FixTestCase):
#     """Test the SFFPolygonList class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFSegment(Py23FixTestCase):
#     """Test the SFFSegment class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
class TestSFFSegmentList(Py23FixTestCase):
    """Test the SFFSegmentList class"""

    def test_default(self):
        """Test default settings"""
        S = schema.SFFSegmentList()
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        for s in S:
            print(s.id, file=sys.stderr)
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        S.add_segment(schema.SFFSegment())
        for s in S:
            print(s, file=sys.stderr)
        S.add_segment(schema.SFFSegment.from_gds_type(
            schema.emdb_sff.segmentType()
        ))
        for s in S:
            print(s, file=sys.stderr)
        # self.assertTrue(False)

#
# class TestSFFShape(Py23FixTestCase):
#     """Test the SFFShape class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFShapePrimitiveList(Py23FixTestCase):
#     """Test the SFFShapePrimitiveList class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFSoftware(Py23FixTestCase):
#     """Test the SFFSoftware class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFTransformationMatrix(Py23FixTestCase):
#     """Test the SFFTransformationMatrix class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFVertex(Py23FixTestCase):
#     """Test the SFFVertex class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)
#
#
# class TestSFFVertexList(Py23FixTestCase):
#     """Test the SFFVertexList class"""
#
#     def test_default(self):
#         """Test default settings"""
#         self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
