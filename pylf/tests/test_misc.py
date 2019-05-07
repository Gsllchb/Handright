# coding: utf-8
from pylf._misc import *


def test_count_bands():
    assert count_bands("1") == 1
    assert count_bands("L") == 1
    assert count_bands("P") == 1
    assert count_bands("RGB") == 3
    assert count_bands("RGBA") == 4
    assert count_bands("CMYK") == 4
    assert count_bands("YCbCr") == 3
    assert count_bands("LAB") == 3
    assert count_bands("HSV") == 3
    assert count_bands("I") == 1
    assert count_bands("F") == 1
