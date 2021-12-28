# Copyright cocotb contributors
# Copyright Kaleb Barrett
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause
from functools import lru_cache
from typing import TYPE_CHECKING, Dict, Optional, Type, TypeVar, Union

LogicConstructibleT = Union[str, "StdLogic"]

Self = TypeVar("Self", bound="StdLogic")


# DEFINING SUBTYPES OF STDLOGIC
#
# A subtype must inherit from StdLogic, or a known subclass of StdLogic.
# The subtype will define a `__values__` class attribute that is a non-empty list of
# the StdLogic value representations listed directly below.
#
# Addendum: You can make existing types act as subtypes of new types using ABC.register, but mypy doesn't like it.
# For example, you can define `class UX01Z(StdLogic)`, then do `UX01Z.register(X01Z)` so that X01Z acts as a subtype of
# the newly-defined UX01Z type.


_U = 0
_X = 1
_0 = 2
_1 = 3
_Z = 4
_W = 5
_L = 6
_H = 7
__ = 8


class StdLogic:
    """
    A 9-value logic type

    The values of this types are: ``U``, ``X``, ``0``, ``1``, ``Z``, ``W``, ``L``, ``H``, and ``-``.
    The value and semantics of this type are defined in IEEE 1164 and are similar to the ``std_ulogic`` type in VHDL.

    StdLogics are constructable from string literals or are copy constructable from any subclass.

    .. code-block:: python3

        >>> StdLogic("z")  # construct from (lowercase) str
        StdLogic('Z')
        >>> StdLogic(X01Z("Z"))  # convert subtype
        StdLogic('Z')

    StdLogics support logical operations ``&``, ``|``, ``^``, and ``~``.
    They can be used in logical operations with subtypes, which will return the widest of the two types.

    .. code-block:: python3

        >>> StdLogic("0") | StdLogic("X")
        StdLogic('X')
        >>> Bit("0") ^ StdLogic("1")
        StdLogic('1')
        >>> ~StdLogic("L")
        StdLogic('1')

    StdLogic supports creating subtypes (like :class:`X01Z` and :class:`Bit`); see the module file for more details.
    Values of a subtype of StdLogic will hash the same and equate, so that they behave as proper subtypes.
    This results in what may seem like atypical behavior, but it is type-safe.

    .. code-block:: python3

        >>> StdLogic("0") == Bit("0")  # subtypes equate
        True
        >>> a = {StdLogic("0")}
        >>> Bit("0") in a        # subtypes are substitutable in hashed collections
        True
        >>> isinstance(Bit("0"), StdLogic)  # subtypes pass isinstance checks
        True

    """

    __slots__ = "_repr"
    _repr: int

    __values__ = [_U, _X, _0, _1, _Z, _L, _H, _W, __]

    @classmethod
    @lru_cache(maxsize=None)
    def _make(cls: Type[Self], repr: int) -> Self:
        self = super().__new__(cls)
        self._repr = repr
        return self

    def __new__(cls: Type[Self], value: Union[str, "StdLogic"]) -> Self:
        _repr: Optional[int]
        if isinstance(value, StdLogic):
            # convert subtype
            _repr = value._repr
            if _repr not in cls.__values__:
                raise ValueError(f"{value!r} not in {cls.__qualname__}")
            else:
                return cls._make(_repr)
        elif isinstance(value, str):
            # convert literal
            _repr = _literal_repr.get(value)
            if _repr is None:
                raise ValueError("invalid literal value")
            elif _repr not in cls.__values__:
                raise ValueError(f"literal {value!r} not in {cls.__qualname__}")
            else:
                return cls._make(_repr)
        else:
            raise TypeError(
                f"{type(value).__qualname__!r} object is not constructible into a {cls.__qualname__}"
            )

    if not TYPE_CHECKING:
        # mypy doesn't like using lru_cache on __new__
        __new__ = lru_cache(maxsize=None)(__new__)

    def __str__(self) -> str:
        return _str_table[self._repr]

    def __and__(self: Self, other: Self) -> Self:
        if isinstance(other, type(self)):
            return type(self)(_and_table[self._repr][other._repr])
        return NotImplemented

    def __rand__(self: Self, other: Self) -> Self:
        return self & other

    def __or__(self: Self, other: Self) -> Self:
        if isinstance(other, type(self)):
            return type(self)(_or_table[self._repr][other._repr])
        return NotImplemented

    def __ror__(self: Self, other: Self) -> Self:
        return self | other

    def __xor__(self: Self, other: Self) -> Self:
        if isinstance(other, type(self)):
            return type(self)(_xor_table[self._repr][other._repr])
        return NotImplemented

    def __rxor__(self: Self, other: Self) -> Self:
        return self ^ other

    def __invert__(self: Self) -> Self:
        return type(self)(_not_table[self._repr])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._repr == other._repr
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._repr)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({str(self)!r})"


