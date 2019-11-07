==========================================================
Developing with ``sfftk-rw``
==========================================================

.. contents::
    :depth: 2

------------
Introduction
------------

``sfftk-rw`` is designed to be relatively straightforward to integrate into other Python applications.

The main components of the package are:

*   the **schema** package (:py:mod:`sfftkrw.schema`) contains two modules:

    -   the **adapter** module (:py:mod:`sfftkrw.schema.adapter`) provides the main API which handles how data fields
        are represented independent of the file formats to be used (XML, HDF5 and JSON). This package provides an
        adapter to the underlying `GenerateDS <https://www.davekuhlman.org/generateDS.html>`_ API which
        *extends* and *simplifies* EMDB-SFF fields.

    -   the **base** module (:py:mod:`sfftkrw.schema.base`) provides the core functionality encapsulated in a set of
        classes that are actualised in the **adapter** module. There are five (5) base classes:

        +   :py:class:`sfftkrw.schema.base.SFFType` defines several class variables which bind each adapter to the
            underlying `generateDS` API;

        +   :py:class:`sfftkrw.schema.base.SFFIndexType` extends :py:class:`sfftkrw.schema.base.SFFType` by adding
            support for indexing;

        +   :py:class:`sfftkrw.schema.base.SFFListType` extends :py:class:`sfftkrw.schema.base.SFFType` by adding
            container attributes;

        +   :py:class:`sfftkrw.schema.base.SFFAttribute` defines a descriptor class that handles attributes, and

        +   :py:class:`sfftkrw.schema.base.SFFTypeError` defines an exception class that reports custom
            :py:class:`TypeError`

*   the **core** package (:py:mod:`:py:class:`.SFFtkrw`.core`) provides a set of useful utilities mainly for the command-line toolkit
    (``:py:class:`.SFF`-rw`` command) that handle command line arguments (making sure that they have the right values) and miscellaneous
    utilities.

------------------------------------------------------------------------
Working with :py:class:`.SFFSegmentation` objects
------------------------------------------------------------------------

A segmentation is represented by an :py:class:`.SFFSegmentation` object. It may be used in two ways:

*   To read a segmentation from a file

*   To create a new segmentation.

Reading EMDB-SFF Files
================================
You can read an EMDB-SFF file directly by using the :py:meth:`.SFFSegmentation.from_file` class method.

.. code-block:: python

    from __future__ import print_function
    import os

    from sfftkrw.schema.adapter import SFFSegmentation
    from sfftkrw.unittests import TEST_DATA_PATH

    # XML file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    print(seg_fn)
    seg = SFFSegmentation.from_file(seg_fn)

    # HDF5 file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')
    seg = SFFSegmentation.from_file(seg_fn)

    # JSON file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.json')
    seg = SFFSegmentation.from_file(seg_fn)
    
Viewing Segmentation Metadata
==============================

.. code-block:: python

    from __future__ import print_function
    import os

    from sfftkrw.schema.adapter import SFFSegmentation
    from sfftkrw.unittests import TEST_DATA_PATH
    
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = SFFSegmentation.from_file(seg_fn)

    # name
    print(seg.name)
    # "Segger Segmentation"

    # schema version
    print(seg.version)
    # "0.7.0.dev0"

    # software details
    print(seg.software)

    # primary descriptor
    print(seg.primary_descriptor)
    # "threeDVolume"

    # transforms
    print(seg.transforms)
    print(len(seg.transforms))
    # 2
    print(seg.transforms[0])

    # bounding box
    print(seg.bounding_box)

    # details
    print(seg.details)
    # DNA replication in eukaryotes is strictly regulated by several mechanisms. A central step in this replication is the assembly of the heterohexameric minichromosome maintenance (MCM2-7) helicase complex at replication origins during G1 phase as an inactive double hexamer. Here, using cryo-electron microscopy, we report a near-atomic structure of the MCM2-7 double hexamer purified from yeast G1 chromatin. Our structure shows that two single hexamers, arranged in a tilted and twisted fashion through interdigitated amino-terminal domain interactions, form a kinked central channel. Four constricted rings consisting of conserved interior β-hairpins from the two single hexamers create a narrow passageway that tightly fits duplex DNA. This narrow passageway, reinforced by the offset of the two single hexamers at the double hexamer interface, is flanked by two pairs of gate-forming subunits, MCM2 and MCM5. These unusual features of the twisted and tilted single hexamers suggest a concerted mechanism for the melting of origin DNA that requires structural deformation of the intervening DNA.


