from abc import abstractmethod, abstractproperty
from typing import (
    Collection,
    Iterable,
    Iterator,
    Protocol,
    Reversible,
    TypeVar,
    overload,
    runtime_checkable,
)

from hdltypes.range import Range

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
Self = TypeVar("Self")


@runtime_checkable
class AbstractConstArray(Collection[T_co], Reversible[T_co], Protocol):
    """
    A fixed-length Sequence-like type that uses a Range as an indexing scheme
    """

    @abstractproperty
    def range(self) -> Range:
        ...

    @property
    def left(self) -> int:
        return self.range.left

    @property
    def right(self) -> int:
        return self.range.right

    @property
    def direction(self) -> str:
        return self.range.direction

    def __len__(self) -> int:
        return len(self.range)

    def __iter__(self) -> Iterator[T_co]:
        for idx in self.range:
            yield self[idx]

    def __reversed__(self) -> Iterator[T_co]:
        for idx in reversed(self.range):
            yield self[idx]

    def __contains__(self, value: object) -> bool:
        for v in self:
            if v == value:
                return True
        return False

    @overload
    @abstractmethod
    def __getitem__(self, item: int) -> T_co:
        ...

    @overload
    @abstractmethod
    def __getitem__(self, item: slice) -> "AbstractConstArray[T_co]":
        ...


@runtime_checkable
class AbstractArray(AbstractConstArray[T], Protocol):
    """
    A mutable version of Array
    """

    @overload
    @abstractmethod
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @overload
    @abstractmethod
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:
        ...


@runtime_checkable
class Number(Protocol):
    """
    A number type

    Specifically designed to allow writing generic functions that work with both
    :py:class:`int`, :py::class:`float`, :class:`Unsigned`, :class:`Signed`,
    :class:`Ufixed`, :class:`Sfixed`, or :class:`Float`.
    """

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...

    @abstractmethod
    def __lt__(self: Self, other: Self) -> bool:
        ...

    @abstractmethod
    def __le__(self: Self, other: Self) -> bool:
        ...

    @abstractmethod
    def __gt__(self: Self, other: Self) -> bool:
        ...

    @abstractmethod
    def __ge__(self: Self, other: Self) -> bool:
        ...

    @abstractmethod
    def __neg__(self: Self) -> Self:
        ...

    @abstractmethod
    def __pos__(self: Self) -> Self:
        ...

    @abstractmethod
    def __abs__(self: Self) -> Self:
        ...

    @abstractmethod
    def __add__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __radd__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __sub__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rsub__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __mul__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rmul__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __truediv__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rtruediv__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __floordiv__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rfloordiv__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __mod__(self: Self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rmod__(self: Self, other: Self) -> Self:
        ...


@runtime_checkable
class Integer(Number, Protocol):
    r"""
    A integer type

    Integers are :class:`Number`\ s that support bitwise logical operators and shifting.
    Specifically designed to allow writing generic functions that work with
    :py:class:`int`, :class:`Unsigned`, and :class:`Signed`.
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

    @abstractmethod
    def __rshift__(self: Self, amt: int) -> Self:
        ...

    @abstractmethod
    def __lshift__(self: Self, amt: int) -> Self:
        ...