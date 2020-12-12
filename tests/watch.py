# coding: utf-8
""" Doing the tests with your naked eyes """
import pathlib

import PIL.Image

from handright import *
from tests.util import *

SEED = "Handright"


def main():
    # TODO: Add case for grid layout
    print("Test by naked eyes:")
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
        font_size=74,
        font=get_default_font(),
    )
    template2 = Template(
        background=image2.resize(size=(image2.size[0] * 2, image2.size[1] * 2)),
        left_margin=40,
        top_margin=200,
        right_margin=30,
        bottom_margin=980,
        line_spacing=88,
        font_size=74,
        font=get_default_font(),
    )
    templates = (template1, template2)
    for file in pathlib.Path(abs_path("texts")).iterdir():
        print(file)
        with file.open(encoding="utf-8") as f:
            text = f.read()
        images = handwrite(text, templates, seed=SEED)
        for im in images:
            im.show()
        assert input("Like it? [Y/N] ").upper() == "Y"


if __name__ == "__main__":
    main()