Creating A New Segmentation
=================================
Creating a new segmentation is a more involving exercise as you need to populate all required fields.

.. code-block:: python

    from __future__ import print_function
    import sys

    from sfftkrw.schema import adapter

    seg = adapter.SFFSegmentation()

    # We can view how the file looks like so far; note the lack of an XML header <?xml ...>
    seg.export(sys.stderr)
    """<segmentation>
        <version>0.7.0.dev0</version>
    </segmentation>"""


Setting Segmentation Metadata
================================

.. code-block:: python

    from __future__ import print_function
    import sys

    from sfftkrw.schema import adapter

    seg = adapter.SFFSegmentation()

    # segmentation name
    seg.name = 'A New Segmentation'

    # segmentation software used
    seg.software = adapter.SFFSoftware(
        name='Some Software',
        version='v0.1.3.dev3',
        processingDetails='Lorem ipsum dolor...'
    )

    # bounding box
    seg.bounding_box = adapter.SFFBoundingBox(
        xmin=0,
        xmax=512,
        ymin=0,
        ymax=1024,
        zmin=0,
        zmax=256
    )

    # an identity matrix with no transformation
    transform = adapter.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='1 0 0 0 0 1 0 0 0 0 1 0'
    )

    # add it to the list of transforms
    seg.transforms = adapter.SFFTransformList()
    seg.transforms.append(transform)

    # or from numpy
    import numpy
    seg.transforms.append(
        adapter.SFFTransformationMatrix.from_array(numpy.random.randint(1, 10, size=(5, 5)))
    )


Exporting to File
============================================

The :py:meth:`.SFFSegmentation.export` method provides a direct way to write your segmentation to disk. All it requires is the name of the output file with the correct extension (``"sff"`` for XML, ``"hff"`` for HDF5 or ``"json"`` for JSON).

.. code-block:: python

    # XML
    seg.export('file.sff')

    # HDF5
    seg.export('file.hff')

    # JSON
    seg.export('file.json')

------------------------------------
Containers
------------------------------------
All classes with ``*List`` in their name are *containers* of corresponding objects (which we will refer to as *items*) e.g. a :py:class:`.SFFTransformList` holds :py:class:`.SFFTransformationMatrix` items.

Here is a full list of all containers:

*   :py:class:`.SFFTransformList`
*   :py:class:`.SFFGlobalExternalReferenceList`
*   :py:class:`.SFFExternalReferenceList`
*   :py:class:`.SFFSegmentList`
*   :py:class:`.SFFMeshList`
*   :py:class:`.SFFVertexList`
*   :py:class:`.SFFPolygonList`
*   :py:class:`.SFFLatticeList`
*   :py:class:`.SFFComplexList`
*   :py:class:`.SFFMacromoleculeList`

Containers support the following operations: *iteration*, *index retrieval*, *Python list methods*, *direct access by item IDs*, *item ID reset on instantiation*.

Iteration
======================

You can iterate over a container object to obtain items of the corresponding class.

Segments
--------------------------------

.. code-block:: python

    for segment in seg.segments:
        # do something with segment
        print(segment.id, segment.parent_id)


Meshes
--------------------------------

.. code-block:: python

    for mesh in segment.meshes:
        for vertex in mesh.vertices:
            print(vertex.id)
            print(vertex.designation) # 'surface' or 'normal'
            x, y, z = vertex.x, vertex.y, vertex.z

        for polygon in mesh.polygons:
            print(polygon.id)
            print(polygon.vertex_ids)


External References
--------------------------------

