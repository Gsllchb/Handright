# coding: utf-8
import PIL.Image

from pylf import handwrite2, handwrite
from tests.util import *
import PIL.ImageColor

WIDTH = 32
HEIGHT = 32
SIZE = (WIDTH, HEIGHT)
SEED = "PyLf"


def get_default_template2() -> dict:
    template2 = {
        "backgrounds": [
            PIL.Image.new(mode="RGB", size=SIZE, color="white"),
            PIL.Image.new(mode="RGB", size=SIZE, color="rgb(0, 128, 255)"),
        ],
        "margins": [
            {"left": 3, "top": 6, "right": 3, "bottom": 6},
            {"left": 3, "top": 7, "right": 3, "bottom": 6},
        ],
        "line_spacings": [2, 1],
        "font_sizes": [2, 1],
        "font": get_default_font(),
        "fill": (0, 0, 0),
    }
    return template2


def test_one_background():
    background = PIL.Image.new(mode="RGB", size=SIZE, color="white")
    margin = {"left": 3, "top": 6, "right": 3, "bottom": 6}
    line_spacing = 2
    font = get_default_font()
    font_size = 2

    text = get_long_text()
    template = {
        "background": background,
        "margin": margin,
        "line_spacing": line_spacing,
        "font": font,
        "font_size": font_size,
        "fill": (0, 0, 0),
    }
    template2 = {
        "backgrounds": (background,),
        "margins": (margin,),
        "line_spacings": (line_spacing,),
        "font_sizes": (font_size,),
        "font": font,
        "fill": (0, 0, 0),
    }
    images1 = handwrite(text, template, seed=SEED)
    images2 = handwrite2(text, template2, seed=SEED)
    assert images1 == images2


def test_seed():
    text = get_long_text()
    template2 = get_default_template2()
    for seed in (0, "PyLf"):
        images1 = handwrite2(text, template2, seed=seed)
        images2 = handwrite2(text, template2, seed=seed)
        assert images1 == images2

    images1 = handwrite2(text, template2, seed=None)
    images2 = handwrite2(text, template2, seed=None)
    assert not images1 == images2


def test_result():
    assert isinstance(handwrite2("", get_default_template2()), list)
    assert isinstance(handwrite2(get_short_text(), get_default_template2()), list)
    assert isinstance(handwrite2(get_long_text(), get_default_template2()), list)


def test_1_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["backgrounds"] = [
        PIL.Image.new("L", SIZE, color="white"),
        PIL.Image.new("L", SIZE, color="white"),
    ]
    template2["fill"] = 0
    criterion = handwrite2(text, template2, seed=SEED)
    template2["backgrounds"] = [
        PIL.Image.new("1", SIZE, color="white"),
        PIL.Image.new("1", SIZE, color="white"),
    ]
    images = handwrite2(text, template2, seed=SEED)
    criterion = [image.convert("1") for image in criterion]
    assert criterion == images


def test_l_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["fill"] = (120, 100, 0)
    template2["backgrounds"] = [
        PIL.Image.new("RGB", SIZE, color="yellow"),
        PIL.Image.new("RGB", SIZE, color="black"),
    ]
    criterion = handwrite2(text, template2, seed=SEED)
    template2["backgrounds"] = [
        PIL.Image.new("L", SIZE, color="yellow"),
        PIL.Image.new("L", SIZE, color="black"),
    ]
    template2["fill"] = PIL.ImageColor.getcolor("rgb{}".format(template2["fill"]), mode="L")
    images = handwrite2(text, template2, seed=SEED)
    criterion = [image.convert("L") for image in criterion]
    assert criterion == images


def test_rgba_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["fill"] = (255, 0, 0)
    template2["backgrounds"] = [
        PIL.Image.new("RGB", SIZE, color="white"),
        PIL.Image.new("RGB", SIZE, color="pink"),
    ]
    criterion = handwrite2(text, template2, seed=SEED)
    template2["fill"] = (255, 0, 0, 0)
    template2["backgrounds"] = [
        PIL.Image.new("RGBA", SIZE, color="white"),
        PIL.Image.new("RGBA", SIZE, color="pink"),
    ]
    images = handwrite2(text, template2, seed=SEED)
    images = [image.convert("RGB") for image in images]
    assert criterion == images


def test_rgb_image():
    # Test by human beings' naked eyes.
    # Please run watch.py
    pass
