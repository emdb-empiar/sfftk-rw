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

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase, _random_float, _random_floats
from ..core import _xrange, _str
from ..schema import adapter, emdb_sff, base

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
            mode='uint32',
            endianness='little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        lattice2 = adapter.SFFLattice(
            mode='float32',
            endianness='big',
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

    def test_create_3D(self):
        """Create an SFFSegmentation object with 3D volume segmentation from scratch"""
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.primary_descriptor = "threeDVolume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(str, range(12)))
            )
        )
        transforms.append(
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
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)]).reshape(20, 20, 20)
        lattice = adapter.SFFLattice(
            mode='uint32',
            endianness='little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        lattice2 = adapter.SFFLattice(
            mode='float32',
            endianness='big',
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
        segmentation.software = adapter.SFFSoftware(
            name=rw.random_word(),
            version=rw.random_word(),
            processingDetails=li.get_sentence(),
        )
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
        )
        transforms.append(transform)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        shapes.append(ellipsoid2)
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
            data=" ".join(map(str, range(12))),
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
        segmentation.export(os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'test_shape_segmentation.hff'))
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
            vertices1.append(vertex)
        polygons1 = adapter.SFFPolygonList()
        no_polygons1 = _random_integer(stop=100)
        for i in _xrange(no_polygons1):
            polygon = adapter.SFFPolygon()
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
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
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
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
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygon.add_vertex(random.choice(range(_random_integer())))
            polygons3.append(polygon)
        mesh.vertices = vertices3
        mesh.polygons = polygons3
        meshes.append(mesh)
        segment.meshes = meshes
        segments.append(segment)
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
        segmentation.global_external_references.append(
            adapter.SFFExternalReference(
                type='one',
                otherType='two',
                value='three'
            )
        )
        segmentation.global_external_references.append(
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
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                type="sldjflj",
                value="doieaik"
            )
        )
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                type="sljd;f",
                value="20ijalf"
            )
        )
        biol_ann.external_references.append(
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
        comp.append(str(_random_integer(1, 1000)))
        comp.append(str(_random_integer(1, 1000)))
        comp.append(str(_random_integer(1, 1000)))
        comp.append(str(_random_integer(1, 1000)))
        comp.append(str(_random_integer(1, 1000)))
        # macromolecules
        macr = adapter.SFFMacromolecules()
        macr.append(str(_random_integer(1, 1000)))
        macr.append(str(_random_integer(1, 1000)))
        macr.append(str(_random_integer(1, 1000)))
        macr.append(str(_random_integer(1, 1000)))
        macr.append(str(_random_integer(1, 1000)))
        macr.append(str(_random_integer(1, 1000)))
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
        matrix = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms.append(matrix)

        transforms2 = adapter.SFFTransformList()
        matrix2 = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(str, range(9))))
        transforms2.append(matrix2)

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
        segmentation = adapter.SFFSegmentation.from_file(hff_file)
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
        segmentation = adapter.SFFSegmentation.from_file(json_file)
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
        self.assertEqual(c.gds_type, emdb_sff.complexType)
        self.assertRegex(_str(c), r"SFFComplexes\(\[.*\]\)")
        with self.assertRaises(StopIteration):  # because it's empty
            next(iter(c))
        c.append(rw.random_word())
        self.assertEqual(len(c), 1)
        c.append(rw.random_word())
        self.assertEqual(len(c), 2)
        c.clear()
        self.assertEqual(len(c), 0)


class TestSFFMacromolecules(Py23FixTestCase):
    def test_default(self):
        """Test default settings"""
        m = adapter.SFFMacromolecules()
        self.assertRegex(_str(m), r"SFFMacromolecules\(\[.*\]\)")
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
        self.assertIsNone(C.complexes)
        self.assertIsNone(C.macromolecules)
        self.assertRegex(_str(C),
                         "SFFComplexesAndMacromolecules\(complexes=None, macromolecules=None\)")
        c = adapter.SFFComplexes()
        _no_items = _random_integer(start=2, stop=10)
        [c.append(rw.random_word()) for _ in _xrange(_no_items)]
        C.complexes = c
        m = adapter.SFFMacromolecules()
        [m.append(rw.random_word()) for _ in _xrange(_no_items)]
        C.macromolecules = m
        self.assertEqual(len(C.complexes), _no_items)
        self.assertEqual(len(C.macromolecules), _no_items)
        self.assertRegex(_str(C),
                         "SFFComplexesAndMacromolecules\(complexes=SFFComplexes\(.*\), macromolecules=SFFMacromolecules\(.*\)\)")
        print(C, file=sys.stderr)


class TestSFFExternalReference(Py23FixTestCase):
    def setUp(self):
        self.i = _random_integer()
        self.t = rw.random_word()
        self.o = rw.random_word()
        self.v = rw.random_word()
        self.l = " ".join(rw.random_words(count=3))
        self.d = li.get_sentence()

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
            """SFFExternalReference(type="{}", otherType="{}", value="{}", label="{}", description="{}")""".format(
                self.t, self.o, self.v, self.l, self.d
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
            """SFFExternalReference(type="{}", otherType="{}", value="{}", label="{}", description="{}")""".format(
                self.t, self.o, self.v, self.l, self.d
            )
        )


