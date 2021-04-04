# coding: utf-8
""" Doing the tests with your naked eyes """

import PIL.Image

from handright import *
from tests.util import *

SEED = "Handright"


def main():
    print("Test by naked eyes:")
    _watch_gird_layout()
    _like_it()
    _watch_flow_layout()
    _like_it()


def _watch_flow_layout():
    path = "backgrounds/even-odd-letter/"
    image1 = PIL.Image.open(abs_path(path + "村庄信笺纸.jpg"))
    image2 = PIL.Image.open(abs_path(path + "树信笺纸.jpg"))
    assert image1.mode == "RGB"
    assert image2.mode == "RGB"

    template1 = Template(
        background=image1.resize(size=(image1.size[0] * 2, image1.size[1] * 2)),
        left_margin=40,
        top_margin=200,
        right_margin=30,
        bottom_margin=560,
        line_spacing=88,
        font=get_default_font(74),
    )
    template2 = Template(
        background=image2.resize(size=(image2.size[0] * 2, image2.size[1] * 2)),
        left_margin=40,
        top_margin=200,
        right_margin=30,
        bottom_margin=980,
        line_spacing=88,
        font=get_default_font(74),
    )
    templates = (template1, template2)
    with open(abs_path("texts/从百草园到三味书屋.txt"), encoding="utf-8") as f:
        text = f.read()
    images = handwrite(text, templates, seed=SEED)
    for im in images:
        im.show()


def _watch_gird_layout():
    image = PIL.Image.open(abs_path("backgrounds/grid.jpeg"))
    assert image.mode == "L"
    template = Template(
        background=image,
        left_margin=0,
        top_margin=0,
        right_margin=0,
        bottom_margin=0,
        line_spacing=56,
        word_spacing=4,
        font=get_default_font(37),
        font_size_sigma=0.3,
        word_spacing_sigma=0.8,
        line_spacing_sigma=1,
        features={Feature.GRID_LAYOUT},
    )
    with open(abs_path("texts/荷塘月色.txt"), encoding="utf-8") as f:
        text = f.read()
    images = handwrite(text, template, seed=SEED)
    for im in images:
        im.show()


def _like_it() -> None:
    assert input("Like it? [Y/N] ").upper() == "Y"


if __name__ == "__main__":
    main()
