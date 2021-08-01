from functools import lru_cache
from typing import TYPE_CHECKING, Dict, Optional, Type, TypeVar, Union, cast

from hdltypes.types import Logic

LogicLiteralT = Union[str, int, bool]
LogicConstructibleT = Union[LogicLiteralT, "StdLogic"]

Self = TypeVar("Self", bound="StdLogic")


# DEFINING SUBTYPES OF STDLOGIC
#
# A subtype must inherit from StdLogic, or a known subclass of StdLogic.
# The subtype will define a `__values__` class attribute that is a non-empty list of
# the StdLogic value representations listed directly below. The first element of that
# list will be used as the default value.


_U = 0
_X = 1
_0 = 2
_1 = 3
_Z = 4
_W = 5
_L = 6
_H = 7
__ = 8


class StdLogic(Logic):
    """
    A 9-value logic type

    The value and semantics of this type are defined in IEEE 1164 and are similar to the
    ``std_ulogic`` type in VHDL. The values of this types are: ``U``, ``X``, ``0``,
    ``1``, ``Z``, ``W``, ``L``, ``H``, and ``-``.

    StdLogics are convertible to and from :py:class:`str`, :py:class:`bool`,
    :py:class:`int`, and subtypes of :class:`StdLogic`.
    Permissible convertible values include: ``0``, ``1``, ``False``, ``True``, ``"U"``,
    ``"X"``, ``"0"``, ``"1"``, ``"Z"``, ``"W"``, ``"L"``, ``"H"``, ``"-"``, and all
    lowercase versions of the strings.
    The default value is ``U``.

    .. code-block:: python3

        >>> StdLogic(False)  # construct from bool
        StdLogic('0')

        >>> StdLogic(False)  # construct from int
        StdLogic('0')

        >>> StdLogic("z")  # construct from (lowercase) str
        StdLogic('Z')

        >>> str(StdLogic("z"))  # cast to str (always uppercase)
        'Z'

        >>> bool(StdLogic(1))  # cast to bool
        True

        >>> int(StdLogic(0))  # cast to int
        0

        >>> StdLogic(X01Z("Z"))  # convert subtype
        StdLogic('Z')

        >>> StdLogic()  # defaults to "U"
        StdLogic('U')

    .. note::
        Attempting to cast a StdLogic value that is not ``0`` or ``1`` to an
        :py:class:`int` or :py:class:`bool` will result in a :exc:`ValueError`.

    StdLogics support logical operations ``&``, ``|``, ``^``, and ``~``;
    and can be used in logical operations with subtypes,
    which will return the widest of the two types.

    .. code-block:: python3

        >>> StdLogic(0) | StdLogic("X")
        StdLogic('X')

        >>> Bit(0) ^ StdLogic("1")
        StdLogic('1')

        >>> ~StdLogic("L")
        StdLogic('1')

    StdLogic supports creating subtypes (like :class:`X01Z` and :class:`Bit`);
    see implementation for more details.
    Values of a subtype of StdLogic will hash the same and equate, so that they behave
    as proper subtypes.
    This results in what may seem like atypical behavior, but it is type-safe.

    .. code-block:: python3

        >>> StdLogic(0) == Bit(0)  # subtypes equate
        True

        >>> a = {StdLogic(0)}
        >>> Bit(0) in a        # subtypes are substitutable in hashed collections
        True

        >>> isinstance(Bit(0), StdLogic)  # subtypes pass isinstance checks
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
        return cast(Self, self)

    def __new__(cls: Type[Self], value: Optional[LogicConstructibleT] = None) -> Self:
        _repr: Optional[int]
        if value is None:
            # default
            return cls._make(cls.__values__[0])
        elif value in _literal_repr:
            # convert literal
            _repr = _literal_repr[cast(LogicLiteralT, value)]
        elif isinstance(value, StdLogic):
            # convert subtype
            _repr = value._repr
        else:
            # type error
            _repr = None
        if _repr is None or _repr not in cls.__values__:
            raise ValueError(
                f"{value!r} is not constructible into a {cls.__qualname__}"
            )
        return cls._make(_repr)

    if not TYPE_CHECKING:
        # mypy doesn't like using lru_cache on __new__
        __new__ = lru_cache(maxsize=None)(__new__)

    def __int__(self) -> int:
        if self._repr == _0:
            return 0
        elif self._repr == _1:
            return 1
        raise ValueError(f"Can convert non-0/1 value {self!r} to int")

    def __bool__(self) -> int:
        if self._repr == _0:
            return False
        elif self._repr == _1:
            return True
        raise ValueError(f"Can convert non-0/1 value {self!r} to bool")

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
    supporting all the same operations, but only the values ``X``, ``0``, ``1``, and
    ``Z``.
    The default value is ``X``.
    Similar to ``X01Z`` from VHDL, or ``logic`` from Verilog.
    """

    __values__ = [_X, _0, _1, _Z]


class Bit(X01Z):
    """
    A 2-value logic type

    A subtype of :class:`StdLogic` and :class:`X01Z`;
    supporting all the same operations, but only the values ``0`` and ``1``.
    The default value is ``0``.
    Similar to ``bit`` from VHDL or Verilog, or :py:class:`bool`.
    """

    __values__ = [_0, _1]


_literal_repr: Dict[LogicLiteralT, int] = {
    "U": _U,
    "u": _U,
    "X": _X,
    "x": _X,
    0: _0,
    "0": _0,
    1: _1,
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
