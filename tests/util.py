# coding: utf-8
"""
This module provides the essential functionality for the whole test suite.
WARNING: Do not change the location of this file!
"""
import os

import PIL.ImageFont

_long_text = None


def visually_equal(image1, image2) -> bool:
    return (image1.tobytes() == image2.tobytes()
            and image1.mode == image2.mode
            and image1.size == image2.size)


def abs_path(*paths) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)


def get_short_text() -> str:
    """ Return one short sentence """
    return "我能吞下玻璃而不伤身体。"


def get_long_text() -> str:
    """ Return a article """
    global _long_text
    if _long_text is None:
        with open(abs_path("texts/荷塘月色.txt"), encoding="utf-8") as f:
            _long_text = f.read()
    return _long_text


def get_default_font(size):
    return PIL.ImageFont.truetype(
        font=abs_path("fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"),
        size=size,
    )
