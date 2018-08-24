# coding: utf-8
"""A customized data structure for perturbation algorithm"""
import array


class NumericOrderedSet(object):
    """This data structure only support storing numeric elements"""

    def __init__(self, typecode: str, flag):
        """More info about typecode: https://docs.python.org/3/library/array.html#module-array
        The value of flag must be within the typecode's range. Flag is invisible in set operations, but it will appear
        in the ordered sequence."""
        self._typecode = typecode
        self._flag = flag
        self._array = array.array(typecode)
        self._set = set()

    def add(self, item) -> bool:
        """This has no effect and would return False if the item is already present"""
        assert item != self._flag
        if item in self._set:
            return False
        self._set.add(item)
        self._array.append(item)
        return True

    def add_flag(self) -> None:
        self._array.append(self._flag)

    def __contains__(self, item) -> bool:
        return item in self._set

    def __iter__(self):
        return iter(self._array)

    def clear(self) -> None:
        self._set.clear()
        self._array = array.array(self._typecode)

    def __len__(self):
        return len(self._array)

    @property
    def typecode(self) -> str:
        return self._typecode

    @property
    def flag(self):
        return self._flag
