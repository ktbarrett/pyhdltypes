from itertools import chain
from typing import Iterable, Optional, Type, TypeVar, Union, cast, overload

from hdltypes.array import Array, ConstArray
from hdltypes.logic import X01Z, Bit, LogicConstructibleT, StdLogic
from hdltypes.range import Range

LogicArrayConstructibleT = Union[str, Iterable[StdLogic]]
LogicT = TypeVar("LogicT", bound=StdLogic)
LogicT_co = TypeVar("LogicT_co", bound=StdLogic, covariant=True)
Self = TypeVar("Self", bound="ConstLogicArrayBase[StdLogic]")


# DEFINING SUBTYPES OF LOGICARRAYBASE
#
# A subtype must inherit from LogicArrayBase and use a StdLogic subtype as a type argument.
# The _element_type class attribute must be filled in with the same subtype.
# Finally, you must register the new array type as a virtual subtype of the parent concrete LogicArray specialization
# Meaning if you make a new StdLogic subtype UX01Z you must run `StdLogicArray.register(UX01ZArray)`.
# It's confusing, but it's necessary to make both mypy and runtime happy.
#
# Addendum: you can also make existing types act as subtypes at runtime using ABC.register, but mypy does not like it.
# For example: After following the above examples you can run `UX01ZArray.register(X01ZArray)` so that X01ZArray acts
# as a subtype of UX01ZArray.


class ConstLogicArrayBase(ConstArray[LogicT_co]):
    """
    Immutable version of :class:`~hdltypes.logic_array.LogicArrayBase`.
    """

    _element_type: Type[LogicT_co]  # change to ClassVar (python/mypy#5144)

    def __init__(
        self, value: LogicArrayConstructibleT, range: Optional[Range] = None
    ) -> None:
        element_type = type(self)._element_type
        super().__init__(value=(element_type(v) for v in value), range=range)

    def __and__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        if isinstance(other, type(self)):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a & b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __rand__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        return self & other

    def __or__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        if isinstance(other, type(self)):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a | b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __ror__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        return self | other

    def __xor__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        if isinstance(other, type(self)):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a ^ b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __rxor__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        return self ^ other

    def __invert__(self: Self) -> Self:
        return type(self)(~v for v in self)

    def __add__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        if isinstance(other, type(self)):
            return type(self)(chain(self, other))
        else:
            return NotImplemented

    def __radd__(self: Self, other: "ConstLogicArrayBase[LogicT_co]") -> Self:
        if isinstance(other, type(self)):
            return type(self)(chain(other, self))
        else:
            return NotImplemented

    def __repr__(self) -> str:
        value_str = "".join(str(v) for v in self)
        return f"{type(self).__qualname__}({value_str!r}, {self._range!r})"


class LogicArrayBase(ConstLogicArrayBase[LogicT], Array[LogicT]):
    """
    Generic Array of StdLogic which supports bitwise logic operators.

    This class is a partial specialization of :class:`~hdltypes.array.Array` limiting the element type to subtypes of
    :class:`~hdltypes.logic.StdLogic`.
    This specialization adds support for bitwise logical operators between two arrays,
    and construction from literals on construction and when setting indexes.

    .. code-block:: python3

        >>> a = StdLogicArray("01XZ")
        >>> a
        StdLogicArray('01XZ', Range(0, 'to', 3))
        >>> a & StdLogicArray("1101")
        StdLogicArray('010X', Range(0, 'to', 3))

    Bitwise logical operators and concatenation between logical subtypes is also supported,
    which will return the widest of the two types.

    .. code-block:: python3

        >>> StdLogicArray("01XZ") | BitArray("1101")
        StdLogicArray('11X1', Range(0, 'to', 3))

    This type cannot be directly used, use the concrete specializations: :class:`~hdltypes.logic_array.StdLogicArray`,
    :class:`~hdltypes.logic_array.X01ZArray` and :class:`~hdltypes.logic_array.BitArray`.
    Creating additional subtypes is supported; see the module file for details.
    """

    @overload
    def __setitem__(self, item: int, value: LogicConstructibleT) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: LogicArrayConstructibleT) -> None:
        ...

    def __setitem__(
        self,
        item: Union[int, slice],
        value: Union[LogicConstructibleT, LogicArrayConstructibleT],
    ) -> None:
        element_type = type(self)._element_type
        if isinstance(item, int):
            super().__setitem__(item, element_type(cast(LogicConstructibleT, value)))
        elif isinstance(item, slice):
            super().__setitem__(
                item, (element_type(v) for v in cast(LogicArrayConstructibleT, value))
            )
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )


class StdLogicArray(LogicArrayBase[StdLogic]):
    _element_type = StdLogic


class X01ZArray(LogicArrayBase[X01Z]):
    _element_type = X01Z


StdLogicArray.register(X01ZArray)


class BitArray(LogicArrayBase[Bit]):
    _element_type = Bit


X01ZArray.register(BitArray)
