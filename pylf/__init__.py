# coding: utf-8
"""A lightweight Python library for simulating Chinese handwriting

Vision: Reveal the nature of Chinese handwriting and use it to implement
beautiful, simple and easy-to-use interfaces.

Algorithm: Randomly perturb each character as a whole in horizontal position,
vertical position and font size. Then, Randomly perturb each stroke of a
character in horizontal position, vertical position and rotation angle.

Implementation: Develop on the top of Pillow and use multiprocessing for
internal parallel acceleration.

Homepage: https://github.com/Gsllchb/PyLf
"""
from pylf.core import handwrite, Template, Error, LayoutError, BackgroundTooLargeError

__version__ = "4.0.0.dev0"
