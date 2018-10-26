# coding: utf-8
import PIL.Image

from pylf import handwrite2, handwrite
from tests.util import *

WIDTH = 100
HEIGHT = 100
SIZE = (WIDTH, HEIGHT)
SEED = "PyLf"


def get_default_template2() -> dict:
    template2 = {
        "backgrounds": [
            PIL.Image.new(mode="RGB", size=SIZE, color="white"),
            PIL.Image.new(mode="RGBA", size=SIZE, color="rgb(0, 128, 255)"),
        ],
        "margins": [
            {"left": 10, "top": 18, "right": 10, "bottom": 20},
            {"left": 10, "top": 19, "right": 10, "bottom": 20},
        ],
        "line_spacings": [7, 4],
        "font_sizes": [6, 4],
        "font_size_sigma": [0, 0],
        "font": get_default_font(),
    }
    return template2


def test_one_background():
    background = PIL.Image.new(mode="RGB", size=SIZE, color="white")
    margin = {"left": 10, "top": 18, "right": 10, "bottom": 20}
    line_spacing = 7
    font = get_default_font()
    font_size = 6
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


def test_1_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["backgrounds"] = [
        PIL.Image.new("L", SIZE, color="white"),
        PIL.Image.new("L", SIZE, color="white"),
    ]
    criterion = handwrite2(text, template2, seed=SEED)
    template2["backgrounds"] = [
        PIL.Image.new("1", SIZE, color="white"),
        PIL.Image.new("1", SIZE, color="white"),
    ]
    images = handwrite2(text, template2, seed=SEED)
    criterion = [image.convert("1") for image in criterion]
    assert all(im1 == im2 for im1, im2 in zip(criterion, images))


def test_l_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["color"] = "orange"
    template2["backgrounds"] = [
        PIL.Image.new("RGB", SIZE, color="yellow"),
        PIL.Image.new("RGB", SIZE, color="black"),
    ]
    criterion = handwrite2(text, template2, seed=SEED)
    template2["backgrounds"] = [
        PIL.Image.new("L", SIZE, color="yellow"),
        PIL.Image.new("L", SIZE, color="black"),
    ]
    images = handwrite2(text, template2, seed=SEED)
    criterion = [image.convert("L") for image in criterion]
    assert all(im1 == im2 for im1, im2 in zip(criterion, images))


def test_rgba_image():
    text = get_long_text()
    template2 = get_default_template2()
    template2["color"] = "red"
    template2["backgrounds"] = [
        PIL.Image.new("RGB", SIZE, color="white"),
        PIL.Image.new("RGB", SIZE, color="pink"),
    ]
    criterion = handwrite2(text, template2, seed=SEED)
    template2["backgrounds"] = [
        PIL.Image.new("RGBA", SIZE, color="white"),
        PIL.Image.new("RGBA", SIZE, color="pink"),
    ]
    images = handwrite2(text, template2, seed=SEED)
    images = [image.convert("RGB") for image in images]
    assert all(im1 == im2 for im1, im2 in zip(criterion, images))


def test_rgb_image():
    # Test by human beings' naked eyes.
    # Please run watch.py
    pass
