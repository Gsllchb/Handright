# coding: utf-8
import PIL.Image
import PIL.ImageDraw

from pylf import handwrite2, handwrite
from tests.util import *

DEFAULT_WIDTH = 2000
DEFAULT_HEIGHT = 2000
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
SEED = "PyLf"
THRESHOLD = 0.006


def get_default_template2() -> dict:
    template2 = {
        "backgrounds": [
            PIL.Image.new(mode="RGB", size=DEFAULT_SIZE, color="white"),
            PIL.Image.new(mode="RGBA", size=DEFAULT_SIZE, color="rgb(0, 128, 255)"),
        ],
        "margins": [
            {"left": 200, "top": 376, "right": 200, "bottom": 400},
            {"left": 200, "top": 384, "right": 200, "bottom": 400},
        ],
        "line_spacings": [144, 96],
        "font_sizes": [120, 80],
        "font_size_sigma": [0, 0],
        "font": get_default_font(),
        "color": "black",
    }
    return template2


def test_one_background():
    background = PIL.Image.new(mode="RGB", size=DEFAULT_SIZE, color="white")
    margin = {"left": 200, "top": 376, "right": 200, "bottom": 400}
    line_spacing = 144
    font = get_default_font()
    font_size = 120
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
    for im1, im2 in zip(images1, images2):
        assert im1 == im2


def test_even_odd():
    text = get_short_text()
    template2 = get_default_template2()
    standard_images = []
    for i in range(2):
        font_size = template2["font_sizes"][i]
        standard_image = template2["backgrounds"][i].copy()
        xy = (
            template2["margins"][i]["left"],
            template2["margins"][i]["top"]
            + template2["line_spacings"][i]
            - template2["font_sizes"][i],
        )
        draw = PIL.ImageDraw.Draw(standard_image)
        draw.text(
            xy=xy,
            text=text,
            fill=template2["color"],
            font=template2["font"].font_variant(size=font_size),
        )
        standard_images.append(standard_image)

    images2 = handwrite2((text + "\n" * 8) * 6, template2)
    for i in range(len(images2)):
        assert diff_histogram(images2[i], standard_images[i % 2]) < THRESHOLD


def test_seed():
    text = get_short_text() * 50
    template2 = get_default_template2()
    for seed in (0, "PyLf"):
        ims1 = handwrite2(text, template2, seed=seed)
        ims2 = handwrite2(text, template2, seed=seed)
        for im1, im2 in zip(ims1, ims2):
            assert im1 == im2


def test_result():
    assert isinstance(handwrite2("", get_default_template2()), list)
    assert isinstance(handwrite2(get_short_text(), get_default_template2()), list)
    assert isinstance(handwrite2(get_long_text(), get_default_template2()), list)
