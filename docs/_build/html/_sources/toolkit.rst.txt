========================================================
EMDB-SFF Read/Write Toolkit (``sfftk-rw``)
========================================================

.. note::

    Looking to convert other segmentation file formats to EMDB-SFF? Then checkout the
    `sfftk package <https://pypi.org/project/sfftk/>`_.

.. contents::

Introduction
============

``sfftk-rw`` is a Python package that consists of command-line utilities and an API for reading and writing
`Electron Microscopy Data Bank - Segmentation File Format
(EMDB-SFF) <https://github.com/emdb-empiar/EMDB-SFF>`_ files.
It is designed to exclusively handle EMDB-SFF files meaning fewer
dependencies simplifying integration into existing applications.

It is a core dependency for ``sfftk``, which extends it by adding functionality
to convert various application-specific segmentation file formats to EMDB-SFF.

License
-------

``sfftk-rw`` is free and open source software released under the terms of the Apache License,
Version 2.0. Source code is copyright EMBL-European Bioinformatics Institute (EMBL-EBI) 2017.

Data Model
----------

The corresponding schema may be obtained at `http://wwwdev.ebi.ac.uk/pdbe/emdb/emdb_static/doc/segmentation_da_docs/segmentation_da.html
<http://wwwdev.ebi.ac.uk/pdbe/emdb/emdb_static/doc/segmentation_da_docs/segmentation_da.html>`_.
Changes to the schema are welcome for discussion at the *Segmentation Working Group*
at `https://listserver.ebi.ac.uk/mailman/listinfo/segtrans-wg
<https://listserver.ebi.ac.uk/mailman/listinfo/segtrans-wg>`_.

Contact
-------

Any questions or comments should be addressed to
`ardan@ebi.ac.uk <mailto:ardan@ebi.ac.uk>`_ or
`pkorir@ebi.ac.uk <mailto:pkorir@ebi.ac.uk>`_.

Publications
------------

The following articles should be cited whenever ``sfftk-rw`` is used in a
publication:

.. note::

    Article in preparation

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

Source
~~~~~~

The ``sfftk-rw`` source is available from Github
`https://github.com/emdb-empiar/sfftk-rw <https://github.com/emdb-empiar/sfftk-rw>`_. You may install the bleeding
edge using:

.. code-block:: bash

    pip install git+https://github.com/emdb-empiar/sfftk-rw.git

User Interface
--------------

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
---------------

As a data model, EMDB-SFF is file format agnostic. However, EMDB-SFF files are currently expressed as either
XML, HDF5 and JSON (textual annotations only). ``sfftk-rw`` allows interconversion between these formats.

Use the ``convert`` utility to carry out interconversions:

.. code-block:: bash

    sff-rw convert file.sff

By default all ``sfftk-rw`` converts to XML except when it receives to HDF5.

For a full description of how to perform format interconversion, please see the
`guide to format interconversion <https://sfftk-rw.readthedocs.io/en/lkatest/converting.html>`_.

Viewing
----------

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

