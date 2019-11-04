========================================
Miscellaneous Operations Using sfftk-rw
========================================

.. contents::

Viewing ``sfftk-rw`` Version
============================

To view the current version of ``sfftk-rw`` run:

.. code-block:: bash

    sff-rw --V
    sff-rw --version

Viewing File Metadata
=====================

.. code-block:: bash

    sff-rw view <file>

The full list of options is:

.. code-block:: bash

    sff-rw view
    usage: sff-rw view [-h] [-V] [-C] [-v] from_file

    View a summary of an SFF file

    positional arguments:
      from_file          any SFF file

    optional arguments:
      -h, --help         show this help message and exit
      -V, --version      show SFF format version
      -C, --show-chunks  show sequence of chunks in IMOD file; only works with
                         IMOD model files (.mod) [default: False]
      -v, --verbose      verbose output


Running Unit Tests
==================

.. code-block:: bash

    sff-rw tests [tool]

where ``tool`` is one of ``all``, ``core``, ``main``, ``formats``, ``readers``, ``notes`` or ``schema``.
