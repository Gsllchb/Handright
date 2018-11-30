# coding: utf-8
"""A wrapper for Pillow Image Object"""
from typing import *

import PIL.Image
import PIL.ImageDraw


# You may think dynamic attribute attachment is a more pythonic solution, but,
# at least here, actually a more problematic one.
class Page(object):
    """A simple wrapper for Pillow Image Object"""

    __slots__ = ("image", "num")

    def __init__(
            self,
            mode: str,
            size: Tuple[int, int],
            color,
            num: int
    ) -> None:
        self.image = PIL.Image.new(mode, size, color)
        self.num = num

    def draw(self):
        return PIL.ImageDraw.Draw(self.image)

    @property
    def matrix(self):
        return self.image.load()

    @property
    def size(self) -> Tuple[int, int]:
        return self.image.size

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height
