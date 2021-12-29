# Copyright cocotb contributors
# Copyright Kaleb Barrett
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause
from typing import Optional, Sequence, Union, overload


class Range(Sequence[int]):
    r"""
    Integer range with inclusive right bound.

    This type mimics Python's :class:`range` type, but uses inclusive right bounds as seen in VHDL and Verilog.
    The attributes :attr:`left` and :attr:`right` are used instead of ``start`` and ``stop`` to mimic VHDL.
    Range direction can be specified using ``'to'`` or ``'downto'`` between the left and right bounds.
    Not specifying a direction will cause the direction to be inferred.

    .. code-block:: python3

        >>> r = Range(-2, 3)
        >>> r.left, r.right, len(r)
        (-2, 3, 6)

        >>> s = Range(8, 'downto', 1)
        >>> s.left, s.right, len(s)
        (8, 1, 8)

    :meth:`from_range` and :meth:`to_range` can be used to convert from and to :py:class:`range`.

    .. code-block:: python3

        >>> py_range = range(-2, 4)
        >>> hdl_range = Range.from_range(py_range)
        >>> hdl_range.to_range()
        range(-2, 4)

    "Null" ranges, as seen in VHDL, occur when a left bound cannot reach a right bound in the given direction.
    They have a length of 0, but the :attr:`left`, :attr:`right`, and :attr:`direction` values remain as given.

    .. code-block:: python3

        >>> r = Range(1, 'to', 0)  # no way to count from 1 'to' 0
        >>> r.left, r.direction, r.right
        (1, 'to', 0)
        >>> len(r)
        0

    .. note::
        Null ranges are only possible when specifying the direction.

    Ranges implement all the features of :py:class:`~collections.abc.Sequence` protocol and are hashable and equatable.

    .. code-block:: python3

        >>> r = Range(-2, 2)

        >>> 4 in r  # is '4' in the Range?
        False
        >>> r.index(0)  # what position in the Range is '0'?
        2
        >>> r[2]  # what value is at position 2 in the Range?
        0
        >>> r.count(0)  # how many '0's are in the Range?
        1

        >>> s = {Range(0, 10)}       # Ranges are hashable
        >>> Range(0, 'to', 10) in s  # and equatable
        True

    Args:
        left: leftmost bound of range
        direction: ``'to'`` if values are ascending, ``'downto'`` if descending
        right: rightmost bound of range (inclusive)
    """

    @overload
    def __init__(self, left: int, direction: str, right: int) -> None:
        ...

    @overload
    def __init__(self, left: int, right: int) -> None:
        ...

    def __init__(  # type: ignore
        self,
        left: int,
        direction: Optional[Union[int, str]] = None,
        right: Optional[int] = None,
    ) -> None:
        start = left
        stop: int
        step: int
        if isinstance(direction, int) and right is None:
            step = _guess_step(left, direction)
            stop = direction + step
        elif direction is None and isinstance(right, int):
            step = _guess_step(left, right)
            stop = right + step
        elif isinstance(direction, str) and isinstance(right, int):
            step = _direction_to_step(direction)
            stop = right + step
        else:
            raise TypeError("invalid arguments")
        self._range = range(start, stop, step)

    @classmethod
    def from_range(cls, range: range) -> "Range":
        """Construct from a :py:class:`range`"""
        return cls(
            left=range.start,
            direction=_step_to_direction(range.step),
            right=(range.stop - range.step),
        )

    def to_range(self) -> range:
        """Convert to :py:class:`range`"""
        return self._range

    @property
    def left(self) -> int:
        """The leftmost value in a Range"""
        return self._range.start

    @property
    def direction(self) -> str:
        """``'to'`` if values are meant to be ascending, ``'downto'`` otherwise."""
        return _step_to_direction(self._range.step)

    @property
    def right(self) -> int:
        """The rightmost value in a Range"""
        return self._range.stop - self._range.step

    def __len__(self) -> int:
        return len(self._range)

    @overload
    def __getitem__(self, item: int) -> int:
        ...

    @overload
    def __getitem__(self, item: slice) -> "Range":
        ...

    def __getitem__(self, item: Union[int, slice]) -> Union[int, "Range"]:
        if isinstance(item, int):
            return self._range[item]
        elif isinstance(item, slice):
            return type(self).from_range(self._range[item])
        else:
            raise TypeError(
                "indices must be integers or slices, not {}".format(
                    type(item).__qualname__
                )
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._range == other._range
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self._range)

    def __repr__(self) -> str:
        return (
            f"{type(self).__qualname__}"
            f"({self.left!r}, {self.direction!r}, {self.right!r})"
        )


def _guess_step(left: int, right: int) -> int:
    if left <= right:
        return 1
    return -1


def _direction_to_step(direction: str) -> int:
    direction = direction.lower()
    if direction == "to":
        return 1
    elif direction == "downto":
        return -1
    raise ValueError("direction must be 'to' or 'downto'")


def _step_to_direction(step: int) -> str:
    if step == 1:
        return "to"
    elif step == -1:
        return "downto"
    raise ValueError("step must be 1 or -1")
