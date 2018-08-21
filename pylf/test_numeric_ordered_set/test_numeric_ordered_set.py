# coding: utf-8
from pylf._numeric_ordered_set import NumericOrderedSet
SIGNED_LONG = 'l'


def test_typecode():
    typecode = SIGNED_LONG
    nos = NumericOrderedSet(typecode)
    assert nos.typecode == typecode


def test_order():
    seq = list(range(10))
    nos = NumericOrderedSet(SIGNED_LONG)
    for i in seq:
        nos.add(i)
    assert list(nos) == seq


def test_len():
    nos = NumericOrderedSet(SIGNED_LONG)
    length = 10
    for i in range(length):
        assert len(nos) == i
        nos.add(i)
    assert len(nos) == length
    nos.clear()
    assert len(nos) == 0


def test_add():
    nos = NumericOrderedSet(SIGNED_LONG)
    assert nos.add(1)
    assert nos.add(0)
    assert not nos.add(1)
    assert len(nos) == 2
    assert not nos.add(1)
    assert len(nos) == 2
    assert nos.add(2)
    assert list(nos) == [1, 0, 2]
