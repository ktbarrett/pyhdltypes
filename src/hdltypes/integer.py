from typing import Iterable, Optional, TypeVar, Union, cast, overload

from hdltypes.logic import Bit, LogicConstructibleT
from hdltypes.logic_array import BitArray
from hdltypes.range import Range
from hdltypes.types import AbstractArray, Integer

UnsignedT = TypeVar("UnsignedT", bound="Unsigned")


class Unsigned(AbstractArray[Bit], Integer):
    """ """

    def __init__(
        self,
        value: Union[int, Iterable[LogicConstructibleT]],
        range: Optional[Range] = None,
    ) -> None:
        if isinstance(value, int):
            length = _min_bit_length(value)
            if range is None:
                self._value = _signed_to_unsigned(value, length)
                self._range = Range(length - 1, "downto", 0)
            else:
                self._value = _signed_to_unsigned(value, len(range))
                self._range = range
                if len(self._range) < length:
                    raise ValueError(
                        f"value with minimum bit length {length} cannot fit in {range}"
                    )
        else:
            bits = [int(Bit(v)) for v in value]
            self._value = sum(v << i for i, v in enumerate(reversed(bits)))
            if range is None:
                self._range = Range(len(bits) - 1, "downto", 0)
            else:
                self._range = range
                if len(self._range) < len(bits):
                    raise ValueError(f"value of length {length} does fit in {range}")

    @property
    def range(self) -> Range:
        return self._range

    @overload
    def __getitem__(self, item: int) -> Bit:
        ...

    @overload
    def __getitem__(self, item: slice) -> BitArray:
        ...

    def __getitem__(self, item: Union[int, slice]) -> Union[Bit, BitArray]:
        if isinstance(item, int):
            idx = self._index(item)
            return Bit((self._value >> idx) & 1)
        elif isinstance(item, slice):
            raise NotImplementedError
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

    @overload
    def __setitem__(self, item: int, value: LogicConstructibleT) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[LogicConstructibleT]) -> None:
        ...

    def __setitem__(
        self,
        item: Union[int, slice],
        value: Union[LogicConstructibleT, Iterable[LogicConstructibleT]],
    ) -> None:
        if isinstance(item, int):
            idx = self._index(item)
            bit_val = int(Bit(cast(LogicConstructibleT, value)))
            mask = ((1 << len(self)) - 1) ^ (1 << idx)
            self._value = (self._value & mask) | (bit_val << idx)
        elif isinstance(item, slice):
            raise NotImplementedError
        else:
            raise TypeError(
                f"expected index to be of type int or slice, not {type(item).__qualname__}"
            )

    def resize(self, new_size: int) -> "Unsigned":
        mask = (1 << new_size) - 1
        return Unsigned(self._value & mask, Range(new_size - 1, "downto", 0))

    def __eq__(self: UnsignedT, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return self._value == cast(UnsignedT, other)._value

    def __lt__(self, other: "Unsigned") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value < other._value

    def __le__(self, other: "Unsigned") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value <= other._value

    def __gt__(self, other: "Unsigned") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value > other._value

    def __ge__(self, other: "Unsigned") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value >= other._value

    def __neg__(self) -> "Unsigned":
        raise NotImplementedError

    def __pos__(self) -> "Unsigned":
        raise NotImplementedError

    def __abs__(self) -> "Unsigned":
        raise NotImplementedError

    def __add__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __radd__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __sub__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rsub__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __mul__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rmul__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __truediv__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rtruediv__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __floordiv__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rfloordiv__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __mod__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rmod__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __and__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rand__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __or__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __ror__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __xor__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __rxor__(self, other: "Unsigned") -> "Unsigned":
        if not isinstance(other, type(self)):
            return NotImplemented
        raise NotImplementedError

    def __invert__(self) -> "Unsigned":
        raise NotImplementedError

    def __lshift__(self, amt: int) -> "Unsigned":
        raise NotImplementedError

    def __rshift__(self, amt: int) -> "Unsigned":
        raise NotImplementedError

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return "".join(str(v) for v in self)

    def __float__(self) -> float:
        return float(self._value)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({int(self)!r}, {self.range!r})"

    def _index(self, index: int) -> int:
        try:
            return len(self) - self.range.index(index) - 1
        except ValueError:
            raise IndexError(f"index {index} out of range {self.range}") from None


class Signed(AbstractArray[Bit], Integer):
    def __init__(
        self,
        value: Union[int, Iterable[LogicConstructibleT]],
        range: Optional[Range] = None,
    ) -> None:
        if isinstance(value, int):
            self._value = value
            length = _min_bit_length(value)
            if range is None:
                self._range = Range(length - 1, "downto", 0)
            else:
                self._range = range
                if len(self._range) >= length:
                    raise ValueError()
        else:
            bits = [int(Bit(v)) for v in value]
            unsigned = sum(v << i for i, v in enumerate(reversed(bits)))
            self._value = _unsigned_to_signed(unsigned, len(bits))
            if range is None:
                self._range = Range(len(bits) - 1, "downto", 0)
            else:
                self._range = range
                if len(self._range) >= len(bits):
                    raise ValueError()


def _min_bit_length(value: int) -> int:
    if value < 0:
        return int.bit_length(-value - 1) + 1
    elif value > 0:
        return int.bit_length(value)
    else:
        return 1


def _signed_to_unsigned(value: int, n_bits: int) -> int:
    if value < 0:
        return value + (1 << n_bits)
    else:
        return value


def _unsigned_to_signed(value: int, n_bits: int) -> int:
    if value & (1 << (n_bits - 1)):
        return value - (1 << n_bits)
    else:
        return value
