import pytest

from hdltypes.logic import StdLogic
from hdltypes.logic_array import BitArray, StdLogicArray


def test_construct() -> None:
    a = StdLogicArray("01XZulH-W")
    assert list(a) == [
        StdLogic("0"),
        StdLogic("1"),
        StdLogic("X"),
        StdLogic("Z"),
        StdLogic("U"),
        StdLogic("L"),
        StdLogic("H"),
        StdLogic("-"),
        StdLogic("W"),
    ]
    with pytest.raises(ValueError):
        StdLogicArray("not a StdLogicArray literal")


def test_setting_index() -> None:
    a = StdLogicArray("1010")
    a[2] = "X"
    assert a == StdLogicArray("10X0")
    a[:] = "1000"
    assert a == StdLogicArray("1000")
    with pytest.raises(TypeError):
        a[[1, 2]] = "0"  # type: ignore


def test_and() -> None:
    assert StdLogicArray("01XZ") & StdLogicArray("1101") == StdLogicArray("010X")
    assert StdLogicArray("X1") & BitArray("10") == StdLogicArray("X0")
    with pytest.raises(ValueError):
        BitArray("1010") & StdLogicArray("10")
    with pytest.raises(TypeError):
        BitArray("100") & 7  # type: ignore
    with pytest.raises(TypeError):
        7 & StdLogicArray("0010")  # type: ignore

    assert type(StdLogicArray("0") & StdLogicArray("1")) is StdLogicArray
    assert type(StdLogicArray("X") & BitArray("0")) is StdLogicArray
    assert type(BitArray("0") & StdLogicArray("0")) is StdLogicArray
    assert type(BitArray("0") & BitArray("1")) is BitArray


def test_or() -> None:
    assert StdLogicArray("01XZ") | StdLogicArray("0011") == StdLogicArray("0111")
    assert BitArray("10") | StdLogicArray("ZX") == StdLogicArray("1X")
    with pytest.raises(ValueError):
        BitArray("1010") | StdLogicArray("10")
    with pytest.raises(TypeError):
        BitArray("100") | [1, 0, 1]  # type: ignore
    with pytest.raises(TypeError):
        "nope" | StdLogicArray("00")  # type: ignore

    assert type(StdLogicArray("0") | StdLogicArray("1")) is StdLogicArray
    assert type(StdLogicArray("X") | BitArray("0")) is StdLogicArray
    assert type(BitArray("0") | StdLogicArray("0")) is StdLogicArray
    assert type(BitArray("0") | BitArray("1")) is BitArray


def test_xor() -> None:
    assert StdLogicArray("01XZ") ^ StdLogicArray("1101") == StdLogicArray("10XX")
    assert StdLogicArray("X1") ^ BitArray("11") == StdLogicArray("X0")
    with pytest.raises(ValueError):
        BitArray("1010") ^ StdLogicArray("10")
    with pytest.raises(TypeError):
        100 ^ BitArray("10")  # type: ignore
    with pytest.raises(TypeError):
        BitArray("10") ^ "100"  # type: ignore

    assert type(StdLogicArray("0") ^ StdLogicArray("1")) is StdLogicArray
    assert type(StdLogicArray("X") ^ BitArray("0")) is StdLogicArray
    assert type(BitArray("0") ^ StdLogicArray("0")) is StdLogicArray
    assert type(BitArray("0") ^ BitArray("1")) is BitArray


def test_invert() -> None:
    assert ~StdLogicArray("UX01Z") == StdLogicArray("UX10X")
    assert type(~BitArray("0")) is BitArray


def test_concat() -> None:
    assert StdLogicArray("01XZ") + StdLogicArray("1101") == StdLogicArray("01XZ1101")
    assert BitArray("10") + StdLogicArray("X1") == StdLogicArray("10X1")
    with pytest.raises(TypeError):
        1 + StdLogicArray("1010")  # type: ignore
    with pytest.raises(TypeError):
        StdLogicArray("00") + object()  # type: ignore

    assert type(StdLogicArray("0") + StdLogicArray("1")) is StdLogicArray
    assert type(StdLogicArray("X") + BitArray("0")) is StdLogicArray
    assert type(BitArray("0") + StdLogicArray("0")) is StdLogicArray
    assert type(BitArray("0") + BitArray("1")) is BitArray
