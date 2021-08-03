=========
Reference
=========

Abstract Types
==============

Abstract Base Classes and Protocols for enforcing or checking type capabilities.

.. autodata:: hdltypes.types.Self

.. autoclass:: hdltypes.types.Logic
    :members:
    :undoc-members:
    :special-members: __and__, __rand__, __or__, __ror__, __xor__, __rxor__, __invert__

Logic Types
===========

Value types that implement the :class:`~hdltypes.types.Logic` protocol.

.. autoclass:: hdltypes.logic.StdLogic
    :members:

.. autoclass:: hdltypes.logic.X01Z
    :members:

.. autoclass:: hdltypes.logic.Bit
    :members:

Utility Types
=============

.. autoclass:: hdltypes.range.Range
    :members:

