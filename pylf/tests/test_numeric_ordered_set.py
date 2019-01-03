# coding: utf-8
from pylf import _numeric_ordered_set as _nos

UNSIGNED_INT32 = "L"
MAX_UNSIGNED_INT32_VALUE = 0xFFFFFFFF


def test_privileged():
    privileged = MAX_UNSIGNED_INT32_VALUE
    nos = _nos.NumericOrderedSet(UNSIGNED_INT32, privileged)
    assert privileged == nos.privileged


def test_typecode():
    nos = _nos.NumericOrderedSet(UNSIGNED_INT32)
    assert nos.typecode == UNSIGNED_INT32


def test_order_with_privileged():
    privileged = MAX_UNSIGNED_INT32_VALUE
    seq1 = list(range(10))
    seq2 = list(range(10, 20, 2))
    nos = _nos.NumericOrderedSet(UNSIGNED_INT32, privileged)
    for i in seq1:
        nos.add(i)
    nos.add_privileged()
    for i in seq2:
        nos.add(i)
    assert list(nos) == seq1 + [privileged] + seq2


def test_order():
    nos = _nos.NumericOrderedSet(UNSIGNED_INT32)
    for i in (0, 2, 1, 0, 9, 8, 2, 0):
        nos.add(i)
    assert tuple(nos) == (0, 2, 1, 9, 8)


def test_len():
    privileged = MAX_UNSIGNED_INT32_VALUE
    nos = _nos.NumericOrderedSet(UNSIGNED_INT32, privileged)
    length = 10
    for i in range(length):
        assert len(nos) == i
        assert nos.add(i)
    assert len(nos) == length
    nos.add_privileged()
    assert len(nos) == length + 1
    nos.add(privileged)
    assert len(nos) == length + 2
    nos.clear()
    assert len(nos) == 0
