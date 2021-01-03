# coding: utf-8
import array
import collections.abc
import random
from typing import *

import PIL.Image
import PIL.ImageDraw


def gauss(rand: random.Random, mu, sigma):
    if sigma == 0:
        return mu
    return rand.gauss(mu, sigma)


def count_bands(mode: str) -> int:
    return sum(not c.islower() for c in mode)


# You may think dynamic attribute attachment is a more pythonic solution, but,
# at least here, actually is a more buggy one.
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

    def matrix(self):
        return self.image.load()

    def size(self) -> Tuple[int, int]:
        return self.image.size

    def width(self) -> int:
        return self.image.width

    def height(self) -> int:
        return self.image.height


class NumericOrderedSet(collections.abc.Collection):
    """A mutable set storing numeric value that remembers its elements insert
    order. Note that, this data structure has not implemented the full
    interfaces of collections.abc.MutableSet or collections.abc.Set. For
    simplicity, it only implements collections.abc.Collection, add method and
    other customized methods."""

    __slots__ = ("_typecode", "_privileged", "_array", "_set")

    def __init__(self, typecode: str, privileged=None) -> None:
        """More info about typecode: https://docs.python.org/3/library/array.html#module-array
        The value of privileged must be within the typecode's range. The
        privileged can be successfully added more than one time to this data
        structure and appear more than one time in the ordered sequence."""
        self._typecode = typecode
        self._privileged = privileged
        self._array = array.array(typecode)
        self._set = set()

    def add(self, item) -> bool:
        """This has no effect and would return False if the item is not equal to
        privileged and already present. Otherwise, it will adds the item and
        returns True."""
        if item != self._privileged and item in self._set:
            return False
        self._set.add(item)
        self._array.append(item)
        return True

    def add_privileged(self) -> None:
        """Equivalent to add(privileged)"""
        self._set.add(self._privileged)
        self._array.append(self._privileged)

    def __contains__(self, item) -> bool:
        return item in self._set

    def __iter__(self):
        return iter(self._array)

    def clear(self) -> None:
        self._set.clear()
        self._array = array.array(self._typecode)

    def __len__(self) -> int:
        """The length of ordered sequence"""
        return len(self._array)

    def typecode(self) -> str:
        return self._typecode

    def privileged(self):
        return self._privileged
