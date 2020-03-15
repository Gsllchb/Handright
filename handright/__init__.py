# coding: utf-8
"""A lightweight Python library for simulating Chinese handwriting

Created by Chenghui Li (Gsllchb).

Licensed under BSD 3-Clause.
"""
from handright._core import handwrite
from handright._exceptions import Error, LayoutError, BackgroundTooLargeError
from handright._template import Template

__version__ = "5.4.0"

__all__ = (
    "handwrite",
    "Template",
    "Error",
    "LayoutError",
    "BackgroundTooLargeError"
)
