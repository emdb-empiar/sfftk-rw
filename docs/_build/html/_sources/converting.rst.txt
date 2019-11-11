==================================
Interconverting EMDB-SFF Files
==================================

.. contents::

--------------
Introduction
--------------

Interconverting EMDB-SFF files is the core functions of ``sfftk-rw``. This guide describes in detail how to accomplish this.

Synopsis
=========

Running

.. code-block:: bash

    sff-rw convert
    sff-rw convert -h
    sff-rw convert --help

displays all conversion options.

.. code-block:: bash

    sff-rw convert
    usage: sff-rw convert [-h] [-p CONFIG_PATH] [-b] [-t] [-d DETAILS]
                       [-R PRIMARY_DESCRIPTOR] [-v] [-m] [-o OUTPUT | -f FORMAT]
                       [from_file [from_file ...]]

    Perform conversions to EMDB-SFF

    positional arguments:
      from_file             file to convert from

    optional arguments:
      -h, --help            show this help message and exit
      -p CONFIG_PATH, --config-path CONFIG_PATH
                            path to configs file
      -b, --shipped-configs
                            use shipped configs only if config path and user
                            configs fail [default: False]
      -t, --top-level-only  convert only the top-level segments [default: False]
      -d DETAILS, --details DETAILS
                            populates <details>...</details> in the XML file
                            [default: '']
      -R PRIMARY_DESCRIPTOR, --primary-descriptor PRIMARY_DESCRIPTOR
                            populates the
                            <primaryDescriptor>...</primaryDescriptor> to this
                            value [valid values: threeDVolume, meshList,
                            shapePrimitiveList]
      -v, --verbose         verbose output
      -m, --multi-file      enables convert to treat multiple files as individual
                            segments of a single segmentation; only works for the
                            following filetypes: stl, map, mrc, rec [default:
                            False]
      -o OUTPUT, --output OUTPUT
                            file to convert to; the extension (.sff, .hff, .json)
                            determines the output format [default: None]
      -f FORMAT, --format FORMAT
                            output file format; valid options are: sff (XML), hff
                            (HDF5), json (JSON) [default: sff]

Quick Start
============

.. code-block:: bash

    # format interconversion
    sff-rw convert file.sff --output /path/to/output/file.hff
    sff-rw convert file.hff --format json
    sff-rw convert file.sff --format sff # reduntant but should work

    # verbose
    sff-rw convert -v file.hff
    sff-rw convert --verbose file.hff

    # set details
    sff-rw convert -d "Lorem ipsum dolor..." file.sff
    sff-rw convert --details "Lorem ipsum dolor..." file.sff

    # override primary descriptor
    sff-rw convert -R shapePrimitiveList file.sff
    sff-rw convert --primary-descriptor shapePrimitiveList file.sff


.. _output_formats:


----------------------------------
EMDB-SFF Format Interconversion
----------------------------------

It is also possible to perform interconversions between XML, HDF5 and JSON
EMDB-SFF files.

.. code-block:: bash

    sff-rw convert file.sff --output /path/to/output/file.hff

or using ``--format``

.. code-block:: bash

    sff-rw convert file.hff --format json

Even null conversions are possible:

.. code-block:: bash

    sff-rw convert file.sff --format sff

As stated previously, conversion to JSON drops all geometrical descriptions.
Similarly, conversions from JSON to EMDB-SFF will not reinstate the geometric
description information.

---------------
Output Formats
---------------

EMDB-SFF files can be output as XML (``.sff``), HDF5 (``.hff``) or JSON
(``.json``).

- XML EMDB-SFF files are typically relatively large compared to HDF5 and
  JSON equivalents. The compression applied in HDF5 files makes them ideal
  for large datasets.

- JSON EMDB-SFF files do not contain geometric descriptors and are primarily
  used as temporary files during annotation.

- Interconversion of the three formats is lossless (with the exception of
  geometrical data when converting to JSON - all geometrical data is excluded).

There are two ways to perform conversion:

-  Specifying the output path with ``-o/--output`` flag

-  Specifying the output format with ``-f/--format`` flag


Specifying the output path with ``-o/--output`` flag
========================================================

Conversion is performed as follows (the output file extension determines the output format):

.. code-block:: bash

    sff-rw convert file.sff -o file.hff

will result in an HDF5 file while

.. code-block:: bash

    sff-rw convert file.sff --output file.json

will be a JSON file.

Specifying the output format with ``-f/--format`` flag
========================================================

The -f/--format options ensures that the output file will be in the same 
directory as the original segmentation file. The ``-f`` flag takes one of three
values:

-  ``sff`` for XML files

-  ``hff`` for HDF5 files

-  ``json`` for JSON files.

Any other value raises an error.

.. code-block:: bash

    sff-rw convert file.sff -f hffr
    sff-rw convert file.sff --format hff

The default format (if none is specified) is ``sff`` (XML).

.. code-block:: bash

    sff-rw convert file.hff

results in ``file.sff`` as output.


----------------------------------
Verbose Operation
----------------------------------

As with many Linux shell programs the ``-v/--verbose`` option prints status 
information on the terminal.

.. code-block:: bash

    sff-rw convert --verbose file.hff
    Tue Sep 12 15:29:18 2017 Seting output file to file.sff
    Tue Sep 12 15:29:18 2017 Converting from EMDB-SFF (HDF5) file file.hff
    Tue Sep 12 15:30:03 2017 Created SFFSegmentation object
    Tue Sep 12 15:30:03 2017 Exporting to file.sff
    Tue Sep 12 15:30:07 2017 Done

----------------------------------
Specify Details
----------------------------------

The EMDB-SFF data model provides for an optional ``<details/>`` tag for 
auxilliary information. The contents of this option will be put into 
``<details/>.``

.. code-block:: bash

    sff-rw convert --details "Lorem ipsum dolor..." file.sff

.. todo::

    Allow a user to pass a **file** whose contents will be inserted into ``<details/>``.

----------------------------------
Changing The Primary Descriptor
----------------------------------

The EMDB-SFF data model provides for three possible geometrical descriptors: 
`meshes (meshList), shape primitives (shapePrimitiveList)` and 
`3D volumes (threeDVolume)`.
 
The mandatory ``<primaryDescriptor/>`` field specifies the main geometrical
descriptor to be used when performing conversions and other processing tasks. 
Only valid values are allowed; otherwise a ``ValueError`` is raised.

