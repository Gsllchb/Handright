# coding: utf-8
"""A customized data structure for perturbation algorithm"""
import array


class NumericOrderedSet(object):
    """This data structure only support storing numeric elements"""

    def __init__(self, typecode: str):
        """More info about typecode: https://docs.python.org/3/library/array.html#module-array"""
        self._typecode = typecode
        self._array = array.array(typecode)
        self._set = set()

    def add(self, item) -> bool:
        """This has no effect and would return False if the item is already present"""
        if item in self._set:
            return False
        self._set.add(item)
        self._array.append(item)
        return True

    def __contains__(self, item) -> bool:
        return item in self._set

    def __iter__(self):
        return iter(self._array)

    def clear(self) -> None:
        self._set.clear()
        self._array = array.array(self._typecode)

    def __len__(self):
        assert len(self._array) == len(self._set)
        return len(self._array)

    @property
    def typecode(self) -> str:
        return self._typecode
