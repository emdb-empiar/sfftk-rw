========================
sfftkrw.schema.base
========================

This adapter API therefore specifies two main base classes from which all other classes are built upon:

.. automodule:: sfftkrw.schema.base

:py:class:`SFFAttribute` descriptor class
================================================

Attributes of subclasses of :py:class:`SFFType` are instances of this descriptor class.

In addition to the two above classes there is a :py:class:`SFFTypeError` class which is raised whenever a type error
occurs which provides details on the required type.

.. autoclass:: SFFAttribute
    :members:
    :show-inheritance:


:py:class:`SFFType` base class
==================================

This class contains all the magic to convert a subclass definition into a user-level class. View the
API documentation of this class for details on its attributes.

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
