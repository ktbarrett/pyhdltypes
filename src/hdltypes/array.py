from itertools import chain
from typing import Iterable, Optional, TypeVar, Union, cast, overload

from hdltypes.range import Range
from hdltypes.types import AbstractArray, AbstractConstArray

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
Self = TypeVar("Self", bound="ConstArray[object]")


class ConstArray(AbstractConstArray[T_co]):
    """
    Immutable version of :class:`~hdltypes.array.Array`.
    """

    def __init__(self, value: Iterable[T_co], range: Optional[Range] = None) -> None:
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
    def __getitem__(self: Self, item: int) -> T_co:
        ...

    @overload
    def __getitem__(self: Self, item: slice) -> Self:
        ...

    def __getitem__(self: Self, item: Union[int, slice]) -> Union[T_co, Self]:
        if isinstance(item, int):
            return cast(T_co, self._value[self._index(item)])
        elif isinstance(item, slice):
            if item.step is not None:
                raise IndexError("do not specify the step in the index")
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            range = Range(left, self.direction, right)
            if len(range) == 0:
                raise IndexError(
                    f"slice '[{left}:{right}]' direction does not match array direction {self.direction!r}"
                )
            left_idx = self._index(left)
            right_idx = self._index(right)
            return type(self)(
                value=self._value[left_idx : right_idx + 1],
                range=range,
            )
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

    def __add__(self: Self, other: Self) -> Self:
        if isinstance(other, type(self)):
            return type(self)(chain(self, other))
        else:
            return NotImplemented

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


class Array(ConstArray[T], AbstractArray[T]):
    r"""
    Type-generic fixed-length mutable sequence type.

    Arrays are capable of holding any type.
    Like :py:class:`list` and :py:class:`tuple`, they are initialized with any :py:term:`iterable`.

    .. code-block:: python3

        >>> Array([123, 456])
        Array([123, 456], Range(0, 'to', 1))
        >>> Array("abc")
        Array(['a', 'b', 'c'], Range(0, 'to', 2))

    Unlike :py:class:`list` and :py:class:`tuple`, arrays can use arbitrary indexing scheme;
    not just 0 to length-1.
    The indexing scheme is described using a :class:`~hdltypes.range.Range`.
    The left most index of the array is the first value of the range.
    The right most index of the array is the last value of the range.
    If no range is given, it is defaulted to ``Range(0, 'to', len(value) - 1)``.

    .. code-block:: python3

        >>> a = Array("abcd", Range(4, "downto", 1))
        >>> a[4]
        'a'
        >>> a[1]
        'd'

    Slicing an array returns a new array with the specified indexes.
    Right bounds in slices are inclusive, just like ranges.
    If no left bound is given, it is assumed to be the left-most index.
    If no right bound is give, it is assumed to be the right-most index.

    .. code-block:: python3

        >>> a = Array([0, 1, 2, "a", "b", "c"])
        >>> a[2:4]
        Array([2, 'a', 'b'], Range(2, 'to', 4))
        >>> a[:2]
        Array([0, 1, 2], Range(0, 'to', 2))
        >>> a[5:]
        Array(['c'], Range(5, 'to', 5))

    Arrays have a fixed size once created, but the elements of the array can be changed.
    Setting a slice requires the new value be an iterable with the same length as the slice.

    .. code-block:: python3

        >>> a = Array("abcd", Range(4, "downto", 1))
        >>> a[2] = 8
        >>> a
        Array(['a', 'b', 8, 'd'], Range(4, 'downto', 1))
        >>> a[:] = [1, 2, 3, 4]
        >>> a
        Array([1, 2, 3, 4], Range(4, 'downto', 1))

    Arrays are a lot like Python's :class:`list` type and support many of the same operations,
    including: :py:func:`len`, iteration, reverse iteration, and testing a value for inclusion in the array, equality,
    and more.

    .. code-block:: python3

        >>> a = Array("1234")
        >>> len(a)
        4
        >>> list(a)
        ['1', '2', '3', '4']
        >>> a[:] = reversed(a)
        >>> a
        Array(['4', '3', '2', '1'], Range(0, 'to', 3))
        >>> '3' in a
        True
        >>> Array("123") == Array("123", Range(2, 'downto', 0))  # range doesn't matter for equality
        True

    Arrays support concatenation with other arrays.

    .. code-block:: python3

        >>> Array("123") + Array("456")
        Array(['1', '2', '3', '4', '5', '6'], Range(0, 'to', 5))

    .. warning::
        Arrays are not :py:term:`sequence`\ s because they do not assume 0-based indexing.
        Beware passing arrays to any function that take sequences.

    Args:
        * value: any iterable to initialize the array.
        * range: the indexing scheme to use with the array, defaults to ``Range(0, 'to', len(value) - 1)``.
    """

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
            if item.step is not None:
                raise IndexError("do not specify the step in the index")
            left = item.start if item.start is not None else self.left
            right = item.stop if item.stop is not None else self.right
            range = Range(left, self.direction, right)
            value = tuple(cast(Iterable[T], value))
            if len(range) == 0:
                raise IndexError(
                    f"slice '[{left}:{right}]' direction does not match array direction {self.direction!r}"
                )
            if len(value) != len(range):
                raise ValueError(
                    f"cannot fit value of length {len(value)} in slice [{left}:{right}]"
                )
            left_idx = self._index(left)
            right_idx = self._index(right)
            self._value[left_idx : right_idx + 1] = value
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )
