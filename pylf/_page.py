# coding: utf-8
"""A wrapper for Pillow Image Object"""
from PIL import Image as image
from PIL import ImageDraw as image_draw


class Page(object):
    """A simple wrapper for Pillow Image Object"""
    __slots__ = ("image", "num")

    def __init__(self, mode: str, size: tuple, color, num: int):
        self.image = image.new(mode, size, color)
        self.num = num

    @property
    def draw(self):
        return image_draw.Draw(self.image)

    @property
    def matrix(self):
        return self.image.load()

    @property
    def size(self) -> tuple:
        return self.image.size

    @property
    def width(self) -> int:
        return self.image.size[0]

    @property
    def height(self) -> int:
        return self.image.size[1]
