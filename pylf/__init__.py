# coding: utf-8
"""A lightweight Python library for simulating Chinese handwriting

Vision: Reveal the nature of Chinese handwriting and use it to implement
beautiful, simple and easy-to-use interfaces.

Algorithm: Randomly perturb each character as a whole in horizontal position,
vertical position and font size. Then, Randomly perturb each stroke of a
character in horizontal position, vertical position and rotation angle.

Homepage: https://github.com/Gsllchb/PyLf
"""
from pylf._core import handwrite, Template, Error, LayoutError, BackgroundTooLargeError

__version__ = "4.0.0"
