========================================================
EMDB-SFF Read/Write Toolkit (``sfftk-rw``)
========================================================

.. note::

    Looking to convert other segmentation file formats to EMDB-SFF? Then checkout the ``sfftk`` package.

.. contents::

Introduction
============


``sfftk-rw`` is a Python package that consists of command-line utilities and an API for reading and writing
`Electron Microscopy Data Bank - Segmentation File Format
(EMDB-SFF) files <https://github.com/emdb-empiar/sfftk/tree/master/sfftk/test_data/sff>`_.
It is designed to exclusively handle EMDB-SFF files meaning it has few
dependencies making it easier to integrate into existing applications.

It is a core dependency for ``sfftk``, which extends it by adding functionality
to convert various application-specific segmentation file formats to EMDB-SFF.

License
-------

``sfftk-rw`` is free and open source software released under the terms of the Apache License, Version 2.0. Source code is
copyright EMBL-European Bioinformatics Institute (EMBL-EBI) 2019.

Data Model
----------

The corresponding schema
(``v0.7.0.dev0``) may be obtained at `http://wwwdev.ebi.ac.uk/pdbe/emdb/emdb_static/doc/segmentation_da_docs/segmentation_da.html
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

Dependencies
~~~~~~~~~~~~

As with any Python software, we recommend installing it in a virtual environment (of your choice). The only dependency
that may be needed is ``numpy`` which can be installed with

.. code:: bash

    pip install numpy

PyPI
~~~~

``sfftk-rw`` is available on PyPI meaning that all that one needs to do is run:

.. code:: bash

    pip install sfftk-rwk

Source
~~~~~~

The ``sfftk-rw`` source is available from Github `https://github.com/emdb-empiar/sfftk <https://github.com/emdb-empiar/sfftk>`_.



Conversion
----------

Segmentation files may be converted to EMDB-SFF files using the ``convert``
command.

.. code:: bash

    sfr convert file.am -o file.sff

For a full description of how to perform conversion, please see the
`guide to format conversion <https://sfftk.readthedocs.io/en/latest/converting.html>`_.

Viewing
----------



Miscellaneous
-------------

``sfftk-rw`` may also be used for several miscellaneous operations such as:

-  `Viewing segmentation metadata <https://sfftk.readthedocs.io/en/latest/misc.html#viewing-file-metadata>`_


-  `Running unit tests <https://sfftk.readthedocs.io/en/latest/misc.html#running-unit-tests>`_  with the ``tests`` command

More information on this can be found in the `guide to miscellaneous operations <https://sfftk.readthedocs.io/en/latest/misc.html>`_.

Developing with ``sfftk-rw``
----------------------------

``sfftk-rw`` is developed as a set of decoupled packages providing the various
functionality. The main classes involved are found in the ``sfftk.schema package``.
Please see `full API <http://sfftk.readthedocs.io/en/latest/sfftk.html>`_.
There is also a `guide to developing with sfftk <https://sfftk.readthedocs.io/en/latest/developing.html>`_ which
provides useful instructions.

