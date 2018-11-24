# coding: utf-8
import PIL.Image
import pytest

from pylf import *
from tests.util import *

WIDTH = 50
HEIGHT = 50
SIZE = (WIDTH, HEIGHT)
FONT_SIZE = 3

SEED = "PyLf"

SUPPORTED_MODES = ("1", "L", "RGB", "RGBA")

MAX_IMAGE_SIDE_LENGTH = 0xFFFF - 1


def get_default_template() -> dict:
    template = {
        "background": PIL.Image.new("RGB", SIZE),
        "margin": {"left": 5, "top": 9, "right": 5, "bottom": 10},
        "line_spacing": 4,
        "font": get_default_font(),
        "font_size": FONT_SIZE,
    }
    return template


def get_default_template2() -> dict:
    template2 = {
        "backgrounds": (
            PIL.Image.new("RGB", SIZE),
            PIL.Image.new("RGBA", SIZE)
        ),
        "margins": (
            {"left": 5, "top": 9, "right": 5, "bottom": 10},
            {"left": 5, "top": 10, "right": 5, "bottom": 10},
        ),
        "line_spacings": (4, 2),
        "font_sizes": (FONT_SIZE, FONT_SIZE),
        "font": get_default_font(),
    }
    return template2


def test_text():
    with pytest.raises(TypeError):
        handwrite(1, get_default_template())
    with pytest.raises(TypeError):
        handwrite2(None, get_default_template2())
    with pytest.raises(TypeError):
        handwrite(list("123"), get_default_template())
    with pytest.raises(TypeError):
        handwrite2(tuple(""), get_default_template2())


def test_worker():
    with pytest.raises(TypeError):
        handwrite("", get_default_template(), worker=3.3)
    with pytest.raises(TypeError):
        handwrite2("", get_default_template2(), worker=-3.3)
    with pytest.raises(ValueError):
        handwrite("", get_default_template(), worker=0)
    with pytest.raises(ValueError):
        handwrite2("", get_default_template2(), worker=-0)


def test_seed():
    with pytest.raises(TypeError):
        handwrite("", get_default_template(), seed=[])
    with pytest.raises(TypeError):
        handwrite2("", get_default_template2(), seed={})


def test_background():
    helper("background", 1, TypeError)
    helper(
        "background",
        PIL.Image.new("1", (MAX_IMAGE_SIDE_LENGTH + 1, 1)),
        ValueError
    )
    helper(
        "background",
        PIL.Image.new("1", (1, MAX_IMAGE_SIDE_LENGTH + 1)),
        ValueError
    )
    for mode in PIL.Image.MODES:
        if mode in SUPPORTED_MODES:
            continue
        helper("background", PIL.Image.new(mode, SIZE), NotImplementedError)


def test_margin():
    helper(
        "margin",
        {"left": 3.3, "right": 0, "top": 0, "bottom": 0},
        TypeError
    )
    helper(
        "margin",
        {"left": 0, "right": -1, "top": 0, "bottom": 0},
        ValueError
    )


def test_line_spacing():
    helper("line_spacing", 1.2, TypeError)
    helper("line_spacing", 0, ValueError)
    helper("line_spacing", HEIGHT * 2, LayoutError)


def test_font_size():
    helper("font_size", 1.2, TypeError)
    helper("font_size", 0, ValueError)
    helper("font_size", WIDTH * 2, LayoutError)


def test_word_spacing():
    helper("word_spacing", 1.2, TypeError)
    helper("word_spacing", -FONT_SIZE // 2, LayoutError)


def test_color():
    helper("color", 0, TypeError)
    helper("color", "2333333333", ValueError)


def test_sigmas():
    for sigma in (
        "line_spacing_sigma",
        "font_size_sigma",
        "word_spacing_sigma",
        "perturb_x_sigma",
        "perturb_y_sigma",
        "perturb_theta_sigma",
    ):
        helper(sigma, 1 + 2j, TypeError)
        helper(sigma, -1, ValueError)


def test_fns():
    for fn in ("is_half_char_fn", "is_end_char_fn"):
        helper(fn, 0, TypeError)


def helper(key: str, value, exception_type) -> None:
    template = get_default_template()
    template[key] = value
    with pytest.raises(exception_type):
        handwrite("PyLf", template)
