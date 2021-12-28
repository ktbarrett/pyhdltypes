=========
Reference
=========

Abstract Types
==============

Abstract Base Classes and Protocols for enforcing or checking type capabilities.

.. note::
    When it comes to TypeVars

.. autoclass:: hdltypes.types.AbstractConstArray
    :members:

.. autoclass:: hdltypes.types.AbstractArray
    :members:

.. autoclass:: hdltypes.types.Number
    :members:

.. autoclass:: hdltypes.types.Integer
    :members:

Logic Types
===========

Value types that implement the :class:`~hdltypes.types.Logic` protocol.

.. autoclass:: hdltypes.logic.StdLogic
    :members:

.. autoclass:: hdltypes.logic.X01Z
    :members:

.. autoclass:: hdltypes.logic.Bit
    :members:

Array and Range Types
=====================

.. autoclass:: hdltypes.range.Range
    :members:

.. autoclass:: hdltypes.array.Array
    :members:
    :inherited-members:

Logic Array Types
=================

.. autoclass:: hdltypes.logic_array.LogicArrayBase
    :members:
    :show-inheritance:
    :inherited-members:

.. autoclass:: hdltypes.logic_array.StdLogicArray
    :show-inheritance:

.. autoclass:: hdltypes.logic_array.X01ZArray
    :show-inheritance:

.. autoclass:: hdltypes.logic_array.BitArray
    :show-inheritance:
