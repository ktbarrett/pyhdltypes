from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

Self = TypeVar("Self")


@runtime_checkable
class Logic(Protocol):
    """ """

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
