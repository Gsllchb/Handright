# coding: utf-8
from PIL import Image as image

from pylf._page import Page


def test_image():
    mode = "RGB"
    size = (10, 10)
    color = "white"
    im = image.new(mode, size, color)
    page = Page(mode, size, color, 0)
    assert page.image == im


def test_num():
    num = 3
    page = Page("L", (10, 10), "white", num)
    assert page.num == num


def test_draw():
    # TODO
    pass


def test_matrix():
    # TODO
    pass


def test_size():
    size = (1, 10)
    page = Page("CMYK", size, "white", 0)
    assert page.size == size


def test_width():
    size = (1, 10)
    page = Page("CMYK", size, "white", 0)
    assert page.width == size[0]


def test_height():
    size = (100, 2)
    page = Page("CMYK", size, "white", 0)
    assert page.height == size[1]