.. code-block:: python

    for ext_ref in segment.biological_annotation.external_references:
        print(ext_ref.type)
        print(ext_ref.other_type)
        print(ext_ref.value)
        print(ext_ref.label)
        print(ext_ref.description)


Index Operations
======================

You can *retrieve*, *set* or *delete* an item from a container using Python’s index syntax. However, you cannot perform slicing (yet).

.. code-block:: python

    import os

    from sfftkrw.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = SFFSegmentation.from_file(seg_fn)

    print(seg.transforms[0])

Python List Methods
======================

The following methods are the preferred way to modify a container as they routinely update the container dictionary for quick access (see the `Dictionary Getter <dictionary_>`_ section).

*   :py:meth:`.append` 
*   :py:meth:`.clear`
*   :py:meth:`.copy`
*   :py:meth:`.extend`
*   :py:meth:`.insert`
*   :py:meth:`.pop`
*   :py:meth:`.remove(ite`
*   :py:meth:`.reverse`

.. _dictionary:

Dictionary Getter (except for :py:class:`.SFFComplexList` and :py:class:`.SFFMacromoleculeList`)
==========================================================================================================
The Python list methods above update an internal dictionary which allows direct access by ID. This provides both the IDs and the items using two special methods:
:py:meth:`get_ids()` returns a :py:func:`dict_key` object (Python3) or a :py:func:`list` which contains the sequence of item IDs. You can cast this to a list. In Python3, the `dict_key` is automatically updated once referenced.

.. code-block:: python

    import os

    from sfftkrw.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = SFFSegmentation.from_file(seg_fn)

    # segment IDs
    print(seg.segments.get_ids())
    # Python3: dict_keys([15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578])
    # Python2: [15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578]

:py:meth:`.get_by_id` returns the object with the corresponding ID. The parent class ensures that no overwriting is done so you should expect that the container maintains integrity.

.. code-block:: python

    import os

    from sfftkrw.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = SFFSegmentation.from_file(seg_fn)

    segment = seg.segments.get_by_id(15559)
    print(segment)

Reset IDs on Instantiation
=================================
Instantiating a container resets the auto-incrementing IDs for all future instances of the corresponding item class. For example, creating a new :py:class:`.SFFSegmentList` object guarantees that all subsequently created :py:class:`.SFFSegment` objects will start counting IDs from 1 (default) again while creating a new :py:class:`.SFFLatticeList` means all future new :py:class:`.SFFLattice` objects will start counting IDs from 0 (default). Please keep this in mind when working with indexed items.

.. code-block:: python

    from sfftkrw.schema import adapter

    adapter.SFFSegment.reset_id()
    new_segment = adapter.SFFSegment()
    print(new_segment) # should have an ID of 1 (segment indexes always start from 1 not 0)

------------------------------------
Indexed Objects
------------------------------------
Some classes have an auto-incrementing index associated with each object i.e. each new instance will have the index incremented by 1 on instantiation.

The following classes (double-check!) are indexed:

*   :py:class:`.SFFTransformationMatrix`
*   :py:class:`.SFFExternalReference`
*   :py:class:`.SFFSegment`
*   :py:class:`.SFFMesh`
*   :py:class:`.SFFVertex`
*   :py:class:`.SFFPolygon`
*   :py:class:`.SFFLattice`

Keep in mind the following behaviours:

*   When reading objects from a file, only those that have an index value will set it to that value; otherwise index values will be ``None``. Furthermore, :py:meth:`.get_ids()` and :py:meth:`.get_by_id()` will ignore objects with index values of ``None``.

    .. code-block:: python

        from sfftkrw.schema import emdb_sff, adapter # the auto API and the adapter

        _segment = emdb_sff.segmentType() # no ID specified
        segment = adapter.SFFSegment.from_gds_type(_segment) # ID is None

        segments = adapter.SFFSegmentList()
        segments.append(segment) # adds the segment but...
        segments.get_ids() # empty dict_keys([])


