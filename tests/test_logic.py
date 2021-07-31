import pytest

from hdltypes.logic import X01Z, Bit, StdLogic


def test_construct():
    # will not be exhaustive
    StdLogic(0)
    StdLogic(True)
    StdLogic("-")
    StdLogic(Bit())
    X01Z(1)
    X01Z(False)
    X01Z("Z")
    X01Z(StdLogic("z"))
    Bit(0)
    Bit(True)
    Bit("1")
    Bit(StdLogic(0))

    assert StdLogic() == StdLogic("U")
    assert X01Z() == X01Z("X")
    assert Bit() == Bit("0")

    with pytest.raises(ValueError):
        StdLogic(object())
    with pytest.raises(ValueError):
        X01Z(StdLogic("L"))
    with pytest.raises(ValueError):
        Bit("x")


def test_convert():
    # will not be exhaustive
    assert int(StdLogic(0)) == 0
    assert int(Bit(1)) == 1
    with pytest.raises(ValueError):
        int(X01Z("X"))

    assert bool(X01Z(True)) is True
    assert bool(StdLogic(0)) is False
    with pytest.raises(ValueError):
        bool(StdLogic("X"))

    assert str(StdLogic("-")) == "-"
    assert str(X01Z("Z")) == "Z"


def test_equality():
    assert StdLogic("0") == Bit(0)
    assert X01Z("X") == StdLogic("X")
    assert Bit(0) != StdLogic(1)
    assert X01Z(False) != 8
    assert "1" != StdLogic("1")


def test_and():
    # will not be exhaustive
    assert StdLogic("1") & StdLogic("H") == StdLogic("1")
    assert X01Z("Z") & X01Z("0") == X01Z("0")
    assert Bit(1) & Bit(1) == Bit(1)
    with pytest.raises(TypeError):
        StdLogic() & object()
    with pytest.raises(TypeError):
        7 & X01Z()


def test_or():
    # will not be exhaustive
    assert StdLogic("0") | StdLogic("H") == StdLogic("1")
    assert X01Z("Z") | X01Z("0") == X01Z("X")
    assert Bit(0) | Bit(0) == Bit(0)
    with pytest.raises(TypeError):
        StdLogic() | object()
    with pytest.raises(TypeError):
        7 | Bit()


def test_xor():
    # will not be exhaustive
    assert StdLogic("0") ^ StdLogic("H") == StdLogic("1")
    assert X01Z("Z") ^ X01Z("0") == X01Z("X")
    assert Bit(1) ^ Bit(1) == Bit(0)
    with pytest.raises(TypeError):
        StdLogic() ^ object()
    with pytest.raises(TypeError):
        7 ^ Bit()


def test_invert():
    assert ~StdLogic("H") == StdLogic("0")
    assert ~X01Z("Z") == X01Z("X")
    assert ~Bit(0) == Bit(1)


def test_repr():
    a = StdLogic("U")
    assert eval(repr(a)) == a


def test_hash():
    assert len({Bit(0), Bit(1)}) == 2
    assert len({Bit(0), StdLogic(0)}) == 1


def test_promotion():
    assert type(StdLogic() & StdLogic()) is StdLogic
    assert type(StdLogic() & X01Z()) is StdLogic
    assert type(StdLogic() & Bit()) is StdLogic
    assert type(X01Z() & StdLogic()) is StdLogic
    assert type(X01Z() & X01Z()) is X01Z
    assert type(X01Z() & Bit()) is X01Z
    assert type(Bit() & StdLogic()) is StdLogic
    assert type(Bit() & X01Z()) is X01Z
    assert type(Bit() & Bit()) is Bit
