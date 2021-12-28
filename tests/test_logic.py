import pytest

from hdltypes.logic import X01Z, Bit, StdLogic


def test_construct() -> None:
    StdLogic("-")
    StdLogic(Bit("1"))
    X01Z("Z")
    X01Z(StdLogic("z"))
    Bit("1")
    Bit(StdLogic("0"))

    with pytest.raises(ValueError):
        X01Z(StdLogic("L"))
    with pytest.raises(ValueError):
        Bit("x")
    with pytest.raises(TypeError):
        StdLogic(object())  # type: ignore
    with pytest.raises(ValueError):
        X01Z("lol")


def test_convert() -> None:
    assert str(StdLogic("-")) == "-"
    assert str(X01Z("Z")) == "Z"


def test_equality() -> None:
    assert StdLogic("0") == Bit("0")
    assert X01Z("X") == StdLogic("X")
    assert Bit("0") != StdLogic("1")
    assert X01Z("0") != 8
    assert "1" != StdLogic("1")


def test_and() -> None:
    # will not be exhaustive
    assert StdLogic("1") & StdLogic("H") == StdLogic("1")
    assert X01Z("Z") & X01Z("0") == X01Z("0")
    assert Bit("1") & Bit("1") == Bit("1")


def test_or() -> None:
    # will not be exhaustive
    assert StdLogic("0") | StdLogic("H") == StdLogic("1")
    assert X01Z("Z") | X01Z("0") == X01Z("X")
    assert Bit("0") | Bit("0") == Bit("0")


def test_xor() -> None:
    # will not be exhaustive
    assert StdLogic("0") ^ StdLogic("H") == StdLogic("1")
    assert X01Z("Z") ^ X01Z("0") == X01Z("X")
    assert Bit("1") ^ Bit("1") == Bit("0")


def test_invert() -> None:
    assert ~StdLogic("H") == StdLogic("0")
    assert ~X01Z("Z") == X01Z("X")
    assert ~Bit("0") == Bit("1")


def test_repr() -> None:
    a = StdLogic("U")
    assert eval(repr(a)) == a


def test_hash() -> None:
    assert len({Bit("0"), Bit("1")}) == 2
    assert len({Bit("0"), StdLogic("0")}) == 1


def test_promotion() -> None:
    assert type(StdLogic("0") & StdLogic("0")) is StdLogic
    assert type(StdLogic("0") | X01Z("0")) is StdLogic
    assert type(StdLogic("0") ^ Bit("0")) is StdLogic
    assert type(X01Z("0") & StdLogic("0")) is StdLogic
    assert type(X01Z("0") | X01Z("0")) is X01Z
    assert type(X01Z("0") ^ Bit("0")) is X01Z
    assert type(Bit("0") & StdLogic("0")) is StdLogic
    assert type(Bit("0") | X01Z("0")) is X01Z
    assert type(Bit("0") ^ Bit("0")) is Bit