*   You can explicitly set IDs on objects but all subsequence objects with no explicit ID value will increment from the explicit value to avoid any index collisions and ensure that the dictionary can be loaded.

    .. code-block:: python

        seg1 = adapter.SFFSegment(id=37)
        seg2 = adapter.SFFSegment() # has an ID of 38

*   All indexed classes support a construction option ``new_obj`` which is ``True`` by default. If set to ``False`` then the index value is ``None`` indicating that no index is needed. This is mainly used when reading objects from a file to ensure that the IDs from the file are used instead of incrementing from the class directly (unclear).

    .. code-block:: python

        from sfftkrw.schema import adapter

        seg1 = adapter.SFFSegment(new_obj=False)
        print(seg1) # no ID
        seg2 = adapter.SFFSegment() # default: new_obj=True
        print(seg2) # has ID
        seg3 = adapter.SFFSegment(new_obj=False)
        print(seg3) # no ID
        seg4 = adapter.SFFSegment()
        print(seg4) # has ID one more than seg2

*   You can create objects with a mixture of ``new_obj=True`` and ``new_obj=False``. Incrementing of indexes continues for every ``new_obj=True``. (see example above)
*   Creating an instance of the corresponding container resets indexes for all subsequently created indexed objects of the corresponding container.

    .. code-block:: python

        from sfftkrw.schema import adapter

        # first reset IDs
        adapter.SFFSegment.reset_id()

        seg1 = adapter.SFFSegment()
        print(seg1)

        segments = adapter.SFFSegmentList()
        seg2 = adapter.SFFSegment()
        print(seg2)

        # both have ID of 1!

*   You can manually reset IDs using the :py:meth:`.reset_id` method.
*   Shapes: :py:class:`.SFFCone`, :py:class:`.SFFCuboid`, :py:class:`.SFFCylinder` and :py:class:`.SFFEllipsoid` objects all share a single ID.

    .. code-block:: python

        from sfftkrw.schema import adapter

        adapter.SFFShape.reset_id()

        cone = adapter.SFFCone()
        print(cone)
        cuboid = adapter.SFFCuboid()
        print(cuboid)
        cylinder = adapter.SFFCylinder()
        print(cylinder)
        ellipsoid = adapter.SFFEllipsoid()
        print(ellipsoid)

        # the shape container resets all IDs
        shapes = adapter.SFFShapePrimitiveList()

        cone = adapter.SFFCone()
        print(cone)
        cuboid = adapter.SFFCuboid()
        print(cuboid)
        cylinder = adapter.SFFCylinder()
        print(cylinder)
        ellipsoid = adapter.SFFEllipsoid()
        print(ellipsoid)

------------------------------------
Special Classes
------------------------------------

:py:class:`.SFFTransformationMatrix`
==============================================================
:py:class:`.SFFTransformationMatrix` objects can be instantiated in two ways:

*   explicitly with no or raw data: row, columns and a space-separated byte-sequence or unicode sequence (string) of the actual data;
*   implicitly from a numpy array (the rows and columns are inferred from the numpy array)

Explicit
------------------------------------
In this scenario the data has to be consistent i.e. the number of items in the string has to match the stated number of rows and columns.

.. code-block:: python

    from sfftkrw.schema import adapter

    T = adapter.SFFTransformationMatrix(
        rows=3, cols=4,
        data="1 0 0 0 0 1 0 0 0 0 1 0"
    )

Implicit
------------------------------------
Use the :py:meth:`.SFFTransformationMatrix.from_array` class method to create an :py:meth:`.SFFTransformationMatrix` object directly from a ``numpy`` 2D array.

.. code-block:: python

    import numpy
    from sfftkrw.schema import adapter

    t = numpy.random.rand(5, 5)
    T = adapter.SFFTransformationMatrix.from_array(t)

The `data` attribute then provides access the the string data while the :py:attr:`.SFFTransformationMatrix.data_array` attribute provides a ``numpy`` array of the matrix.

.. code-block:: python

    T.data_array


:py:class:`.SFFLattice`
===================================================
In a similar way to :py:class:`.SFFTransformationMatrix` objects, :py:class:`.SFFLattice` objects may be instantiated in several ways:

