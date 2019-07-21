# coding: utf-8
import PIL.Image

from handright._util import *

UNSIGNED_INT32 = "L"
MAX_UNSIGNED_INT32_VALUE = 0xFFFFFFFF


def test_count_bands():
    assert count_bands("1") == 1
    assert count_bands("L") == 1
    assert count_bands("P") == 1
    assert count_bands("RGB") == 3
    assert count_bands("RGBA") == 4
    assert count_bands("CMYK") == 4
    assert count_bands("YCbCr") == 3
    assert count_bands("LAB") == 3
    assert count_bands("HSV") == 3
    assert count_bands("I") == 1
    assert count_bands("F") == 1


def test_page_image():
    mode = "RGB"
    size = (1, 1)
    color = "white"
    im = PIL.Image.new(mode, size, color)
    page = Page(mode, size, color, 0)
    assert page.image == im


def test_page_num():
    num = 3
    page = Page("L", (1, 1), "white", num)
    assert page.num == num


def test_page_draw():
    # TODO
    pass


def test_page_matrix():
    # TODO
    pass


def test_page_size():
    size = (1, 2)
    page = Page("CMYK", size, "white", 0)
    assert page.size() == size


def test_page_width():
    size = (1, 2)
    page = Page("CMYK", size, "white", 0)
    assert page.width() == size[0]


def test_page_height():
    size = (1, 2)
    page = Page("CMYK", size, "white", 0)
    assert page.height() == size[1]


def test_nos_privileged():
    privileged = MAX_UNSIGNED_INT32_VALUE
    nos = NumericOrderedSet(UNSIGNED_INT32, privileged)
    assert privileged == nos.privileged()


def test_nos_typecode():
    nos = NumericOrderedSet(UNSIGNED_INT32)
    assert nos.typecode() == UNSIGNED_INT32


def test_nos_order_with_privileged():
    privileged = MAX_UNSIGNED_INT32_VALUE
    seq1 = list(range(10))
    seq2 = list(range(10, 20, 2))
    nos = NumericOrderedSet(UNSIGNED_INT32, privileged)
    for i in seq1:
        nos.add(i)
    nos.add_privileged()
    for i in seq2:
        nos.add(i)
    assert list(nos) == seq1 + [privileged] + seq2


def test_nos_order():
    nos = NumericOrderedSet(UNSIGNED_INT32)
    for i in (0, 2, 1, 0, 9, 8, 2, 0):
        nos.add(i)
    assert tuple(nos) == (0, 2, 1, 9, 8)


def test_nos_len():
    privileged = MAX_UNSIGNED_INT32_VALUE
    nos = NumericOrderedSet(UNSIGNED_INT32, privileged)
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
