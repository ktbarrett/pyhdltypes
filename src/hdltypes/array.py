from typing import Iterable, Optional, Union, cast, overload

from hdltypes.range import Range
from hdltypes.types import Array, MutableArray, Self, T, T_co


class FrozenGArray(Array[T_co]):
    """ """

    def __init__(self, value: Iterable[T_co], range: Optional[Range] = None) -> None:
        super().__init__()
        self._value = list(value)
        if range is None:
            self._range = Range(0, "to", len(self._value) - 1)
        elif len(range) != len(self._value):
            raise ValueError(
                f"value of length {len(self._value)} does not fit in {range!r}"
            )
        else:
            self._range = range

    @property
    def range(self) -> Range:
        return self._range

    @range.setter
    def range(self, new_range: Range) -> None:
        if len(new_range) != len(self):
            raise ValueError(
                f"{new_range!r} is not the same size as the array ({len(self)})"
            )
        self._range = new_range

    @overload
    def __getitem__(self, item: int) -> T_co:
        ...

    @overload
    def __getitem__(self: Self, item: slice) -> "FrozenGArray[T_co]":
        ...

    def __getitem__(self, item):  # type: ignore
        if isinstance(item, int):
            idx = self._index(item)
            return self._value[idx]
        elif isinstance(item, slice):
            start = item.start if item.start is not None else self.left
            stop = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify step")
            start_idx = self._index(start)
            stop_idx = self._index(stop)
            step = self.range.to_range().step
            value = self._value[start_idx : (stop_idx + step) : step]
            range = Range(start, self.direction, stop)
            return type(self)(value=value, range=range)
        else:
            raise TypeError(
                f"indices must be integers or slices, not {type(item).__qualname__}"
            )

    def _index(self, idx: int) -> int:
        try:
            return self.range.index(idx)
        except ValueError:
            raise IndexError(f"{idx!r} not in {self.range!r}") from None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._value == other._value
        return NotImplemented

    __hash__: None  # type: ignore

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({self._value!r}, {self.range!r})"


class GArray(FrozenGArray[T], MutableArray[T]):
    """ """

    @overload
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:
        ...

    def __setitem__(
        self, item: Union[int, slice], value: Union[T, Iterable[T]]
    ) -> None:
        if isinstance(item, int):
            idx = self._index(item)
            self._value[idx] = cast(T, value)
        elif isinstance(item, slice):
            start = item.start if item.start is not None else self.left
            stop = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify step")
            start_idx = self._index(start)
            stop_idx = self._index(stop)
            step = self.range.to_range().step
            _value = list(cast(Iterable[T], value))
            if len(_value) != len(range(start_idx, (stop_idx + step), step)):
                raise ValueError(
                    f"value of length {len(_value)} "
                    f"will not fit in slice [{start}:{stop}]"
                )
            self._value[start_idx : (stop_idx + step) : step] = _value
        else:
            raise TypeError(
                f"indices must be integers or slices, not {type(item).__qualname__}"
            )