*   directly with either a ``numpy`` array, ``byte``-sequence or unicode string,
*   explicitly from a numpy array, or
*   explicitly from a byte sequence.


Direct
------------------------------------

.. code-block:: python

    import struct
    import zlib
    import base64
    import numpy
    from sfftkrw.schema import adapter

    # from numpy array
    _l = numpy.random.randint(0, 100, size=(10, 10, 10))
    ln = adapter.SFFLattice(
        mode='uint8',
        endianness='little',
        size=adapter.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_l
    )
    print(l)

    # from a byte sequence
    _b = struct.pack(">1000b", *list(numpy.random.randint(0, 127, size=(1000,)))) # big-endian, 1000, signed char integer
    # needs to be zlib compressed
    _bc = zlib.compress(_b)
    # and base64-encoded
    _bce = base64.b64encode(_bc)
    lb = adapter.SFFLattice(
        mode='int8',
        endianness='big',
        size=adapter.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_bce
    )
    print(lb)

    # the same as above but now with a unicode string of the same data
    _bceu = _bce.decode('utf-8')
    lbu = adapter.SFFLattice(
        mode='int8',
        endianness='big',
        size=adapter.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_bceu
    )
    print(lbu)


Explicit from numpy Array
------------------------------------
Use the :py:meth:`.SFFLattice.from_array`

.. code-block:: python

    import struct
    import zlib
    import base64
    import numpy
    from sfftkrw.schema import adapter

    _l = numpy.random.randint(0, 100, size=(10, 10, 10))
    l = adapter.SFFLattice.from_array(_l,
        mode='uint8',
        endianness='little',
        size=adapter.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
    )
    print(l)


Explicit from Byte Sequence
------------------------------------
Use the :py:meth:`.SFFLattice.from_bytes`

.. code-block:: python

    import struct
    import zlib
    import base64
    import numpy
    from sfftkrw.schema import adapter

    # from a byte sequence
    _b = struct.pack(">1000b", *list(numpy.random.randint(0, 127, size=(1000,)))) # big-endian, 1000, signed char integer
    # needs to be zlib compressed
    _bc = zlib.compress(_b)
    # and base64-encoded
    _bce = base64.b64encode(_bc)
    l = adapter.SFFLattice.from_bytes(_bce,
        mode='int8',
        endianness='big',
        size=adapter.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
    )
    print(l)

The ``data`` attribute then provides access the the string data while the ``data_array`` attribute provides a numpy array of the matrix.

:py:class:`.SFFRGBA`
========================================
This is the main class to represent RGBA colours.

.. code-block:: python

    from sfftkrw.schema import adapter

    colour = adapter.SFFRGBA(
        red=0.1,
        green=0.2,
        blue=0.3,
        alpha=0.7
    )
    print(colour)

Aside from being able to set channel values or leave them blank we also provide an argument to generate colours randomly.

.. code-block:: python

    from sfftkrw.schema import adapter

    colour = adapter.SFFRGBA(random_colour=True)
    print(colour)

----------------------------------------------
Working with :py:class:`.SFFSegment` objects
----------------------------------------------
We show how to represent a segment using the three types of geometry by example.

Viewing Segments
================

.. code-block:: python

    print(seg.segments)

Viewing Segment Metadata
================================

ID and Parent ID
--------------------------------

.. code-block:: python

    print(segment.id)
    # 15559
    # Every segment is a child of the root segment with parentID = 0
    print(segment.parent_id)
    # 0

Biological Annotation
--------------------------------

.. code-block:: python

    print(segment.biological_annotation)
    print(segment.biological_annotation.name)
    # 'P3 trimer'
    print(segment.biological_annotation.description)
    # 'Homotrimeric molecule of 43.1 kDa per monomer which accounts for 75% of the virion protein'
    print(segment.biological_annotation.number_of_instances)
    # 1
    print(segment.biological_annotation.external_references)
    print(segment.biological_annotation.external_references[0]) # first reference

Complexes and Macromolecules
--------------------------------

