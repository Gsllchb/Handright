# coding: utf-8
import PIL.Image
import PIL.ImageDraw

from pylf import handwrite2, handwrite
from tests.util import *

DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 200
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
SEED = "PyLf"


def get_default_template2() -> dict:
    template2 = {
        "backgrounds": [
            PIL.Image.new(mode="RGB", size=DEFAULT_SIZE, color="white"),
            PIL.Image.new(mode="RGBA", size=DEFAULT_SIZE, color="rgb(0, 128, 255)"),
        ],
        "margins": [
            {"left": 20, "top": 37, "right": 20, "bottom": 40},
            {"left": 20, "top": 38, "right": 20, "bottom": 40},
        ],
        "line_spacings": [14, 9],
        "font_sizes": [12, 8],
        "font_size_sigma": [0, 0],
        "font": get_default_font(),
        "color": "black",
    }
    return template2


def test_one_background():
    background = PIL.Image.new(mode="RGB", size=DEFAULT_SIZE, color="white")
    margin = {"left": 20, "top": 37, "right": 20, "bottom": 40}
    line_spacing = 14
    font = get_default_font()
    font_size = 12
    font_size_sigma = 0

    text = get_long_text()
    template = {
        "background": background,
        "margin": margin,
        "line_spacing": line_spacing,
        "font": font,
        "font_size": font_size,
        "font_size_sigma": font_size_sigma,
    }
    template2 = {
        "backgrounds": (background,),
        "margins": (margin,),
        "line_spacings": (line_spacing,),
        "font_sizes": (font_size,),
        "font_size_sigmas": (font_size_sigma,),
        "font": font,
    }
    images1 = handwrite(text, template, seed=SEED)
    images2 = handwrite2(text, template2, seed=SEED)
    assert all(im1 == im2 for im1, im2 in zip(images1, images2))


def test_seed():
    text = get_long_text()
    template2 = get_default_template2()
    for seed in (0, "PyLf"):
        images1 = handwrite2(text, template2, seed=seed)
        images2 = handwrite2(text, template2, seed=seed)
        assert all(im1 == im2 for im1, im2 in zip(images1, images2))


def test_result():
    assert isinstance(handwrite2("", get_default_template2()), list)
    assert isinstance(handwrite2(get_short_text(), get_default_template2()), list)
    assert isinstance(handwrite2(get_long_text(), get_default_template2()), list)
