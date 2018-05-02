"""
This module provides the essential functionality for the whole test suite.
"""
import math


def compare_histogram(image1, image2) -> float:
    """
    Compare the two images and return the root mean square in histogram
    This algorithm is inspired by the discussion of 'Compare two images the python/linux way' in Stackoverflow
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
    # TODO
    pass