.. code-block:: python

    print(segment.complexes_and_macromolecules)
    print(segment.complexes_and_macromolecules.complexes)
    print(segment.complexes_and_macromolecules.macromolecules)

Setting Segments
================================

Setting Segment Metadata
--------------------------------

.. code-block:: python

    segment = adapter.SFFSegment()

Biological Annotation
````````````````````````````````

.. code-block:: python

    # define the biological annotation object
    bioAnn = adapter.SFFBiologicalAnnotation()
    bioAnn.name = "Segment name"
    bioAnn.description = "Some description"
    bioAnn.number_of_instances = 1

    # define the external references
    ext_refs = adapter.SFFExternalReferenceList()
    ext_refs.append(
    adapter.SFFExternalReference(
        type="ncbitaxon",
        otherType="http://purl.obolibrary.org/obo/NCBITaxon_559292",
        value="NCBITaxon_559292",
        label="Saccharomyces cerevisiae S288C",
        description="",
        )
    )
    ext_refs.append(
        adapter.SFFExternalReference(
            type="pdb",
            otherType="http://www.ebi.ac.uk/pdbe/entry/pdb/3ja8",
            value="3ja8",
            label="",
            description="",
        )
    )
    # add the external references to the biological annotation
    bioAnn.external_references = ext_refs

    # add the biological annotation to the segment
    segment.biological_annotation = bioAnn

Complexes and Macromolecules
````````````````````````````````

.. code-block:: python

    compMacr = adapter.SFFComplexesAndMacromolecules()
    # complexes
    comp = adapter.SFFComplexList()
    comp.append("comp1")
    comp.append("comp2")

    # macromolecules
    macr = adapter.SFFMacromoleculeList()
    macr.append("macr1")
    macr.append("macr2")

    # add the complexes and macromolecules
    compMacr.complexes = comp
    compMacr.macromolecules = macr

    # add them to the segment
    segment.complexes_and_macromolecules = compMacr

Colour
````````````````````````````````

Colours should be described using normalised RGBA values (each channel has a value in the interval [0,1]).

.. code-block:: python

    segment.colour = adapter.SFFRGBA(
        red=0.1,
        green=0.2,
        blue=0.3,
        alpha=0.7
    )
    print(segment.colour)




Meshes: :py:class:`.SFFMeshList`, :py:class:`.SFFMeshes`, :py:class:`.SFFVertexList`, :py:class:`.SFFVertex`, :py:class:`.SFFPolygonList`, and :py:class:`.SFFPolygon`
==========================================================================================================================================================================================
First, create the mesh container that will hold the meshes.

.. code-block:: python

    from random import random, randint, choice
    from sfftkrw.schema import adapter
    
    # the list of meshes
    meshes = adapter.SFFMeshList()

Then create the vertex list and polygon lists.

.. code-block:: python
    
    # a list of vertices
    vertices = adapter.SFFVertexList()
    no_vertices = randint(0, 100)
    
    # a list of polygons
    polygons = adapter.SFFPolygonList()
    no_polygons = randint(0, 100)
    
Next, populate the vertex lists and polygon lists with vertices and polygons, respectively.

.. code-block:: python

    # add vertices from the list of vertices
    for i in range(no_vertices):
        vertex = adapter.SFFVertex()
        vertex.point = tuple(
            map(float, (randint(1, 1000), randint(1, 1000), randint(1, 1000)))
        )
        vertices.append(vertex)


    
    # add polygons to the list of polygons
    for i in range(no_polygons):
        polygon = adapter.SFFPolygon()
        polygon.append(choice(range(randint(1, 1000))))
        polygon.append(choice(range(randint(1, 1000))))
        polygon.append(choice(range(randint(1, 1000))))
        polygons.append(polygon)
        
Now create the mesh and add it to the mesh list.

.. code-block:: python

    # a mesh
    mesh = adapter.SFFMesh()

    # set the vertices and polygons on the mesh
    mesh.vertices = vertices
    mesh.polygons = polygons

    # add the mesh to the list of meshes
    meshes.append(mesh)
    
