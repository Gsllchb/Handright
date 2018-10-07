# coding: utf-8
"""
This module provides the essential functionality for the whole test suite.
WARNING: Do not change the location of this file!
"""
import os

import PIL.ImageFont


def diff_histogram(image1, image2) -> float:
    """Return the ratio of the difference of the two images."""
    if image1.mode != image2.mode or image1.size != image2.size:
        raise ValueError("image1 and image2 must have same mode and same size")
    h1 = image1.histogram()
    h2 = image2.histogram()
    assert len(h1) == len(h2)
    summation = 0
    difference = 0
    for i1, i2 in zip(h1, h2):
        difference += abs(i1 - i2)
        summation += i1 + i2
    return difference / summation


def equal(image1, image2) -> bool:
    return image1.tobytes() == image2.tobytes()


def abs_path(path: str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


def get_short_text() -> str:
    """ Return one short sentence """
    return "我能吞下玻璃而不伤身体。"


def get_long_text() -> str:
    """ Return a article """
    with open(abs_path("texts/荷塘月色.txt"), encoding='utf-8') as f:
        return f.read()


def get_default_font():
    return PIL.ImageFont.truetype(abs_path("fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"))
