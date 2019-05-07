# coding: utf-8
from pylf import _misc


def test_count_bands():
    assert _misc.count_bands("1") == 1
    assert _misc.count_bands("L") == 1
    assert _misc.count_bands("P") == 1
    assert _misc.count_bands("RGB") == 3
    assert _misc.count_bands("RGBA") == 4
    assert _misc.count_bands("CMYK") == 4
    assert _misc.count_bands("YCbCr") == 3
    assert _misc.count_bands("LAB") == 3
    assert _misc.count_bands("HSV") == 3
    assert _misc.count_bands("I") == 1
    assert _misc.count_bands("F") == 1
