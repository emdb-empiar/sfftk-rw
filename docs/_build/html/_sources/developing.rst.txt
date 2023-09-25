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

    -   the **adapter** module (:py:mod:`sfftkrw` and version-specific modules in :py:mod:`sfftkw.schema`) provides the
        main API which handles how data fields
        are represented independent of the file formats to be used (XML, HDF5 and JSON). This package provides an
        adapter to the underlying `GenerateDS <https://www.davekuhlman.org/generateDS.html>`_ API which
        *extends* and *simplifies* EMDB-SFF fields.

    -   the **base** module (:py:mod:`sfftkrw.schema.base`) provides the core functionality encapsulated in a set of
        classes that are actualised in the **adapter** module. There are six (6) base classes:

        +   :py:class:`sfftkrw.schema.base.SFFType` defines several class variables which bind each adapter to the
            underlying `generateDS` API;

        +   :py:class:`sfftkrw.schema.base.SFFIndexType` extends :py:class:`sfftkrw.schema.base.SFFType` by adding
            support for indexing;

        +   :py:class:`sfftkrw.schema.base.SFFListType` extends :py:class:`sfftkrw.schema.base.SFFType` by adding
            container attributes;

        +   :py:class:`sfftkrw.schema.base.SFFAttribute` defines a descriptor class that handles attributes, and

        +   :py:class:`sfftkrw.schema.base.SFFTypeError` defines an exception class that reports custom
            :py:class:`TypeError`

        +   :py:class:`sfftkrw.schema.base.SFFValueError` is for custom :py:class:`ValueError` exceptions (particularly with
            regard to validation)

*   the **core** package (:py:mod:`sfftkrw.core`) provides a set of useful utilities mainly for the command-line toolkit
    (``sff`` command) that handle command line arguments (making sure that they have the right values) and miscellaneous
    utilities.

.. warning::

    Please note that test data is only available when you clone the repository and not when you install from PyPI.

------------------------------------------------------------------------
Working with :py:class:`sfftkrw.SFFSegmentation` objects
------------------------------------------------------------------------

A segmentation is represented by an :py:class:`sfftkrw.SFFSegmentation` object. It may be used in two ways:

*   To read a segmentation from a file

*   To create a new segmentation.

Reading EMDB-SFF Files
================================
You can read an EMDB-SFF file directly by using the :py:meth:`sfftkrw.SFFSegmentation.from_file` class method.

.. code-block:: python

    from __future__ import print_function
    import os

    from sfftkrw import SFFSegmentation
    from sfftkrw.unittests import TEST_DATA_rPATH

    # XML file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
    print(seg_fn)
    seg = SFFSegmentation.from_file(seg_fn)

    # HDF5 file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.hff')
    seg = SFFSegmentation.from_file(seg_fn)

    # JSON file
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.json')
    seg = SFFSegmentation.from_file(seg_fn)
    
Viewing Segmentation Metadata
==============================

.. code-block:: python

    from __future__ import print_function
    import os

    from sfftkrw import SFFSegmentation
    from sfftkrw.unittests import TEST_DATA_PATH
    
    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
    seg = SFFSegmentation.from_file(seg_fn)

    # name
    print(seg.name)
    # "Segger Segmentation"

    # schema version
    print(seg.version)
    # "0.8.0.dev1"

    # software details
    print(seg.software_list)

    # primary descriptor
    print(seg.primary_descriptor)
    # "three_d_volume"

    # transforms
    print(seg.transform_list)
    print(len(seg.transform_list))
    # 2
    print(seg.transform_list[0])

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

    import sfftkrw as sff

    seg = sff.SFFSegmentation()
    seg.export(sys.stderr)
    # Mon Feb 24 12:59:10 2020	SFFSegmentation(name=None, version="0.8.0.dev1") is missing the following required attributes: name, primary_descriptor
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "/Users/pkorir/PycharmProjects/sfftk-rw/sfftkrw/schema/base.py", line 234, in export
    #     raise SFFValueError("export failed due to validation error")
    # sfftkrw.schema.base.SFFValueError: export failed due to validation error

    # name and primary_descriptor are now required
    seg = sff.SFFSegmentation(name="my segmentation", primary_descriptor="three_d_volume")

    # We can view how the file looks like so far; note the lack of an XML header <?xml ...>
    seg.export(sys.stderr)
    # <segmentation>
    #    <version>0.8.0.dev1</version>
    #    <name>my segmentation</name>
    #    <primary_descriptor>three_d_volume</primary_descriptor>
    # </segmentation>


