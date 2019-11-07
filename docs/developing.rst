==========================================================
Developing with ``:py:class:`.SFFtk`-rw``
==========================================================

.. contents::

------------
Introduction
------------

``:py:class:`.SFFtk`-rw`` is designed to be relatively straightforward to integrate into other Python applications.

The main components of the package are:

*   the **schema** package (:py:mod:`:py:class:`.SFFtkrw`.schema`) contains two modules:

    -   the **adapter** module (:py:mod:`:py:class:`.SFFtkrw`.schema.adapter`) provides the main API which handles how data fields
        are represented independent of the file formats to be used (XML, HDF5 and JSON). This package provides an
        adapter to the underlying `GenerateDS <https://www.davekuhlman.org/generateDS.html>`_ API which
        *extends* and *simplifies* EMDB-SFF fields.

    -   the **base** module (:py:mod:`:py:class:`.SFFtkrw`.schema.base`) provides the core functionality encapsulated in a set of
        classes that are actualised in the **adapter** module. There are five (5) base classes:

        +   :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFType` defines several class variables which bind each adapter to the
            underlying `generateDS` API;

        +   :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFIndexType` extends :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFType` by adding
            support for indexing;

        +   :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFListType` extends :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFType` by adding
            container attributes;

        +   :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFAttribute` defines a descriptor class that handles attributes, and

        +   :py:class:`:py:class:`.SFFtkrw`.schema.base.SFFTypeError` defines an exception class that reports custom
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

    from :py:class:`.SFFtkrw`.schema.adapter import :py:class:`.SFFSegmentation`
    from :py:class:`.SFFtkrw`.unittests import TEST_DATA_PATH

    # XML file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    print(seg_fn)
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    # HDF5 file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    # JSON file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.json')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

Creating A New Segmentation
=================================
Creating a new segmentation is a more involving exercise as you need to populate all required fields.

.. code-block:: python

    from __future__ import print_function
    import sys

    from :py:class:`.SFFtkrw`.schema import adapter

    seg = adapter.SFFSegmentation()

    # We can view how the file looks like so far; note the lack of an XML header <?xml ...>
    seg.export(sys.stderr)
    """<segmentation>
        <version>0.7.0.dev0</version>
    </segmentation>"""

Exporting to File
============================================
The :py:meth:`.SFFSegmentation.export` method provides a direct way to write your segmentation to disk. All it requires is the name of the output file with the correct extension (``":py:class:`.SFF`"`` for XML, ``"hff"`` for HDF5 or ``"json"`` for JSON).

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
All classes with ``*List`` in their name are *containers* of corresponding objects (we will refer to these as *items*) e.g. a :py:class:`.SFFTransformList` holds :py:class:`.SFFTransformationMatrix` items.

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
        print(segment.id, segment.parentID)


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

    for extRef in segment.biological_annotation.externalReferences:
        print(extRef.type)
        print(extRef.otherType)
        print(extRef.value)
        print(extRef.label)
        print(extRef.description)


Index Operations
======================

You can *retrieve*, *set* or *delete* an item from a container using Python’s index syntax. However, you cannot perform slicing (yet).

.. code-block:: python

    import os

    from :py:class:`.SFFtkrw`.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    print(seg.transforms[0])

Python List Methods
======================

The following methods are the preferred way to modify a container as they routinely update the container dictionary for quick access (see the section below on IDs).

*   :py:meth:`.append` 
*   :py:meth:`.clear`
*   :py:meth:`.copy`
*   :py:meth:`.extend`
*   :py:meth:`.insert`
*   :py:meth:`.pop`
*   :py:meth:`.remove(ite`
*   :py:meth:`.reverse`

Dictionary Getter (except for :py:class:`.SFFComplexList` and :py:class:`.SFFMacromoleculeList`)
==========================================================================================================
The Python list methods above update an internal dictionary which allows direct access by ID. This provides both the IDs and the items using two special methods:
:py:meth:`get_ids()` returns a :py:func:`dict_key` object (Python3) or a :py:func:`list` which contains the sequence of item IDs. You can cast this to a list. In Python3, the `dict_key` is automatically updated once referenced.

.. code-block:: python

    import os

    from :py:class:`.SFFtkrw`.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    # segment IDs
    print(seg.segments.get_ids())
    # Python3: dict_keys([15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578])
    # Python2: [15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578]

:py:meth:`get_by_id(id)` returns the object with the corresponding ID. The parent class ensures that no overwriting is done so you should expect that the container maintains integrity.

.. code-block:: python

    import os

    from :py:class:`.SFFtkrw`.schema import adapter

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    segment = seg.segments.get_by_id(15559)
    print(segment)

Reset IDs on Instantiation
=================================
Instantiating a container resets the auto-incrementing IDs for all future instances of the corresponding item class. For example, creating a new :py:class:`.SFFSegmentList` object guarantees that all subsequently created :py:class:`.SFFSegment` objects will start counting IDs from 1 (default) again while creating a new :py:class:`.SFFLatticeList` means all future new :py:class:`.SFFLattice` objects will start counting IDs from 0 (default). Please keep this in mind when working with indexed items.

