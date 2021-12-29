import pytest

from hdltypes.array import Array
from hdltypes.range import Range


def test_array_construct() -> None:
    Array("1234")
    Array([1, 2, 3, 4])
    with pytest.raises(TypeError):
        Array(object())  # type: ignore
    Array("1234", Range(1, "to", 4))
    with pytest.raises(TypeError):
        Array("1234", object())  # type:ignore
    with pytest.raises(TypeError):
        Array(range=Range(0, "to", 1))  # type:ignore
    with pytest.raises(ValueError):
        Array("1234", Range(0, "to", 100))


def test_range_attributes() -> None:
    a = Array("1234", Range(10, "downto", 7))
    assert a.range == Range(10, "downto", 7)
    assert a.left == 10
    assert a.right == 7
    assert a.direction == "downto"
    assert len(a) == 4


def test_sequence_operators() -> None:
    a = Array([1, 2, 3, 4])
    assert 2 in a
    assert object() not in a
    assert list(a) == [1, 2, 3, 4]
    assert list(reversed(a)) == [4, 3, 2, 1]


def test_equality() -> None:
    assert Array("1234") == Array("1234", Range(100, "to", 103))
    assert Array("1234") != 1
    assert 1 != Array("1234")


def test_indexing() -> None:
    a = Array("abcdef", Range(100, "to", 105))
    assert a[101] == "b"
    b = a[104:]
    assert b == Array("ef")
    assert b.range == Range(104, "to", 105)
    b = a[:103]
    assert b == Array("abcd")
    assert b.range == Range(100, "to", 103)
    with pytest.raises(IndexError):
        a[1000]
    with pytest.raises(TypeError):
        a[0.1]  # type: ignore
    with pytest.raises(IndexError):
        a[100:103:2]
    with pytest.raises(IndexError):
        a[103:100]


def test_setting_index() -> None:
    a = Array("abcd")
    a[0] = "q"
    assert a == Array("qbcd")
    a[0:1] = "ba"
    assert a == Array("bacd")
    a[:2] = "908"
    assert a == Array("908d")
    a[2:] = ["7", "0"]
    assert a == Array("9070")
    with pytest.raises(ValueError):
        a[:] = "way too long"
    with pytest.raises(IndexError):
        a[1000] = "1"
    with pytest.raises(TypeError):
        a[object()] = "k"  # type: ignore
    with pytest.raises(IndexError):
        a[0:3:2] = "vv"
    with pytest.raises(IndexError):
        a[3:1] = "123"


def test_concat() -> None:
    assert Array("123") + Array("456") == Array("123456")
    with pytest.raises(TypeError):
        Array("123") + 1  # type: ignore
    with pytest.raises(TypeError):
        1 + Array("123")  # type: ignore


def test_repr() -> None:
    a = Array("1234")
    assert a == eval(repr(a))