Setting Segmentation Metadata
================================

.. code-block:: python

    from __future__ import print_function
    import sys

    import sfftkrw as sff

    seg = sff.SFFSegmentation()

    # segmentation name
    seg.name = 'A New Segmentation'

    # segmentation software used
    # first create the container
    seg.software_list = sff.SFFSoftwareList()
    # then append a software object
    seg.software_list.append(
        sff.SFFSoftware(
            name='Some Software',
            version='v0.1.3.dev3',
            processing_details='Lorem ipsum dolor...'
        )
    )

    # bounding box
    seg.bounding_box = sff.SFFBoundingBox(
        xmin=0,
        xmax=512,
        ymin=0,
        ymax=1024,
        zmin=0,
        zmax=256
    )

    # an identity matrix with no transformation
    # for convenience you can use numpy arrays
    import numpy
    tx = numpy.eye(4)
    transform = sff.SFFTransformationMatrix.from_array(tx)

    # add it to the list of transforms
    seg.transform_list = sff.SFFTransformList()
    seg.transform_list.append(transform)


Exporting to File
============================================

The :py:meth:`sfftkrw.SFFSegmentation.export` method provides a direct way to write your segmentation to disk. Keep in mind it will raise an
:py:class:`.base.SFFValueError` exception if the implied data model is invalid. Please refer to `the schema documentation <https://emdb-empiar.github.io/EMDB-SFF/>`_ on which fields are mandatory/optional.

To export to a file provide the name of the output file with the correct extension (``"sff"`` for XML, ``"hff"`` for HDF5 or ``"json"`` for JSON).
It should also recognise ``.xml``, ``.h5``, and ``.hdf5``. It is case insensitive (both ``.sff`` and ``.SFF`` should work).
Additionally, there is now an alias method :py:meth:`sfftkrw.SFFSegmentation.to_file`
which mirrors the :py:meth:`sfftkrw.SFFSegmentation.from_file` method.

