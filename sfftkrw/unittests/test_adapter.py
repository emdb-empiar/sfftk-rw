# -*- coding: utf-8 -*-
# test_adapter.py
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

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase, _random_float
from ..core import _xrange, _str
from ..schema import adapter

rw = RandomWords()
li = LoremIpsum()

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-02-20"


# todo: add ID within each test method
# todo: the individual class tests should include the repr_string check
class TestSFFSegmentation(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        # empty segmentation object
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.primary_descriptor = "threeDVolume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
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
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)])
        lattice = adapter.SFFLattice(
            mode='uint32',
            endianness='little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.add_lattice(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)])
        lattice2 = adapter.SFFLattice(
            mode='float32',
            endianness='big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.add_lattice(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment()
        vol1_value = 1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segment.colour = adapter.SFFRGBA(
            red=random.random(),
            green=random.random(),
            blue=random.random(),
            alpha=random.random()
        )
        segments.add_segment(segment)
        # segment two
        segment = adapter.SFFSegment()
        vol2_value = 37.1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=1,
            value=vol2_value
        )
        segment.colour = adapter.SFFRGBA(
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
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.primary_descriptor = "threeDVolume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.add_transform(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
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
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)])
        lattice = adapter.SFFLattice(
            mode='uint32',
            endianness='little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.add_lattice(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)])
        lattice2 = adapter.SFFLattice(
            mode='float32',
            endianness='big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.add_lattice(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment()
        vol1_value = 1
        segment.volume = adapter.SFFThreeDVolume(
            latticeId=0,
            value=vol1_value,
        )
        segments.add_segment(segment)
        # segment two
        segment = adapter.SFFSegment()
        vol2_value = 37.1
        segment.volume = adapter.SFFThreeDVolume(
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
        segmentation = adapter.SFFSegmentation()
        segmentation.primary_descriptor = "shapePrimitiveList"
        transforms = adapter.SFFTransformList()
        segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.add_shape(cylinder)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        ellipsoid = adapter.SFFEllipsoid(
            x=_random_float() * 100,
            y=_random_float() * 100,
            z=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.add_shape(ellipsoid)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        shapes.add_shape(ellipsoid2)
        print('cylinder.id', cylinder.id, file=sys.stderr)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        print('cylinder.id', cylinder.id, file=sys.stderr)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        print('cylinder.id', cylinder.id, file=sys.stderr)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        print('cylinder.id', cylinder.id, file=sys.stderr)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        print('cylinder.id', cylinder.id, file=sys.stderr)
        print('ellipsoid.id', ellipsoid.id, file=sys.stderr)
        print('ellipsoid2.id', ellipsoid2.id, file=sys.stderr)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        print('ellipsoid2.id', ellipsoid2.id, file=sys.stderr)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        print('ellipsoid2.id', ellipsoid2.id, file=sys.stderr)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        print('ellipsoid2.id', ellipsoid2.id, file=sys.stderr)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        print('ellipsoid2.id', ellipsoid2.id, file=sys.stderr)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        segment.shapes = shapes
        segments.add_segment(segment)
        # more shapes
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCylinder(
                height=_random_float() * 100,
                diameter=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
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
            data=" ".join(map(str, range(12))),
        )
        transforms.add_transform(transform)
        shapes.add_shape(
            adapter.SFFCone(
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
        segmentation = adapter.SFFSegmentation()
        segmentation.primary_descriptor = "meshList"
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
            vertices1.add_vertex(vertex)
        polygons1 = adapter.SFFPolygonList()
        no_polygons1 = _random_integer(stop=100)
        for i in _xrange(no_polygons1):
            polygon = adapter.SFFPolygon()
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygons1.add_polygon(polygon)
        mesh.vertices = vertices1
        mesh.polygons = polygons1
        vertices2 = adapter.SFFVertexList()
        no_vertices2 = _random_integer(stop=100)
        for i in _xrange(no_vertices2):
            vertex = adapter.SFFVertex()
            vertex.point = tuple(map(float, (
                _random_integer(1, 1000), _random_integer(1, 1000), _random_integer(1, 1000))))
            vertices2.add_vertex(vertex)
        polygons2 = adapter.SFFPolygonList()
        no_polygons2 = _random_integer(stop=100)
        for i in _xrange(no_polygons2):
            polygon = adapter.SFFPolygon()
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
            vertices3.add_vertex(vertex)
        polygons3 = adapter.SFFPolygonList()
        no_polygons3 = _random_integer(stop=100)
        for i in _xrange(no_polygons3):
            polygon = adapter.SFFPolygon()
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
        segmentation = adapter.SFFSegmentation()  # annotation
        segmentation.name = "name"
        segmentation.software = adapter.SFFSoftware(
            name="Software",
            version="1.0.9",
            processingDetails="Processing details"
        )
        segmentation.details = "Details"
        # global external references
        segmentation.global_external_references = adapter.SFFGlobalExternalReferences()
        segmentation.global_external_references.add_external_reference(
            adapter.SFFExternalReference(
                type='one',
                otherType='two',
                value='three'
            )
        )
        segmentation.global_external_references.add_external_reference(
            adapter.SFFExternalReference(
                type='four',
                otherType='five',
                value='six'
            )
        )
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        biol_ann = adapter.SFFBiologicalAnnotation()
        biol_ann.name = "Segment1"
        biol_ann.description = "Some description"
        # external refs
        biol_ann.external_references = adapter.SFFExternalReferences()
        biol_ann.external_references.add_external_reference(
            adapter.SFFExternalReference(
                type="sldjflj",
                value="doieaik"
            )
        )
        biol_ann.external_references.add_external_reference(
            adapter.SFFExternalReference(
                type="sljd;f",
                value="20ijalf"
            )
        )
        biol_ann.external_references.add_external_reference(
            adapter.SFFExternalReference(
                type="lsdjlsd",
                otherType="lsjfd;sd",
                value="23ijlsdjf"
            )
        )
        biol_ann.number_of_instances = 30
        segment.biological_annotation = biol_ann
        # complexes and macromolecules
        # complexes
        comp_mac = adapter.SFFComplexesAndMacromolecules()
        comp = adapter.SFFComplexes()
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        comp.add_complex(str(_random_integer(1, 1000)))
        # macromolecules
        macr = adapter.SFFMacromolecules()
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
        segment.colour = adapter.SFFRGBA(
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
        segmentation = adapter.SFFSegmentation()
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        segmentation.segments.add_segment(segment)
        # segmentation two
        segmentation2 = adapter.SFFSegmentation()
        segmentation2.segments = adapter.SFFSegmentList()
        segmentation2.segments.add_segment(adapter.SFFSegment())
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
        matrix = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms.add_transform(matrix)

        transforms2 = adapter.SFFTransformList()
        matrix2 = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms2.add_transform(matrix2)

        self.assertIsNotNone(transforms[0].id)
        self.assertEqual(transforms[0].id, transforms2[0].id)

    def test_read_sff(self):
        """Read from XML (.sff) file"""
        sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        segmentation = adapter.SFFSegmentation.from_file(sff_file)
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
        segmentation = adapter.SFFSegmentation(hff_file)
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
        segmentation = adapter.SFFSegmentation(json_file)
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
        with h5py.File(self.test_hdf5_fn, 'w') as h:
            group = h.create_group("container")
            group = colour.as_hff(group)
            self.assertIn("colour", group)
            self.assertCountEqual(group['colour'][()], colour.value)

    def test_from_hff(self):
        """Test create from HDF5 group"""
        colour = adapter.SFFRGBA(
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
            colour2 = adapter.SFFRGBA.from_hff(h['container'])
            self.assertCountEqual(colour.value, colour2.value)

    def test_native_random_colour(self):
        """Test that using a kwarg random_colour will set random colours"""
        colour = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(0 <= colour.red <= 1)
        self.assertTrue(0 <= colour.green <= 1)
        self.assertTrue(0 <= colour.blue <= 1)
        self.assertTrue(0 <= colour.alpha <= 1)


class TestSFFComplexes(Py23FixTestCase):
    """Tests for SFFComplexes class"""

    def test_default(self):
        """Test default settings"""
        c = adapter.SFFComplexes()
        self.assertEqual(c.gds_type, adapter.emdb_sff.complexType)
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
        vs = adapter.SFFVolumeStructure(cols=10, rows=20, sections=30)
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
        cls.lattice_size = adapter.SFFVolumeStructure(
            cols=10, rows=10, sections=10,
        )
        cls.lattice_endianness = 'little'
        cls.lattice_mode = 'uint32'
        cls.lattice_start = adapter.SFFVolumeIndex(cols=0, rows=0, sections=0)
        data_ = numpy.array(range(1000), dtype=numpy.uint32).reshape((10, 10, 10))  # data
        numpy.random.shuffle(data_)  # shuffle in place
        cls.lattice_data = data_
        lattices = adapter.SFFLatticeList()  # to reset lattice_id
        cls.lattice = adapter.SFFLattice(
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

    def test_iterate(self):
        """Test default settings"""
        S = adapter.SFFSegmentList()
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        for s in S:
            print(s.id, file=sys.stderr)
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        S.add_segment(adapter.SFFSegment())
        for s in S:
            print(s, file=sys.stderr)
        S.add_segment(adapter.SFFSegment.from_gds_type(
            adapter.emdb_sff.segmentType()
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
