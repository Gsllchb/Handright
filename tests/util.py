# coding: utf-8
"""
This module provides the essential functionality for the whole test suite.
WARNING: Do not change the location of this file!
"""
import os

import PIL.ImageFont


def abs_path(path: str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


def get_short_text() -> str:
    """ Return one short sentence """
    return "我能吞下玻璃而不伤身体。"


def get_long_text() -> str:
    """ Return a article """
    with open(abs_path("texts/荷塘月色.txt"), encoding="utf-8") as f:
        return f.read()


def get_default_font():
    return PIL.ImageFont.truetype(
        abs_path(
            "fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"
        )
    )
