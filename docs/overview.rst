========================================================
EMDB-SFF Read/Write Toolkit (``sfftk-rw``)
========================================================

.. contents::

Introduction
============

``sfftk-rw`` is a Python toolkit for *reading and writing EMDB-SFF files only*. It is part of a family of tools
designed to work with EMDB-SFF files (see `Data Model`_ below). Other related tools are:

-   ``sfftk`` - depends on ``sfftk-rw`` and additionally:

    *   **converts** application-specific segmentation files to valid EMDB-SFF files;

    *   **annotates** EMDB-SFF files;

    *   **prepares** segmentation files prior to conversion to EMDB-SFF files;

-   **SAT** - an online wrapper around ``sfftk`` available at https://wwwdev.ebi.ac.uk/pdbe/emdb/sat_branch/sat/

.. _data_model:

Data Model
----------

The **Electron Microscopy Data Bank - Segmentation File Format (EMDB-SFF)** is an open, community-drive segmentation and transformations data model that supports **annotations** and various segmentation **geometries**.

By **annotations** we mean that segmentations may be augmented through addition of textual descriptions derived from curated ontologies and data archives in addition to free text.

Segmentation **geometries** may consist of one or more of the following structures:

*   3D volumes
*   3D surfaces
*   3D shapes

You can find out more about the data model by viewing the schema from the `EMDB Segmentation Data Model <http://wwwdev.ebi.ac.uk/pdbe/emdb/emdb_static/doc/segmentation_da_docs/segmentation_da.html>`_ page, checking out code from the `data model repository on Github <https://github.com/emdb-empiar/EMDB-SFF>`_ or reading an overview from the section `Understanding the EMDB-SFF Data Model <data_model.html>`_.

Changes to the schema are welcome for discussion at the *Segmentation Working Group*
at `https://listserver.ebi.ac.uk/mailman/listinfo/segtrans-wg
<https://listserver.ebi.ac.uk/mailman/listinfo/segtrans-wg>`_.

License
-------

``sfftk-rw`` is free and open source software released under the terms of the Apache License,
Version 2.0. Source code is copyright EMBL-European Bioinformatics Institute (EMBL-EBI) 2017.

Contact
-------

You are welcome to report queries, bugs and feature requests to `pkorir@ebi.ac.uk <mailto:pkorir@ebi.ac.uk>`_.

Publications
------------

.. The following articles should be cited whenever ``sfftk-rw`` is used in a publication:

.. .. note::

..     Article in preparation

The EMDB-SFF data model is the result of various community consultations which
are published in the following articles:

-  `Patwardhan, Ardan, Robert Brandt, Sarah J. Butcher, Lucy Collinson, David Gault, Kay Grünewald, Corey Hecksel et al. Building bridges between cellular and molecular structural biology. eLife 6 (2017). <http://europepmc.org/abstract/MED/28682240>`_

-  `Patwardhan, Ardan, Alun Ashton, Robert Brandt, Sarah Butcher, Raffaella Carzaniga, Wah Chiu, Lucy Collinson et al. A 3D cellular context for the macromolecular world. Nature structural & molecular biology 21, no. 10 (2014): 841-845. <http://europepmc.org/abstract/MED/25289590>`_

-  `Patwardhan, Ardan, José-Maria Carazo, Bridget Carragher, Richard Henderson, J. Bernard Heymann, Emma Hill, Grant J. Jensen et al. Data management challenges in three-dimensional EM. Nature structural & molecular biology 19, no. 12 (2012): 1203-1207. <http://europepmc.org/abstract/MED/23211764>`_

Getting Started
===============

Obtaining and Installing ``sfftk-rw``
-------------------------------------

We recommend installing ``sfftk-rw`` in a virtual environment of your choice (``virtualenv``, ``pyenv``, ``anaconda/miniconda``
or ``pipenv`` - see their respective documentation on how to do so).

PyPI
~~~~

``sfftk-rw`` is available on PyPI. Simply run:

.. code-block:: bash

    pip install sfftk-rw

Source Code
~~~~~~~~~~~

The ``sfftk-rw`` source is available from Github
`https://github.com/emdb-empiar/sfftk-rw <https://github.com/emdb-empiar/sfftk-rw>`_. You may install the bleeding
edge using:

.. code-block:: bash

    pip install git+https://github.com/emdb-empiar/sfftk-rw.git

Using ``sfftk-rw``
------------------

Synopsis
~~~~~~~~

There are two main ways to use ``sfftk-rw``:

*   On the command line:

    -   **view** metadata of a EMDB-SFF file

    -   **interconvert** between EMDB-SFF formats (XML, HDF5 and JSON)

*   Programmatically via `the API <sfftk-rw.html>`_:

    -   **read** EMDB-SFF files

    -   **create** valid EMDB-SFF segmentation objects and export as XML, HDF5 or JSON files

For more information on each please see the guide to the command-line and the `Developing with sfftk-rw <data_model_>`_.

User Interface
~~~~~~~~~~~~~~

``sfftk-rw`` is designed as a command-line tool with various utilities. Type ``sff-rw`` to see all options;

.. code-block:: bash

    sff-rw
    usage: sff-rw [-h] [-V] EMDB-SFF Read/Write Tools ...

    The EMDB-SFF Read/Write Toolkit (sfftk-rw)

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show the sfftk-rw version string and the supported
                            EMDB-SFF Read/Write version string

    Tools:
      The EMDB-SFF Read/Write Toolkit (sfftk-rw) provides the following tools:

      EMDB-SFF Read/Write Tools
        convert             converts between EMDB-SFF formats
        view                view file summary
        tests               run unit tests

Interconversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a data model, EMDB-SFF is file format agnostic. However, EMDB-SFF files are currently expressed as either
XML, HDF5 and JSON (textual annotations only). ``sfftk-rw`` allows interconversion between these formats.

Use the ``convert`` utility to carry out interconversions:

.. code-block:: bash

    sff-rw convert file.sff

By default all ``sfftk-rw`` converts to XML except when it receives to HDF5.

For a full description of how to perform format interconversion, please see the
`guide to format interconversion <https://sfftk-rw.readthedocs.io/en/lkatest/converting.html>`_.

Viewing
~~~~~~~~~~~~~~

Basic metadata about an EMDB-SFF file may be obtained using the ``view`` utility:

.. code-block:: bash

    sff-rw view [options] file.sff


Developing with ``sfftk-rw``
----------------------------

We have designed ``sfftk-rw`` to be easy to integrate into existing applications but are also open
for suggestions on how to improve the developer experience. Please consult the `guide to developing
with sfftk-rw <https://sfftk-rw.readthedocs.io/en/latest/developing.html>`_ or peruse
the `API documentation <http://sfftk-rw.readthedocs.io/en/latest/sfftk-rw.html>`_.

As a brief example, you can handle EMDB-SFF files using the ``SFFSegmentation`` class:

.. code-block:: python

    from sfftkrw.schema import adapter

    # read from a file
    seg = adapter.SFFSegmentation.from_file("file.sff")

    # or create one from scratch
    seg = adapter.SFFSegmentation()
    # then create relevant attributes
    seg.name = "My segmentation"
    seg.software = adapter.SFFSoftware(
        name="sfftk-rw",
        version="0.5.0",
        processingDetails="Used the command line utility to convert segmentation"
    )

    # export by specifying the name of the output file for auto format detection
    seg.export("file.hff") # HDF5