class TestSFFExternalReferences(Py23FixTestCase):
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
        E = adapter.SFFExternalReferences()
        [E.append(e) for e in ee]
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferences\(\[.*\]\)"""
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
        E = adapter.SFFExternalReferences.from_gds_type(_E)
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferences\(\[.*\]\)"""
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
        E = adapter.SFFExternalReferences()
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
        print(b, file=sys.stderr)
        self.assertRegex(
            _str(b),
            r"""SFFBiologicalAnnotation\(""" \
            r"""name="{}", description="{}", """ \
            r"""numberOfInstances={}, """ \
            r"""externalReferences=SFFExternalReferences\(\[.*\]\)\)""".format(
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
            r"""externalReferences=SFFExternalReferences\(\[.*\]\)\)""".format(
                self.name,
                self.description,
                self.no
            )
        )
        self.assertEqual(b.name, self.name)
        self.assertEqual(b.description, self.description)
        self.assertEqual(b.number_of_instances, self.no)
        self.assertEqual(b.external_references, self.external_references)


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
        self.r, self.c, self.s = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10), _random_integer(
            start=2, stop=10)
        self.l_mode = 'float64'
        self.l_endian = 'little'
        self.l_size = adapter.SFFVolumeStructure(rows=self.r, cols=self.c, sections=self.s)
        self.l_start = adapter.SFFVolumeIndex(rows=0, cols=0, sections=0)
        self.l_data = numpy.random.rand(self.r, self.c, self.s)
        self.l_bytes = adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian)
        self.l_unicode = self.l_bytes.decode('utf-8')

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
            """SFFLattice(mode="{}", endianness="{}", size={}, start={}, data={})""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                l.data[:100] + b"..."
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
            """SFFLattice(mode="{}", endianness="{}", size={}, start={}, data={})""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                l.data[:100] + b"..."
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
            """SFFLattice(mode="{}", endianness="{}", size={}, start={}, data={})""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                l.data[:100] + b"..."
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
            """SFFLattice(mode="{}", endianness="{}", size={}, start={}, data={})""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                l.data[:100] + b"..."
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
            """SFFLattice(mode="{}", endianness="{}", size={}, start={}, data={})""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                l.data[:100] + b"..."
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
        mode_ = 'uint8'
        _bytes = adapter.SFFLattice._encode(_data, endianness='big', mode=mode_)
        _l = emdb_sff.latticeType(
            mode=mode_,
            endianness='big',
            size=emdb_sff.volumeStructureType(cols=c, rows=r, sections=s),
            start=emdb_sff.volumeIndexType(cols=0, rows=0, sections=0),
            data=_bytes
        )
        l = adapter.SFFLattice.from_gds_type(_l)
        self.assertTrue(hasattr(l, 'data_array'))


class TestSFFMesh(Py23FixTestCase):
    """Test the SFFMesh class"""

    def setUp(self):
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
        # self.vertices = adapter.SFFVertexList()
        # [self.vertices.append(
        #     adapter.SFFVertex(
        #         x=_random_float(10),
        #         y=_random_float(10),
        #         z=_random_float(10),
        #     )
        # ) for _ in _xrange(self._no_vertices)]
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
        # self.polygons = adapter.SFFPolygonList()
        # [self.polygons.append(
        #     adapter.SFFPolygon(
        #         v=[
        #             _random_integer(start=2, stop=20),
        #             _random_integer(start=2, stop=20),
        #             _random_integer(start=2, stop=20),
        #         ]
        #     )
        #
        # ) for _ in _xrange(self._no_polygons)]
        self.polygons = adapter.SFFPolygonList.from_gds_type(self._polygons)

    def tearDown(self):
        adapter.SFFMesh.reset_id()

    def test_default(self):
        """Test default settings"""
        m = adapter.SFFMesh(vertexList=self.vertices, polygonList=self.polygons)
        self.assertRegex(
            _str(m),
            r"""SFFMesh\(id=\d+, vertexList=SFFVertexList\(\[.*\]\), polygonList=SFFPolygonList\(\[.*\]\)\)"""
        )
        self.assertEqual(m.id, 0)
        self.assertEqual(m.vertices, self.vertices)
        self.assertEqual(m.polygons, self.polygons)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _m = emdb_sff.meshType(vertexList=self._vertices, polygonList=self._polygons)
        m = adapter.SFFMesh.from_gds_type(_m)
        print(m, file=sys.stderr)
        self.assertRegex(
            _str(m),
            r"""SFFMesh\(id=\d+, vertexList=SFFVertexList\(\[.*\]\), polygonList=SFFPolygonList\(\[.*\]\)\)"""
        )
        self.assertEqual(m.vertices, self.vertices)
        self.assertEqual(m.polygons, self.polygons)


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
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        for s in S:
            print(s.id, file=sys.stderr)
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        S.append(adapter.SFFSegment())
        for s in S:
            print(s, file=sys.stderr)
        S.append(adapter.SFFSegment.from_gds_type(
            emdb_sff.segmentType()
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
class TestSFFTransformationMatrix(Py23FixTestCase):
    """Test the SFFTransformationMatrix class"""

    def test_create_init(self):
        """Test creating from __init__"""
        r, c = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10)
        _d = _random_floats(r * c)
        d = " ".join(list(map(_str, _d)))
        T = adapter.SFFTransformationMatrix(
            rows=r,
            cols=c,
            data=d
        )
        self.assertEqual(T.rows, r)
        self.assertEqual(T.cols, c)
        self.assertEqual(T.data, d)
        self.assertEqual(T.data_array.flatten().tolist(), _d)

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
        self.assertTrue(hasattr(t, 'data_array'))


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
