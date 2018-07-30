# coding: utf-8
"""
This module provides the essential functionality for the whole test suite.
WARNING: Do not change the location of this file!
"""
import math
import os

from PIL import ImageFont as image_font


THRESHOLD = 17.0


def compare_histogram(image1, image2) -> float:
    """
    Compare the two images and return the root mean square in histogram
    This algorithm is inspired by the discussion about "Compare two images the python/linux way" in Stackoverflow
    """
    if image1.mode != image2.mode or image1.size != image2.size:
        raise ValueError("image1 and image2 must have same mode and same size")
    h1 = image1.histogram()
    h2 = image2.histogram()
    assert len(h1) == len(h2)
    s = 0
    for c1, c2 in zip(h1, h2):
        s += (c1 - c2) ** 2
    return math.sqrt(s / len(h1))


def absolute_equal(image1, image2) -> bool:
    return image1.tobytes() == image2.tobytes()


def compare_pixel(image1, image2) -> float:
    """ Compare the two images pixel by pixel and return the root mean square """
    raise NotImplementedError("do not need yet")


def get_path(path:str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


def get_short_text() -> str:
    """ Return one short sentence """
    return "我能吞下玻璃而不伤身体。"


def get_long_text() -> str:
    """ Return a article """
    with open(get_path("data/texts/荷塘月色.txt"), encoding='utf-8') as f:
        return f.read()


def get_default_font():
    return image_font.truetype(get_path("data/fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"))
