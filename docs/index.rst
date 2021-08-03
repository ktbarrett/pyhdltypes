========
Overview
========

pyhdltypes is a library providing accurate and high performance Python models of common VHDL and Verilog data types.
The library is intended to be used for writing models of an algorithm to be implemented in HDL.

Use Case
========

Developing HDL implementation of complex algorithms usually involves multiple people/teams.

**Algorithms designers**

* Design the algorithm at the high-level, but may be unaware of the constraints of implementation
* Most worried about algorithmic performance

**Implementers**

* Translate the algorithm into a reasonable implementation in HDL
* Most worried about feasibility of a particular algorithm design (resource utilization, clock speed)

**Testers**

* Ensure that the implementation meets requirements and is implemented correctly

All of these groups need an executable model of the algorithm for one or more reasons.

* **Algorithm designers** may use models for proof-of-concept, or as an executable algorithm specification
* **Implementers** use models as a source of truth while testing their implementation during development
* **Implementers** may use models as a way of communicating changes due to implementation constraints to the other teams
* **Testers** use models as a source of truth in their test, which may happen in simulation or on hardware
* **Algorithm designers** can use an accurate models of the implementation as a basis for exploring optimizations

Ideally, all these groups should use the same model to prevent duplication of effort or inaccuracy.
However, each group has different priorities when it comes to the model.

* **Algorithms designers** want the models to be easy to use for prototyping purposes
* **Testers and Implementers** want the models to be accurate to the implementation
* **Testers** care about execution speed, as they may run very long simulations or want to qualify production hardware as quickly as possible
* **Everyone** wants the models to be written in a language and framework they are familiar with

Existing Solutions
==================

**MATLAB**

* Very easy to prototype algorithms with.
* MATLAB has `some` capability for modeling hardware (e.g. Simulink and/or the fixed point toolkit).
* MATLAB can be difficult to integrate into simulation or hardware testing environments.
* If written improperly, it can be rather slow to execute.
* MATLAB is reasonably familiar with many groups.

**C++ and SystemC**

* Can execute fast.
* Not as easy to prototype with as other solutions.
* Easy to integrate into simulations (many HDL simulator directly support SystemC) and hardware testing (no OS necessary) environments.
* SystemC accurately models common data types used in HDL designs.
* SystemC has overall less familiarity with non-EDA-adjacent groups.
* C++ is less familiar with many groups.

**Python**

* Can execute fast using C/C++ extensions (e.g. numpy) or compilation (e.g. Cython, Nuitka).
* C++ extensions are fairly easy (thanks to pybind11).
* Python is very familiar with most groups.
* Easy to integrate into simulations (Python co-simulation or cocotb) and hardware testing (PYNQ or PetaLinux w/ Python) environments.
* **No common HDL data types.**

This library intends to solve the highlighted limitation, making Python a viable solution in this problem space.
In fact, with a quality library, it is arguably the `best` solution in the problem space.

Installation
============

pyhdltypes is a pure Python package and can be installed with ``pip``.

.. code-block::

    pip install hdltypes

.. warning::
    PyPI release not yet available

Roadmap
=======

The basic types and features will be implemented as such.

* :class:`~hdltypes.types.Logic`\ : protocol for types that support logical operators
* :class:`~hdltypes.logic.StdLogic`\ : 9-value logic type
* :class:`~hdltypes.logic.X01Z`\ : 4-value logic type
* :class:`~hdltypes.logic.Bit`\ : 2-value logic type
* :class:`~hdltypes.range.Range`\ : HDL Range type and Array indexing scheme
* :class:`~hdltypes.types.Array`\ : protocol for immutable array-like types
* :class:`~hdltypes.types.MutableArray`\ : protocol for mutable array-like types
* :class:`~hdltypes.logic.FrozenGArray`\ : immutable generic array type
* :class:`~hdltypes.array.GArray`\ : mutable version of ``FrozenGArray``
* :class:`~hdltypes.logic_array.FrozenLogicArray`\ : immutable generic ``Logic`` array type that supports element-wise logical operators
* :class:`~hdltypes.logic_array.LogicArray`\ : mutable version of ``FrozenLogicArray``
* :class:`~hdltypes.logic_array.StdLogicArray`\ : mutable ``LogicArray`` of ``StdLogic``
* :class:`~hdltypes.logic_array.X01ZArray`\ : mutable ``LogicArray``of ``X01Z``
* :class:`~hdltypes.logic_array.BitArray`\ : mutable ``LogicArray`` of ``Bit``
* :class:`~hdltypes.types.Integer`\ : protocol for integer-like types, supports logical and arithmetic operators
* :class:`~hdltypes.integer.FrozenUnsigned`\ : immutable array of ``Bit`` / ``Integer`` type with unsigned representation
* :class:`~hdltypes.integer.Unsigned`\ : mutable version of ``FrozenUnsigned``
* :class:`~hdltypes.integer.FrozenSigned`\ : immutable array of ``Bit``  / ``Integer`` type with two's complement representation
* :class:`~hdltypes.integer.Signed`\ : mutable version of ``FrozenSigned``
* :class:`~hdltypes.types.FixedPoint`\ : protocol for fixed-point-like types, supports logical and arithmetic operators, resizing, rounding, and conversion to and from :py:class:`float`
* :class:`~hdltypes.fixed.FrozenUfixed`\ : immutable array of ``Bit`` / ``FixedPoint`` type with unsigned representation
* :class:`~hdltypes.fixed.Ufixed`\ : mutable version of ``FrozenUfixed``
* :class:`~hdltypes.fixed.FrozenSfixed`\ : immutable array of ``Bit`` / ``FixedPoint`` type with two's complement representation
* :class:`~hdltypes.fixed.Sfixed`\ : mutable version of ``FrozenSfixed``
* :class:`~hdltypes.types.FixedPoint`\ : protocol for floating-point-like types, supports logical and arithmetic operators, resizing, rounding, and conversion to and from :py:class:`float`
* :class:`~hdltypes.float.FrozenFloat`\ : immutable array of ``Bit`` / floating point type
* :class:`~hdltypes.float.Float`\ : mutable version of ``FrozenFloat``

The ``Frozen`` classes may not be instantiable classes, but only for typing purposes.
However, making them instantiable may be rather easy, so that decision is still up in the air.
