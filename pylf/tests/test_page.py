# coding: utf-8
import PIL.Image

from pylf import _page


def test_image():
    mode = "RGB"
    size = (1, 1)
    color = "white"
    im = PIL.Image.new(mode, size, color)
    page = _page.Page(mode, size, color, 0)
    assert page.image == im


def test_num():
    num = 3
    page = _page.Page("L", (1, 1), "white", num)
    assert page.num == num


def test_draw():
    # TODO
    pass


def test_matrix():
    # TODO
    pass


def test_size():
    size = (1, 2)
    page = _page.Page("CMYK", size, "white", 0)
    assert page.size == size


def test_width():
    size = (1, 2)
    page = _page.Page("CMYK", size, "white", 0)
    assert page.width == size[0]


def test_height():
    size = (1, 2)
    page = _page.Page("CMYK", size, "white", 0)
    assert page.height == size[1]
