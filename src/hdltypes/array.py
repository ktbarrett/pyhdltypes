from itertools import chain
from typing import Iterable, Optional, TypeVar, Union, cast, overload

from hdltypes.range import Range
from hdltypes.types import AbstractArray

T = TypeVar("T")
Self = TypeVar("Self", bound="Array[object]")


class Array(AbstractArray[T]):
    """
    Type-generic fixed-length mutable Array type
    """

    def __init__(self, value: Iterable[T], range: Optional[Range] = None) -> None:
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
    def __getitem__(self: Self, item: int) -> T:
        ...

    @overload
    def __getitem__(self: Self, item: slice) -> Self:
        ...

    def __getitem__(self: Self, item: Union[int, slice]) -> Union[T, Self]:
        if isinstance(item, int):
            return cast(T, self._value[self._index(item)])
        elif isinstance(item, slice):
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify the step in the index")
            left_idx = self._index(left)
            right_idx = self._index(right)
            return type(self)(
                self._value[left_idx:right_idx], Range(left, self.direction, right)
            )
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

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
            self._value[self._index(item)] = cast(T, value)
        elif isinstance(item, slice):
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            if item.step is not None:
                raise ValueError("do not specify the step in the index")
            left_idx = self._index(left)
            right_idx = self._index(right)
            value = tuple(cast(Iterable[T], value))
            if len(value) != len(range(left_idx, right_idx)):
                raise ValueError(
                    f"cannot value of length {len(value)} in slice [{left}:{right}]"
                )
            self._value[left_idx:right_idx] = value
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

    def concat(self: Self, other: Self) -> Self:
        """
        Concatenates two arrays
        """
        if isinstance(other, type(self)):
            return type(self)(chain(self, other))
        else:
            raise TypeError(
                f"Cannot concatenate {type(self).__qualname__!r} object and {type(other).__qualname__!r} object"
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._value == other._value
        else:
            return NotImplemented

    __hash__: None  # type: ignore

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({self._value!r}, {self._range!r})"

    def _index(self, index: int) -> int:
        try:
            return self.range.index(index)
        except ValueError:
            raise IndexError(f"index {index} out of range {self.range}") from None
