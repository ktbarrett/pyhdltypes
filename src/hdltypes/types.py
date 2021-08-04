from abc import abstractmethod, abstractproperty
from typing import (
    Collection,
    Iterable,
    Iterator,
    Optional,
    Reversible,
    TypeVar,
    overload,
)

from hdltypes.compat import Protocol, runtime_checkable
from hdltypes.range import Range

Self = TypeVar("Self")
T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")


@runtime_checkable
class Logic(Protocol):
    """
    Protocol for a type that supports logical operations

    A type that implements this protocol supports the logical binary operators:
    ``&``, ``|``, ``^``, symmetrically with another value of the same type or a subtype;
    and the ``~`` unary operator.
    """

    @abstractmethod
    def __and__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rand__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __or__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __ror__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __xor__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rxor__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __invert__(self: Self) -> Self:
        ...


@runtime_checkable
class Array(Reversible[T_co], Collection[T_co], Protocol):
    r"""
    Like a Sequence, but uses a Range to describe a non-0-based indexing scheme

    Similar to the builtin protocol :py:class:`~collections.abc.Sequence`.
    It has the same interface in general, including the mixins :meth:`count` and
    :meth:`index`.
    However, Sequences assume 0-based indexing;
    while Arrays support using :class:`~hdltypes.range.Range`\ s to describe the
    indexing scheme.

    .. code-block:: python3

        a: Array[str] = GArray("1234", Range(3, 'downto', 0))
        a.left   # leftmost index is 3, per the Range object above
        a.right  # rightmost index is 0, per the Range object above
        a[3]     # using the index '3' to get the leftmost element in the Array

    This protocol can be used as an :py:term:`abstract base class`.
    First, inherit from :class:`~hdltypes.types.Array`;
    then, fill in an implementation for :attr:`__getitem__` and :attr:`range`.

    See :class:`MutableArray` for a variant of this protocol that supports mutation.
    """

    @abstractproperty  # mypy does not like stacking abstract and property decorators
    def range(self) -> Range:
        """Returns a :class:`~hdltypes.range.Range` describing the indexing scheme"""
        ...

    @range.setter
    def range(self, __range: Range) -> None:
        ...

    @property
    def left(self) -> int:
        """The leftmost index in the array"""
        return self.range.left

    @property
    def direction(self) -> str:
        """The direction of the indexes, either ``'to'`` or ``'downto'``"""
        return self.range.direction

    @property
    def right(self) -> int:
        """The rightmost index in the array"""
        return self.range.right

    def __len__(self) -> int:
        return len(self.range)

    @overload
    def __getitem__(self, item: int) -> T_co:
        ...

    @overload
    def __getitem__(self, item: slice) -> "Array[T_co]":
        ...

    @abstractmethod
    def __getitem__(self, item):  # type: ignore
        ...

    def __iter__(self) -> Iterator[T_co]:
        for i in self.range:
            yield self[i]

    def __reversed__(self) -> Iterator[T_co]:
        for i in reversed(self.range):
            yield self[i]

    def __contains__(self, value: object) -> bool:
        for v in self:
            if v == value:
                return True
        return False

    def index(
        self,
        value: object,
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> int:
        """
        Returns the first index of *value*

        Args:
            value: the value to search for
            start: the first index to search
            stop: the last index (inclusive) to search

        Raises:
            IndexError: if the value is not present in the array
        """
        if start is None:
            start = self.left
        if stop is None:
            stop = self.right
        for i in Range(start, self.direction, stop):
            if self[i] == value:
                return i
        raise IndexError(f"{value} is not in array")

    def count(self, value: object) -> int:
        """Returns the number of occurences of *value* in the array"""
        c = 0
        for v in self:
            if v == value:
                c += 1
        return c


@runtime_checkable
class MutableArray(Array[T], Protocol):
    """
    A mutable variant of Array and allows element assignment

    Add to :class:`Array` the ability to mutate elements in the Array.
    Unlike :py:class:`~collections.abc.MutableSequence`,
    changing the size of the Array is not allowed.

    See :class:`Array` for a protocol that does not support mutation.
    """

    @overload
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:
        ...

    @abstractmethod
    def __setitem__(self, item, value):  # type: ignore
        ...