.. code-block:: python

    from :py:class:`.SFFtkrw`.schema import adapter

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

        from :py:class:`.SFFtkrw`.schema import emdb_sff, adapter # the auto API and the adapter

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

        from :py:class:`.SFFtkrw`.schema import adapter

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

        from :py:class:`.SFFtkrw`.schema import adapter

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

        from :py:class:`.SFFtkrw`.schema import adapter

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

    from :py:class:`.SFFtkrw`.schema import adapter

    T = adapter.SFFTransformationMatrix(
        rows=3, cols=4,
        data="1 0 0 0 0 1 0 0 0 0 1 0"
    )

Implicit
------------------------------------
Use the :py:meth:`.SFFTransformationMatrix.from_array` class method to create an :py:meth:`.SFFTransformationMatrix` object directly from a ``numpy`` 2D array.

.. code-block:: python

    import numpy
    from :py:class:`.SFFtkrw`.schema import adapter

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
    from :py:class:`.SFFtkrw`.schema import adapter

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
    from :py:class:`.SFFtkrw`.schema import adapter

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
    from :py:class:`.SFFtkrw`.schema import adapter

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
This is the main class to represent RGBA colours. Aside from being able to set channel values or leave them blank we also provide an argument to generate colours randomly.
[code]

------------------------------------
Segment Geometry
------------------------------------
We show how to represent a segment using the three types of geometry by example.

Meshes: :py:class:`.SFFMeshList`, :py:class:`.SFFMeshes`, :py:class:`.SFFVertexList`, :py:class:`.SFFVertex`, :py:class:`.SFFPolygonList`, and :py:class:`.SFFPolygon`
==========================================================================================================================================================================================
First, create the mesh container that will hold the meshes.
Then create the vertex list and polygon lists.
Next, populate the vertex lists and polygon lists with vertices and polygons, respectively.
Now create the mesh and add it to the mesh list.
Repeat this for as many meshes will need to be contained in the mesh list.
[code]

3D Volumes: :py:class:`.SFFLatticeList`, :py:class:`.SFFThreeDVolume`, :py:class:`.SFFVolumeStructure`, :py:class:`.SFFVolumeIndex`
==================================================================================================================================================
First, define the lattice container
then define the volume structure and starting index objects.
Now create the lattice and add it to the list of lattices.
For each segment (voxel value) in the lattice create a 3D volume object that references the lattice.
[code]

Shape Primitives: :py:class:`.SFFShapePrimitveList`, :py:class:`.SFFCone`, :py:class:`.SFFCuboid`, :py:class:`.SFFCylinder`, :py:class:`.SFFEllipsoid`, :py:class:`.SFFSubtomogramAverage`
=====================================================================================================================================================================================================
Create a shape container for all shapes.
Then load each shape once created into this shape container.
[code]



Extensive Examples

-----------------------
Reading EMDB-SFF Files
-----------------------

All aspects of the structure of an EMDB-SFF file are handled by :py:mod:`:py:class:`.SFFtkrw`.schema.adapter` package which
defines the :py:class:`.SFFSegmentation` class to handle reading, creation and writing of
EMDB-SFF files. Please consult the section on :ref:`output_formats` for background information.

You can read an EMDB-SFF file directly by using the :py:meth:`.SFFSegmentation.from_file` class method.

.. code-block:: python

    from __future__ import print_function
    import os

    from :py:class:`.SFFtkrw`.schema.adapter import :py:class:`.SFFSegmentation`
    from :py:class:`.SFFtkrw`.unittests import TEST_DATA_PATH

    # XML file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    print(seg_fn)
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    # HDF5 file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

    # JSON file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.json')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)


Viewing Segmentation Metadata
==============================

.. code-block:: python

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
    seg = :py:class:`.SFFSegmentation`.from_file(seg_fn)

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


Viewing Segments
================

.. code-block:: python

    print(seg.segments)


Getting The List of Segment IDs
--------------------------------

.. code-block:: python

    # segment IDs
    print(seg.segments.get_ids())
    # Python3: dict_keys([15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578])
    # Python2: [15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578]

Getting A Segment By ID
--------------------------------

.. code-block:: python

    segment = seg.segments.get_by_id(15559)
    print(segment)


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


--------------------------
Creating EMDB-SFF Objects
--------------------------

Users can create EMDB-SFF objects from scratch then export them to a file format of your choice.

.. code-block:: python

    from __future__ import print_function
    from :py:class:`.SFFtkrw`.schema import adapter
    import sys
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
    from :py:class:`.SFFtkrw`.schema import adapter
    import sys
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
    bioAnn.number_ofInstances = 1
    
    # define the external references
    extRefs = adapter.SFFExternalReferenceList()
    extRefs.append(
    adapter.SFFExternalReference(
        type="ncbitaxon",
        otherType="http://purl.obolibrary.org/obo/NCBITaxon_559292",
        value="NCBITaxon_559292",
        label="Saccharomyces cerevisiae S288C",
        description="",
        )
    )
    extRefs.append(
        adapter.SFFExternalReference(
            type="pdb",
            otherType="http://www.ebi.ac.uk/pdbe/entry/pdb/3ja8",
            value="3ja8",
            label="",
            description="",
        )
    )
    # add the external references to the biological annotation
    bioAnn.external_references = extRefs
    
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



Setting Mesh Segments
--------------------------------

.. code-block:: python

    from random import random, randint, choice
    
    # the list of meshes
    meshes = adapter.SFFMeshList()
    
    # a mesh
    mesh = adapter.SFFMesh()
    
    # a list of vertices
    vertices = adapter.SFFVertexList()
    no_vertices = randint(0, 100)
    
    # add vertices from the list of vertices
    for i in range(no_vertices):
        vertex = adapter.SFFVertex()
        vertex.point = tuple(
            map(float, (randint(1, 1000), randint(1, 1000), randint(1, 1000)))
        )
        vertices.append(vertex)

    # a list of polygons

    polygons = adapter.SFFPolygonList()
    no_polygons = randint(0, 100)
    
    # add polygons to the list of polygons

    for i in range(no_polygons):
        polygon = adapter.SFFPolygon()
        polygon.append(choice(range(randint(1, 1000))))
        polygon.append(choice(range(randint(1, 1000))))
        polygon.append(choice(range(randint(1, 1000))))
        polygons.append(polygon)

    # set the vertices and polygons on the mesh
    mesh.vertices = vertices
    mesh.polygons = polygons
    
    # add the mesh to the list of meshes
    meshes.append(mesh)
    
    # add the mesh to the segment
    segment.meshes = meshes
    segment.meshes
    # meshList
    print(len(segment.meshes))
    # 1
    

Setting Shape Segments
--------------------------------

.. code-block:: python

    from random import random
    
    # a list of shape
    shapes = adapter.SFFShapePrimitiveList()
    
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

Setting Volume Segments
--------------------------------

Working with 3D volumes consists of two steps:

* first, we need to define the volumes that contain the actual volume data as a set of :py:class:`.SFFLattice` objects contained in a :py:class:`.SFFLatticeList`;

* next, we reference the lattice by specifying how the segment is associated with the lattice e.g. by contour level or voxel value using a :py:class:`.SFFThreeDVolume` object contained in a :py:class:`.SFFSegment` object as a ``volume`` attribute i.e. if ``segment`` is a :py:class:`.SFFSegment` object then ``segment.volume`` will be a :py:class:`.SFFThreeDVolume` object and we say that ``segment`` contains a ``threeDVolume`` segment representation.

.. code-block:: python

    import numpy
    import random

    # lattice container
    lattices = adapter.SFFLatticeList()
    
    # lattice 1
    _data = numpy.random.randint(0, 100, size=(20, 20, 20))
    lattice = adapter.SFFLattice(
        mode='uint32',
        endianness='little',
        size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
        start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_data,
    )
    lattices.append(lattice)
    print(lattice)
    print(lattice.mode)
    # 'uint32'
    print(lattice.endianness)
    # 'little'
    print(lattice.size)
    print(lattice.start)
    # the lattice data is base64 encoded
    print(lattice.data)
    # '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'
    # view the data as an array
    print(lattice.data_array)
    
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
    
    print(lattices)
    print(len(lattices))
    # 2
    
    # now we define the segments that reference the lattices above
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
    segments.append(segment)
    
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
    

Adding A Segment To The Segmentation
----------------------------------------------------------------
Once we have added the individual segment representations to the respective segments we can add the segment to the 
segmentation. The list of segments is contained in a :py:class:`.SFFSegmentList` object.

.. code-block:: python

    # create the list of segments
    seg.segments = adapter.SFFSegmentList()
    
    # add the segment
    seg.segments.append(segment)
    
----------------------------
Exporting EMDB-SFF Objects
----------------------------

Finally, after completing the segmentation we can export it to disk as a file. The :py:meth:`.SFFType.export` method infers the output file type from from the file extension.

.. code-block:: python

    # XML
    seg.export('file.sff')
    
    # HDF5
    seg.export('file.hff')
    
    # JSON
    seg.export('file.json')
    
--------------------------------------------
Navigating Your Way Through A Segmentation
--------------------------------------------

Iterating
================================

Segments
--------------------------------

.. code-block:: python

    for segment in seg.segments:
        # do something with segment
        print(segment.id, segment.parentID)


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

    for extRef in segment.biological_annotation.externalReferences:
        print(extRef.type)
        print(extRef.otherType)
        print(extRef.value)
        print(extRef.label)
        print(extRef.description)
    