class X01Z(StdLogic):
    """
    A 4-value logic type

    A subtype of :class:`StdLogic`;
    supporting all the same operations, but only the values ``X``, ``0``, ``1``, and ``Z``.
    Similar to ``X01Z`` from VHDL, or ``logic`` from Verilog.
    """

    __values__ = [_X, _0, _1, _Z]


class Bit(X01Z):
    """
    A 2-value logic type

    A subtype of :class:`StdLogic` and :class:`X01Z`;
    supporting all the same operations, but only the values ``0`` and ``1``.
    Similar to ``bit`` from VHDL or Verilog, or :py:class:`bool`.
    """

    __values__ = [_0, _1]


_literal_repr: Dict[str, int] = {
    "U": _U,
    "u": _U,
    "X": _X,
    "x": _X,
    "0": _0,
    "1": _1,
    "Z": _Z,
    "z": _Z,
    "L": _L,
    "l": _L,
    "H": _H,
    "h": _H,
    "W": _W,
    "w": _W,
    "-": __,
}

_and_table = (
    ("U", "U", "0", "U", "U", "U", "0", "U", "U"),  # U
    ("U", "X", "0", "X", "X", "X", "0", "X", "X"),  # X
    ("0", "0", "0", "0", "0", "0", "0", "0", "0"),  # 0
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # 1
    ("U", "X", "0", "X", "X", "X", "0", "X", "X"),  # Z
    ("U", "X", "0", "X", "X", "X", "0", "X", "X"),  # W
    ("0", "0", "0", "0", "0", "0", "0", "0", "0"),  # L
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # H
    ("U", "X", "0", "X", "X", "X", "0", "X", "X"),  # -
)
#     U    X    0    1    Z    W    L    H    -

_or_table = (
    ("U", "U", "U", "1", "U", "U", "U", "1", "U"),  # U
    ("U", "X", "X", "1", "X", "X", "X", "1", "X"),  # X
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # 0
    ("1", "1", "1", "1", "1", "1", "1", "1", "1"),  # 1
    ("U", "X", "X", "1", "X", "X", "X", "1", "X"),  # Z
    ("U", "X", "X", "1", "X", "X", "X", "1", "X"),  # W
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # L
    ("1", "1", "1", "1", "1", "1", "1", "1", "1"),  # H
    ("U", "X", "X", "1", "X", "X", "X", "1", "X"),  # -
)
#     U    X    0    1    Z    W    L    H    -

_xor_table = (
    ("U", "U", "U", "U", "U", "U", "U", "U", "U"),  # U
    ("U", "X", "X", "X", "X", "X", "X", "X", "X"),  # X
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # 0
    ("U", "X", "1", "0", "X", "X", "1", "0", "X"),  # 1
    ("U", "X", "X", "X", "X", "X", "X", "X", "X"),  # Z
    ("U", "X", "X", "X", "X", "X", "X", "X", "X"),  # W
    ("U", "X", "0", "1", "X", "X", "0", "1", "X"),  # L
    ("U", "X", "1", "0", "X", "X", "1", "0", "X"),  # H
    ("U", "X", "X", "X", "X", "X", "X", "X", "X"),  # -
)
#     U    X    0    1    Z    W    L    H    -

_not_table = ("U", "X", "1", "0", "X", "X", "1", "0", "X")
#              U    X    0    1    Z    W    L    H    -

_str_table = ("U", "X", "0", "1", "Z", "W", "L", "H", "-")
#              U    X    0    1    Z    W    L    H    -
