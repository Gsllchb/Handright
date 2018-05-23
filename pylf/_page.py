"""A wrapper for Pillow Image Object"""
from PIL import Image
from PIL import ImageDraw


class Page(object):
    """A simple wrapper for Pillow Image Object"""

    def __init__(self, mode: str, size: tuple, color, index: int = None):
        self.image = Image.new(mode, size, color)
        self.index = index

    @property
    def draw(self):
        return ImageDraw.Draw(self.image)

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
