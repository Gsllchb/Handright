# coding: utf-8
import PIL.Image
import pytest

from pylf import *
from tests.util import *

BACKGROUND_COLOR = "white"
DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
SEED = "PyLf"
THRESHOLD = 0.01


def get_default_template() -> dict:
    template = {"background": PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color=BACKGROUND_COLOR),
                "margin": {"left": 50, "top": 94, "right": 50, "bottom": 100},
                "line_spacing": 36,
                "font": get_default_font(),
                "font_size": 30,
                "font_size_sigma": 0}
    return template


def get_default_template2() -> dict:
    template2 = {"backgrounds": (PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color="white"),
                                 PIL.Image.new(mode='RGBA', size=DEFAULT_SIZE, color='rgb(0, 128, 255)')),
                 "margins": ({"left": 50, "top": 94, "right": 50, "bottom": 100},
                            {"left": 50, "top": 96, "right": 50, "bottom": 100}),
                 "line_spacings": (36, 24),
                 "font_sizes": (30, 20),
                 "font_size_sigma": (0, 0),
                 "font": get_default_font(),
                 "color": "black"}
    return template2


def test_text_error():
    with pytest.raises(TypeError):
        handwrite(1, get_default_template())
    with pytest.raises(TypeError):
        handwrite2(1, get_default_template2())


def test_worker_error():
    with pytest.raises(TypeError):
        handwrite("", get_default_template(), worker=3.3)
    with pytest.raises(TypeError):
        handwrite2("", get_default_template2(), worker=3.3)
    with pytest.raises(ValueError):
        handwrite("", get_default_template(), worker=0)
    with pytest.raises(ValueError):
        handwrite2("", get_default_template2(), worker=0)


def test_seed_error():
    with pytest.raises(TypeError):
        handwrite("", get_default_template(), seed=[])
    with pytest.raises(TypeError):
        handwrite2("", get_default_template2(), seed=[])


def test_template_error():
    template_error_helper("background", 1, TypeError)

    template_error_helper("margin", {"left": 3.3, "right": 0, "top": 0, "bottom": 0}, TypeError)
    template_error_helper("margin", {"left": 0, "right": -1, "top": 0, "bottom": 0}, ValueError)

    template_error_helper("line_spacing", 1.2, TypeError)
    template_error_helper("line_spacing", 0, ValueError)
    template_error_helper("line_spacing", DEFAULT_HEIGHT * 2, ValueError)

    template_error_helper("font_size", 1.2, TypeError)
    template_error_helper("font_size", 0, ValueError)
    template_error_helper("font_size", DEFAULT_WIDTH * 2, ValueError)

    template_error_helper("word_spacing", 1.2, TypeError)
    template_error_helper("word_spacing", (-get_default_template()["font_size"] // 2), ValueError)

    template_error_helper("color", 0, TypeError)

    for sigma in ("line_spacing_sigma", "font_size_sigma", "word_spacing_sigma", "perturb_x_sigma", "perturb_y_sigma",
                  "perturb_theta_sigma"):
        template_error_helper(sigma, "1", TypeError)
        template_error_helper(sigma, -1, ValueError)

    for fn in ("is_half_char_fn", "is_end_char_fn"):
        template_error_helper(fn, 0, TypeError)


def template_error_helper(key: str, value, error_type) -> None:
    template = get_default_template()
    template[key] = value
    with pytest.raises(error_type):
        handwrite("", template)


def test_template2_error():
    template2 = get_default_template2()
    template2["word_spacings"] = (0, )
    with pytest.raises(ValueError):
        handwrite2("", template2)
    # TODO: test all the parameters
