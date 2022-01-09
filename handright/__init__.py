# coding: utf-8
"""A lightweight Python library for simulating Chinese handwriting

Created by Chenghui Li (Gsllchb).

Licensed under BSD 3-Clause.

A minimal example:
```
text = "我能吞下玻璃而不伤身体。"
template = Template(
    background=PIL.Image.new(mode="1", size=(1024, 2048), color=1),
    font_size=100,
    font=PIL.ImageFont.truetype("path/to/my/font.ttf"),
)
images = handwrite(text, template)
```

As can be seen, Handright is built on the top of Pillow. `handwrite`, as the
core function, implements the feature of simulating handwriting, and `Template`
is the auxiliary parameter class. The return value of `handwrite` is an
`Iterable` of Pillow `Image`, so the images can be shown, saved, or further
processed.
"""
from handright._core import handwrite
from handright._exceptions import Error, LayoutError, BackgroundTooLargeError
from handright._template import Template, Feature

__version__ = "8.0.0"

__all__ = (
    "handwrite",
    "Template",
    "Feature",
    "Error",
    "LayoutError",
    "BackgroundTooLargeError"
)
