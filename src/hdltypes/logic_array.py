from typing import Iterable, Optional, Type, TypeVar, Union, cast, overload

from hdltypes.array import Array
from hdltypes.logic import X01Z, Bit, LogicConstructibleT, StdLogic
from hdltypes.range import Range
from hdltypes.types import AbstractConstArray

LogicArrayConstructibleT = Union[str, Iterable[LogicConstructibleT]]
LogicT = TypeVar("LogicT", bound=StdLogic)
Self = TypeVar("Self", bound="LogicArrayBase[StdLogic]")


class LogicArrayBase(Array[LogicT]):
    """ """

    _element_type: Type[LogicT]  # change to ClassVar (python/mypy#5144)

    def __init__(
        self, value: LogicArrayConstructibleT, range: Optional[Range] = None
    ) -> None:
        element_type = type(self)._element_type
        super().__init__(value=(element_type(v) for v in value), range=range)

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

    def __and__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        if isinstance(other, AbstractConstArray):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a & b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __rand__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        return self & other

    def __or__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        if isinstance(other, AbstractConstArray):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a | b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __ror__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        return self | other

    def __xor__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        if isinstance(other, AbstractConstArray):
            if len(self) != len(other):
                raise ValueError("Can't combine arrays of different length")
            else:
                return type(self)(a ^ b for a, b in zip(self, other))  # type: ignore
        else:
            return NotImplemented

    def __rxor__(self: Self, other: AbstractConstArray[LogicT]) -> Self:
        return self ^ other

    def __invert__(self: Self) -> Self:
        return type(self)(~v for v in self)

    def __repr__(self) -> str:
        value_str = "".join(str(v) for v in self)
        return f"{type(self).__qualname__}({value_str!r}, {self._range!r})"


class StdLogicArray(LogicArrayBase[StdLogic]):
    _element_type = StdLogic


class X01ZArray(LogicArrayBase[X01Z]):
    _element_type = X01Z


class BitArray(LogicArrayBase[Bit]):
    _element_type = Bit
