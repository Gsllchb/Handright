# coding: utf-8
def count_bands(mode: str) -> int:
    return sum(not c.islower() for c in mode)
