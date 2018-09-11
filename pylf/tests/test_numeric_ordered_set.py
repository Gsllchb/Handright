# coding: utf-8
import pytest

from pylf._numeric_ordered_set import NumericOrderedSet

UNSIGNED_INT32 = 'L'
MAX_UNSIGNED_INT32_VALUE = 0xFFFFFFFF


def test_flag():
    nos = NumericOrderedSet(UNSIGNED_INT32, MAX_UNSIGNED_INT32_VALUE)
    assert MAX_UNSIGNED_INT32_VALUE == nos.flag


def test_typecode():
    nos = NumericOrderedSet(UNSIGNED_INT32, MAX_UNSIGNED_INT32_VALUE)
    assert nos.typecode == UNSIGNED_INT32


def test_order():
    seq1 = list(range(10))
    seq2 = list(range(10, 20, 2))
    nos = NumericOrderedSet(UNSIGNED_INT32, MAX_UNSIGNED_INT32_VALUE)
    for i in seq1:
        nos.add(i)
    nos.add_flag()
    for i in seq2:
        nos.add(i)
    assert list(nos) == seq1 + [MAX_UNSIGNED_INT32_VALUE, ] + seq2


def test_len():
    nos = NumericOrderedSet(UNSIGNED_INT32, MAX_UNSIGNED_INT32_VALUE)
    length = 10
    for i in range(length):
        assert len(nos) == i
        assert nos.add(i)
    assert len(nos) == length
    nos.add_flag()
    assert len(nos) == length + 1
    nos.add_flag()
    assert len(nos) == length + 2
    nos.clear()
    assert len(nos) == 0


def test_add():
    nos = NumericOrderedSet(UNSIGNED_INT32, MAX_UNSIGNED_INT32_VALUE)
    assert nos.add(1)
    assert nos.add(0)
    assert not nos.add(1)
    assert len(nos) == 2
    assert not nos.add(1)
    assert len(nos) == 2
    assert nos.add(2)
    nos.add_flag()
    assert list(nos) == [1, 0, 2, MAX_UNSIGNED_INT32_VALUE]
    with pytest.raises(ValueError):
        nos.add(MAX_UNSIGNED_INT32_VALUE)
