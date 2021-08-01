from abc import abstractmethod
from typing import TypeVar

from hdltypes.compat import Protocol, runtime_checkable

Self = TypeVar("Self")


@runtime_checkable
class Logic(Protocol):
    """
    Protocol for a type that supports logical operations

    A type that implements this :py:class:`~typing.Protocol` supports the logical binary
    operators:
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