.. code-block:: python

    # XML
    seg.export('file.sff')
    seg.to_file('file.sff)

    # HDF5
    seg.export('file.hff')
    seg.to_file('file.hff)

    # JSON
    seg.export('file.json')
    seg.to_file('file.json)




------------------------------------
Containers
------------------------------------
All classes with ``*List`` in their name are *containers* of corresponding objects (which we will refer to as *items*) e.g. a :py:class:`sfftkrw.SFFTransformList` holds :py:class:`sfftkrw.SFFTransformationMatrix` items.

Here is a full list of all containers:

*   :py:class:`sfftkrw.SFFSoftwareList`
*   :py:class:`sfftkrw.SFFTransformList`
*   :py:class:`sfftkrw.SFFGlobalExternalReferenceList`
*   :py:class:`sfftkrw.SFFExternalReferenceList`
*   :py:class:`sfftkrw.SFFSegmentList`
*   :py:class:`sfftkrw.SFFMeshList`
*   :py:class:`sfftkrw.SFFLatticeList`
*   :py:class:`.ShapePrimitiveList`

Containers support the following operations: *iteration*, *index retrieval*, *Python list methods*, *direct access by item IDs*, *item ID reset on instantiation*.

Iteration
======================

You can iterate over a container object to obtain items of the corresponding class.

Software
-----------

.. code-block:: python

    for sw in seg.software_list:
        print(sw.name, sw.version)

Segments
--------------------------------

.. code-block:: python

    for segment in seg.segment_list:
        # do something with segment
        print(segment.id, segment.parent_id)


Meshes
--------------------------------

.. code-block:: python

    for mesh in segment.mesh_list:
        print(mesh.vertices)
        print(mesh.normals) # may be None
        print(mesh.triangles)


External References
--------------------------------

.. code-block:: python

    for ext_ref in segment.biological_annotation.external_references:
        print(ext_ref.resource)
        print(ext_ref.url)
        print(ext_ref.accession)
        print(ext_ref.label)
        print(ext_ref.description)


Index Operations
======================

You can *retrieve*, *set* or *delete* an item from a container using Python’s index syntax. However, you cannot perform slicing (yet).

.. code-block:: python

    import os

    import sfftkrw as sff
    from sfftkrw.unittests import TEST_DATA_PATH

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
    seg = sff.SFFSegmentation.from_file(seg_fn)

    print(seg.transform_list[0])

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

Dictionary Getter
============================
The Python list methods above update an internal dictionary which allows direct access by ID. This provides both the IDs and the items using two special methods:
:py:meth:`get_ids()` returns a :py:func:`dict_key` object (Python3) or a :py:func:`list` which contains the sequence of item IDs. You can cast this to a list. In Python3, the `dict_key` is automatically updated once referenced.

.. code-block:: python

    import os

    import sfftkrw as sff
    from sfftkrw.unittests import TEST_DATA_PATH

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
    seg = sff.SFFSegmentation.from_file(seg_fn)

    # segment IDs
    print(seg.segment_list.get_ids())
    # Python3: dict_keys([15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578])
    # Python2: [15559, 15560, 15561, 15562, 15563, 15564, 15565, 15566, 15567, 15568, 15569, 15570, 15571, 15572, 15573, 15574, 15575, 15576, 15577, 15578]

:py:meth:`.get_by_id` returns the object with the corresponding ID. The parent class ensures that no overwriting is done so you should expect that the container maintains integrity.

.. code-block:: python

    import os

    import sfftkrw as sff
    from sfftkrw.unittests import TEST_DATA_PATH

    seg_fn = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
    seg = sff.SFFSegmentation.from_file(seg_fn)

    segment = seg.segment_list.get_by_id(15559)
    print(segment)

Reset IDs on Instantiation
=================================
Instantiating a container resets the auto-incrementing IDs for all future instances of the corresponding item class. For example, creating a new :py:class:`sfftkrw.SFFSegmentList` object guarantees that all subsequently created :py:class:`sfftkrw.SFFSegment` objects will start counting IDs from 1 (default) again while creating a new :py:class:`sfftkrw.SFFLatticeList` means all future new :py:class:`sfftkrw.SFFLattice` objects will start counting IDs from 0 (default). Please keep this in mind when working with indexed items.

.. code-block:: python

    import sfftkrw as sff

    sff.SFFSegment.reset_id()
    new_segment = sff.SFFSegment()
    print(new_segment) # should have an ID of 1 (segment indexes always start from 1 not 0)

------------------------------------
Indexed Objects
------------------------------------
Some classes have an auto-incrementing index associated with each object i.e. each new instance will have the index incremented by 1 on instantiation.

The following classes (double-check!) are indexed:

*   :py:class:`sfftkrw.SFFSoftware`
*   :py:class:`sfftkrw.SFFTransformationMatrix`
*   :py:class:`sfftkrw.SFFExternalReference`
*   :py:class:`sfftkrw.SFFSegment`
*   :py:class:`sfftkrw.SFFMesh`
*   :py:class:`sfftkrw.SFFLattice`
*   all shape classes: :py:class:`sfftkrw.SFFCone`, :py:class:`sfftkrw.SFFCuboid`, :py:class:`sfftkrw.SFFCylinder` and :py:class:`sfftkrw.SFFEllipsoid`

Keep in mind the following behaviours:

*   When reading objects from a file, only those that have an index value will set it to that value; otherwise index values will be ``None``. Furthermore, :py:meth:`.get_ids()` and :py:meth:`.get_by_id()` will ignore objects with index values of ``None``.

    .. code-block:: python

        import sfftkrw as sff

        # the autogenerated generateDS API is available on the `gds_api` namespace
        _segment = sff.gds_api.segment_type() # no ID specified
        segment = sff.SFFSegment.from_gds_type(_segment) # ID is None

        segments = sff.SFFSegmentList()
        segments.append(segment) # adds the segment but...
        segments.get_ids() # empty dict_keys([])

    However, when you *write* to HDF5 unique IDs will be created since the entity dataset name is the ID. Therefore, if you read this back in you will have IDs that didn't
    exist in the original XML file.

*   You can explicitly set IDs on objects but all subsequence objects with no explicit ID value will increment from the explicit value to avoid any index collisions and ensure that the dictionary can be loaded.

    .. code-block:: python

        seg1 = sff.SFFSegment(id=37)
        seg2 = sff.SFFSegment() # has an ID of 38

*   All indexed classes support a construction option ``new_obj`` which is ``True`` by default. If set to ``False`` then the index value is ``None`` indicating that no index is needed. This is mainly used when reading objects from a file to ensure that the IDs from the file are used instead of incrementing from the class directly (unclear).

    .. code-block:: python

        import sfftkrw as sff

        seg1 = sff.SFFSegment(new_obj=False)
        print(seg1) # no ID
        seg2 = sff.SFFSegment() # default: new_obj=True
        print(seg2) # has ID
        seg3 = sff.SFFSegment(new_obj=False)
        print(seg3) # no ID
        seg4 = sff.SFFSegment()
        print(seg4) # has ID one more than seg2

*   You can create objects with a mixture of ``new_obj=True`` and ``new_obj=False``. Incrementing of indexes continues for every ``new_obj=True``. (see example above)
*   Creating an instance of the corresponding container resets indexes for all subsequently created indexed objects of the corresponding container.

    .. code-block:: python

        import sfftkrw as sff

        # first reset IDs
        sff.SFFSegment.reset_id()

        seg1 = sff.SFFSegment()
        print(seg1)

        segments = sff.SFFSegmentList()
        seg2 = sff.SFFSegment()
        print(seg2)

        # both have ID of 1!

*   You can manually reset IDs using the :py:meth:`.reset_id` method.
*   Shapes: :py:class:`sfftkrw.SFFCone`, :py:class:`sfftkrw.SFFCuboid`, :py:class:`sfftkrw.SFFCylinder` and :py:class:`sfftkrw.SFFEllipsoid` objects all share a single ID.

    .. code-block:: python

        import sfftkrw as sff

        sff.SFFShape.reset_id()

        cone = sff.SFFCone()
        print(cone)
        cuboid = sff.SFFCuboid()
        print(cuboid)
        cylinder = sff.SFFCylinder()
        print(cylinder)
        ellipsoid = sff.SFFEllipsoid()
        print(ellipsoid)

        # the shape container resets all IDs
        shapes = sff.SFFShapePrimitiveList()

        cone = sff.SFFCone()
        print(cone)
        cuboid = sff.SFFCuboid()
        print(cuboid)
        cylinder = sff.SFFCylinder()
        print(cylinder)
        ellipsoid = sff.SFFEllipsoid()
        print(ellipsoid)

------------------------------------
Special Classes
------------------------------------

:py:class:`sfftkrw.SFFTransformationMatrix`
==============================================================
:py:class:`sfftkrw.SFFTransformationMatrix` objects can be instantiated in two ways:

*   explicitly with no or raw data: row, columns and a space-separated byte-sequence or unicode sequence (string) of the actual data;
*   implicitly from a numpy array (the rows and columns are inferred from the numpy array)

Explicit
------------------------------------
In this scenario the data has to be consistent i.e. the number of items in the string has to match the stated number of rows and columns.

.. code-block:: python

    import sfftkrw as sff

    T = sff.SFFTransformationMatrix(
        rows=3, cols=4,
        data="1 0 0 0 0 1 0 0 0 0 1 0"
    )

Implicit
------------------------------------
Use the :py:meth:`sfftkrw.SFFTransformationMatrix.from_array` class method to create an :py:meth:`sfftkrw.SFFTransformationMatrix` object directly from a ``numpy`` 2D array.

.. code-block:: python

    import numpy
    import sfftkrw as sff

    t = numpy.random.rand(5, 5)
    T = sff.SFFTransformationMatrix.from_array(t)

The `data` attribute then provides access the the string data while the :py:attr:`sfftkrw.SFFTransformationMatrix.data_array` attribute provides a ``numpy`` array of the matrix.

.. code-block:: python

    T.data_array


:py:class:`sfftkrw.SFFLattice`
===================================================
In a similar way to :py:class:`sfftkrw.SFFTransformationMatrix` objects, :py:class:`sfftkrw.SFFLattice` objects may be instantiated in several ways:

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
    import sfftkrw as sff

    # from numpy array
    _l = numpy.random.randint(0, 100, size=(10, 10, 10))
    ln = sff.SFFLattice(
        mode='uint8',
        endianness='little',
        size=sff.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=sff.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_l
    )
    print(l)

    # from a byte sequence
    _b = struct.pack(">1000b", *list(numpy.random.randint(0, 127, size=(1000,)))) # big-endian, 1000, signed char integer
    # needs to be zlib compressed
    _bc = zlib.compress(_b)
    # and base64-encoded
    _bce = base64.b64encode(_bc)
    lb = sff.SFFLattice(
        mode='int8',
        endianness='big',
        size=sff.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=sff.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_bce
    )
    print(lb)

    # the same as above but now with a unicode string of the same data
    _bceu = _bce.decode('utf-8')
    lbu = sff.SFFLattice(
        mode='int8',
        endianness='big',
        size=sff.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=sff.SFFVolumeIndex(cols=0, rows=0, sections=0),
        data=_bceu
    )
    print(lbu)


Explicit from numpy Array
------------------------------------
Use the :py:meth:`sfftkrw.SFFLattice.from_array`

.. code-block:: python

    import struct
    import zlib
    import base64
    import numpy
    import sfftkrw as sff

    _l = numpy.random.randint(0, 100, size=(10, 10, 10))
    l = sff.SFFLattice.from_array(_l,
        mode='uint8',
        endianness='little',
        size=sff.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=sff.SFFVolumeIndex(cols=0, rows=0, sections=0),
    )
    print(l)


Explicit from Byte Sequence
------------------------------------
Use the :py:meth:`sfftkrw.SFFLattice.from_bytes`

.. code-block:: python

    from __future__ import print_function

    import struct
    import zlib
    import base64
    import numpy
    import sfftkrw as sff

    # from a byte sequence
    _b = struct.pack(">1000b", *list(numpy.random.randint(0, 127, size=(1000,)))) # big-endian, 1000, signed char integer
    # needs to be zlib compressed
    _bc = zlib.compress(_b)
    # and base64-encoded
    _bce = base64.b64encode(_bc)
    l = sff.SFFLattice.from_bytes(_bce,
        mode='int8',
        endianness='big',
        size=sff.SFFVolumeStructure(cols=10, rows=10, sections=10),
        start=sff.SFFVolumeIndex(cols=0, rows=0, sections=0),
    )
    print(l)

The ``data`` attribute then provides access the the string data while the ``data_array`` attribute provides a numpy array of the matrix.


:py:class:`sfftkrw.SFFRGBA`
========================================
This is the main class to represent RGBA colours.

.. code-block:: python

    import sfftkrw as sff

    colour = sff.SFFRGBA(
        red=0.1,
        green=0.2,
        blue=0.3,
        alpha=0.7
    )
    print(colour)

Aside from being able to set channel values or leave them blank we also provide an argument to generate colours randomly.

.. code-block:: python

    import sfftkrw as sff

    colour = sff.SFFRGBA(random_colour=True)
    print(colour)

----------------------------------------------------
Working with :py:class:`sfftkrw.SFFSegment` objects
----------------------------------------------------
We show how to represent a segment using the three types of geometry by example.

Viewing Segments
================

.. code-block:: python

    print(seg.segment_list)

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


Setting Segments
================================

Setting Segment Metadata
--------------------------------

.. code-block:: python

    segment = sff.SFFSegment()

Biological Annotation
````````````````````````````````

.. code-block:: python

    # define the biological annotation object
    bioAnn = sff.SFFBiologicalAnnotation()
    bioAnn.name = "Segment name"
    bioAnn.description = "Some description"
    bioAnn.number_of_instances = 1

    # define the external references
    ext_refs = sff.SFFExternalReferenceList()
    ext_refs.append(
    sff.SFFExternalReference(
        type="ncbitaxon",
        otherType="http://purl.obolibrary.org/obo/NCBITaxon_559292",
        value="NCBITaxon_559292",
        label="Saccharomyces cerevisiae S288C",
        description="",
        )
    )
    ext_refs.append(
        sff.SFFExternalReference(
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



Colour
````````````````````````````````

Colours should be described using normalised RGBA values (each channel has a value in the interval [0,1]).

.. code-block:: python

    segment.colour = sff.SFFRGBA(
        red=0.1,
        green=0.2,
        blue=0.3,
        alpha=0.7
    )
    print(segment.colour)




Meshes: :py:class:`sfftkrw.SFFMeshList`, :py:class:`sfftkrw.SFFMeshes`, :py:class:`sfftkrw.SFFVertices`, :py:class:`sfftkrw.SFFNormals`, :py:class:`sfftkrw.SFFTriangles`
==========================================================================================================================================================================================
First, create the mesh container that will hold the meshes.

.. code-block:: python

    import sfftkrw as sff
    
    # the list of meshes
    meshes = sff.SFFMeshList()


To create a mesh you will need to specify *vertices*, *normals* (optional) and *triangles*. These are all subclasses of
:py:class:`sfftkrw.SFFEncodedSequence` class. Here we show how to define a mesh using all three components using a simple
:py:meth:`sfftkrw.SFFVertices.from_array` method which takes a :py:class:`numpy.ndarray` object.

.. code-block:: python

    from __future__ import print_function
    import sys

    import numpy
    import sfftrw as sff

    vertices = sff.SFFVertices.from_array(numpy.random.rand(10, 3)) # 3: must be 3-space
    normals = sff.SFFNormals.from_array(numpy.random.rand(10, 3)) # normals must correspond in length to vertices
    triangles = sff.SFFTriangles.from_array(numpy.random.randint(0, 10, size=(8, 3)))

    mesh = sff.SFFMesh(
        vertices=vertices,
        normals=normals,
        triangles=triangles,
    )
    # view as XML
    mesh.export(sys.stderr)
    # view as JSON
    print(mesh.as_json())
    
Repeat this for as many meshes will need to be contained in the mesh list.

.. code-block:: python
    
    # add the mesh to the segment
    segment.mesh_list = meshes
    
    print(len(segment.mesh_list))

3D Volumes: :py:class:`sfftkrw.SFFLatticeList`, :py:class:`sfftkrw.SFFThreeDVolume`, :py:class:`sfftkrw.SFFVolumeStructure`, :py:class:`sfftkrw.SFFVolumeIndex`
===============================================================================================================================================================================================
First, define the lattice container.

.. code-block:: python

    import numpy
    import random
    import sfftkrw as sff

    # lattice container
    lattices = sff.SFFLatticeList()

then define the volume structure and starting index objects.

.. code-block:: python

    _size = sff.SFFVolumeStructure(cols=20, rows=20, sections=20)
    _start = sff.SFFVolumeIndex(cols=0, rows=0, sections=0)

Now create the lattice and add it to the list of lattices.

.. code-block:: python

    # lattice 1
    _data = numpy.random.randint(0, 100, size=(20, 20, 20))
    lattice = sff.SFFLattice(
        mode='uint32',
        endianness='little',
        size=_size,
        start=_start,
        data=_data,
    )
    lattices.append(lattice)
    
    # lattice 2
    _data = numpy.random.rand(30, 40, 50)
    lattice2 = sff.SFFLattice(
        mode='float32',
        endianness='big',
        size=sff.SFFVolumeStructure(cols=30, rows=40, sections=50),
        start=sff.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
        data=_data,
    )
    lattices.append(lattice2)
    
    
For each segment (voxel value) in the lattice create a 3D volume object that references the lattice.

.. code-block:: python
    
    # now we define the segments that reference the lattices above
    segments = sff.SFFSegmentList()
    
    # segment one
    segment = sff.SFFSegment()
    vol1_value = 1
    segment.three_d_volume = sff.SFFThreeDVolume(
        lattice_id=0,
        value=vol1_value,
    )
    segment.colour = sff.SFFRGBA(
        red=random.random(),
        green=random.random(),
        blue=random.random(),
        alpha=random.random()
    )
    segments.append(segment)
    
    # segment two
    segment = sff.SFFSegment()
    vol2_value = 37.1
    segment.three_d_volume = sff.SFFThreeDVolume(
        lattice_id=2,
        value=vol2_value
    )
    segment.colour = sff.SFFRGBA(
        red=random.random(),
        green=random.random(),
        blue=random.random(),
        alpha=random.random()
    )


Shape Primitives: :py:class:`sfftkrw.SFFShapePrimitveList`, :py:class:`sfftkrw.SFFCone`, :py:class:`sfftkrw.SFFCuboid`, :py:class:`sfftkrw.SFFCylinder`, :py:class:`sfftkrw.SFFEllipsoid`, :py:class:`sfftkrw.SFFSubtomogramAverage`
==================================================================================================================================================================================================================================================
Create a shape container for all shapes.

.. code-block:: python

    from random import random
    import sfftkrw as sff
    
    # a list of shape
    shapes = sff.SFFShapePrimitiveList()

Then load each shape once created into this shape container.

.. code-block:: python
    
    # a cone
    # first we define the transform that locates it in place
    transform = sff.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='1 0 0 0 0 1 0 0 0 0 1 0'
    )
    
    # second we define its dimension
    shapes.append(
        sff.SFFCone(
            height=random()*100,
            bottomRadius=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transform_list.append(transform)
    
    # a cuboid
    transform = sff.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='2 0 0 5 3 0 0 27 0 0 1 9'
    )
    shapes.append(
        sff.SFFCuboid(
            x=random()*100,
            y=random()*100,
            z=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transform_list.append(transform)
    
    # a cylinder
    transform = sff.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='2 0 0 15 3 0 0 17 0 0 1 16'
    )
    shapes.append(
        sff.SFFCylinder(
            height=random()*100,
            diameter=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transform_list.append(transform)
    
    # an ellipsoid
    transform = sff.SFFTransformationMatrix(
        rows=3,
        cols=4,
        data='1 0 0 15 1 0 0 17 0 0 1 16'
    )
    shapes.append(
        sff.SFFEllipsoid(
            x=random()*100,
            y=random()*100,
            z=random()*100,
            transformId=transform.id,
        )
    )
    
    # add the transform to the list of transforms
    seg.transform_list.append(transform)






Adding A Segment To The Segmentation
==========================================================
Once we have added the individual segment representations to the respective segments we can add the segment to the 
segmentation. The list of segments is contained in a :py:class:`sfftkrw.SFFSegmentList` object.

.. code-block:: python

    # create the list of segments
    seg.segment_list = sff.SFFSegmentList()
    
    # add the segment
    seg.segment_list.append(segment)
    


