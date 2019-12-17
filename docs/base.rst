========================
sfftkrw.schema.base
========================

This API specifies several base classes from which all other classes are built upon:

.. automodule:: sfftkrw.schema.base

:py:class:`SFFAttribute` descriptor class
================================================

.. autoclass:: SFFAttribute(name, sff_type=None, required=False, default=None, help="")
    :members:
    :show-inheritance:

:py:class:`SFFType` base class
==================================

.. autoclass:: SFFType
    :members:
    :show-inheritance:


:py:class:`SFFIndexType` base class
================================================

.. autoclass:: SFFIndexType
    :members:
    :show-inheritance:


:py:class:`SFFListType` base class
================================================

.. autoclass:: SFFListType
    :members:
    :show-inheritance:

:py:class:`SFFTypeError` class
==================================

.. autoclass:: SFFTypeError
    :members:
    :show-inheritance:

:py:class:`SFFValueError` class
==================================

.. autoclass:: SFFValueError
    :members:
    :show-inheritance:
