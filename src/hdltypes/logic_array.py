from itertools import chain
from typing import Iterable, Optional, TypeVar, Union, cast, overload

from hdltypes.logic import X01Z, Bit, LogicConstructibleT, StdLogic
from hdltypes.range import Range
from hdltypes.types import AbstractArray, AbstractConstArray

LogicT = TypeVar("LogicT", bound=StdLogic)
LogicT_co = TypeVar("LogicT_co", covariant=True, bound=StdLogic)


class _ConstLogicArray(AbstractConstArray[LogicT_co]):
    """ """

    def __init__(
        self, value: Iterable[LogicT_co], range: Optional[Range] = None
    ) -> None:
        self._value = list(value)
        if range is None:
            self._range = Range(0, "to", len(self._value) - 1)
        else:
            self._range = range
            if len(self._value) != len(self._range):
                raise ValueError(
                    f"value of length {len(self._value)} does not fit in {self._range!r}"
                )

    @property
    def range(self) -> Range:
        return self._range

    @overload
    def __getitem__(self, item: int) -> LogicT_co:
        ...

    @overload
    def __getitem__(self, item: slice) -> "LogicArray[LogicT_co]":
        ...

    def __getitem__(
        self, item: Union[int, slice]
    ) -> Union[StdLogic, "LogicArray[LogicT_co]"]:
        if isinstance(item, int):
            return self._value[self._index(item)]
        elif isinstance(item, slice):
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify the step in the index")
            left_idx = self._index(left)
            right_idx = self._index(right)
            return LogicArray[LogicT_co](
                self._value[left_idx:right_idx], Range(left, self.direction, right)
            )
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

    def __and__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        if not isinstance(other, _ConstLogicArray):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("Can't combine arrays of different length")
        return LogicArray[LogicT_co](a & b for a, b in zip(self, other))

    def __rand__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        ...

    def __or__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        if not isinstance(other, _ConstLogicArray):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("Can't combine arrays of different length")
        return LogicArray[LogicT_co](a | b for a, b in zip(self, other))

    def __ror__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        ...

    def __xor__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        if not isinstance(other, type(self)):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("Can't combine arrays of different length")
        return LogicArray[LogicT_co](a ^ b for a, b in zip(self, other))

    def __rxor__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        ...

    def __invert__(self) -> "LogicArray[LogicT_co]":
        return LogicArray[LogicT_co](~v for v in self)

    def __add__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        if not isinstance(other, _ConstLogicArray):
            return NotImplemented
        return LogicArray[LogicT_co](chain(self, other))

    def __radd__(self, other: "_ConstLogicArray[LogicT_co]") -> "LogicArray[LogicT_co]":
        ...

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._value == other._value
        return NotImplemented

    __hash__: None  # type: ignore

    def __repr__(self) -> str:
        value = "".join(str(v) for v in self)
        return f"{type(self).__qualname__}({value!r}, {self.range!r})"

    def _index(self, index: int) -> int:
        try:
            return self.range.index(index)
        except ValueError:
            raise IndexError(f"index {index} out of range {self.range}") from None


class LogicArray(_ConstLogicArray[LogicT], AbstractArray[LogicT]):
    """ """

    @overload
    def __setitem__(self, item: int, value: LogicT) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[LogicT]) -> None:
        ...

    def __setitem__(
        self,
        item: Union[int, slice],
        value: Union[LogicT, Iterable[LogicT]],
    ) -> None:
        if isinstance(item, int):
            self._value[self._index(item)] = cast(LogicT, value)
        elif isinstance(item, slice):
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify the step in the index")
            left_idx = self._index(left)
            right_idx = self._index(right)
            value_as_logic = tuple(cast(Iterable[LogicT], value))
            if len(value_as_logic) != len(range(left_idx, right_idx)):
                raise ValueError(
                    f"cannot value of length {len(value_as_logic)} in slice [{left}:{right}]"
                )
            self._value[left_idx:right_idx] = value_as_logic
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )


def StdLogicArray(
    value: Iterable[LogicConstructibleT], range: Optional[Range] = None
) -> LogicArray[StdLogic]:
    return LogicArray[StdLogic](value=(StdLogic(v) for v in value), range=range)


def X01ZArray(
    value: Iterable[LogicConstructibleT], range: Optional[Range] = None
) -> LogicArray[X01Z]:
    return LogicArray[X01Z](value=(X01Z(v) for v in value), range=range)


def BitArray(
    value: Iterable[LogicConstructibleT], range: Optional[Range] = None
) -> LogicArray[Bit]:
    return LogicArray[Bit](value=(Bit(v) for v in value), range=range)