Repeat this for as many meshes will need to be contained in the mesh list.

.. code-block:: python
    
    # add the mesh to the segment
    segment.meshes = meshes
    
    print(len(segment.meshes))

3D Volumes: :py:class:`.SFFLatticeList`, :py:class:`.SFFThreeDVolume`, :py:class:`.SFFVolumeStructure`, :py:class:`.SFFVolumeIndex`
==================================================================================================================================================
First, define the lattice container.

.. code-block:: python

    import numpy
    import random
    from sfftkrw.schema import adapter

    # lattice container
    lattices = adapter.SFFLatticeList()

then define the volume structure and starting index objects.

.. code-block:: python

    _size = adapter.SFFVolumeStructure(cols=20, rows=20, sections=20)
    _start = adapter.SFFVolumeIndex(cols=0, rows=0, sections=0)

Now create the lattice and add it to the list of lattices.

.. code-block:: python

    # lattice 1
    _data = numpy.random.randint(0, 100, size=(20, 20, 20))
    lattice = adapter.SFFLattice(
        mode='uint32',
        endianness='little',
        size=_size,
        start=_start,
        data=_data,
    )
    lattices.append(lattice)
    
    # lattice 2
    _data = numpy.random.rand(30, 40, 50)
    lattice2 = adapter.SFFLattice(
        mode='float32',
        endianness='big',
        size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
        start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
        data=_data,
    )
    lattices.append(lattice2)
    
    
For each segment (voxel value) in the lattice create a 3D volume object that references the lattice.

.. code-block:: python
    
    # now we define the segments that reference the lattices above
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
    segments.append(segment)
    
    # segment two
    segment = adapter.SFFSegment()
    vol2_value = 37.1
    segment.volume = adapter.SFFThreeDVolume(
        latticeId=2,
        value=vol2_value
    )
    segment.colour = adapter.SFFRGBA(
        red=random.random(),
        green=random.random(),
        blue=random.random(),
        alpha=random.random()
    )


Shape Primitives: :py:class:`.SFFShapePrimitveList`, :py:class:`.SFFCone`, :py:class:`.SFFCuboid`, :py:class:`.SFFCylinder`, :py:class:`.SFFEllipsoid`, :py:class:`.SFFSubtomogramAverage`
=====================================================================================================================================================================================================
Create a shape container for all shapes.

.. code-block:: python

    from random import random
    from sfftkrw.schema import adapter
    
    # a list of shape
    shapes = adapter.SFFShapePrimitiveList()

Then load each shape once created into this shape container.

.. code-block:: python
    
    # a cone
    # first we define the transform that locates it in place
    transform = adapter.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='1 0 0 0 0 1 0 0 0 0 1 0'
    )
    
    # second we define its dimension
    shapes.append(
        adapter.SFFCone(
            height=random()*100,
            bottomRadius=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transforms.append(transform)
    
    # a cuboid
    transform = adapter.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='2 0 0 5 3 0 0 27 0 0 1 9'
    )
    shapes.append(
        adapter.SFFCuboid(
            x=random()*100,
            y=random()*100,
            z=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transforms.append(transform)
    
    # a cylinder
    transform = adapter.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='2 0 0 15 3 0 0 17 0 0 1 16'
    )
    shapes.append(
        adapter.SFFCylinder(
            height=random()*100,
            diameter=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transforms.append(transform)
    
    # an ellipsoid
    transform = adapter.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='1 0 0 15 1 0 0 17 0 0 1 16'
    )
    shapes.append(
        adapter.SFFEllipsoid(
            x=random()*100,
            y=random()*100,
            z=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transforms.append(transform)






Adding A Segment To The Segmentation
==========================================================
Once we have added the individual segment representations to the respective segments we can add the segment to the 
segmentation. The list of segments is contained in a :py:class:`.SFFSegmentList` object.

.. code-block:: python

    # create the list of segments
    seg.segments = adapter.SFFSegmentList()
    
    # add the segment
    seg.segments.append(segment)
    


