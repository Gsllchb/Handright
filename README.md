# Handright
___A lightweight Python library for simulating Chinese handwriting___

[![released version](https://img.shields.io/pypi/v/Handright.svg)][pypi]
[![python version](https://img.shields.io/pypi/pyversions/Handright.svg)][pypi]
[![license](https://img.shields.io/github/license/Gsllchb/Handright.svg)][license]
[![downloads](https://img.shields.io/pypi/dm/Handright.svg)](https://pypistats.org/packages/handright)

![Test on Linux](https://github.com/Gsllchb/Handright/workflows/Test%20on%20Linux/badge.svg)
![Test on Windows](https://github.com/Gsllchb/Handright/workflows/Test%20on%20Windows/badge.svg)
![Test on MacOS](https://github.com/Gsllchb/Handright/workflows/Test%20on%20MacOS/badge.svg)

[Tutorial][tutorial] |
[Release Notes][release-notes] |
[Contributing][contributing]

![](https://github.com/Gsllchb/Handright/blob/master/docs/images/slogan.png)

## Vision
Reveal the nature of Chinese handwriting and use it to implement beautiful, simple and easy-to-use interfaces.

## Algorithm
首先，在水平位置、竖直位置和字体大小三个自由度上，对每个字的整体做随机扰动。随后，在水平位置、竖直位置和旋转角度三个自由度上，对每个字的每个笔画做随机扰动。

## Installation
```console
pip install handright
```

## Quick Start
```python
# coding: utf-8
from PIL import Image, ImageFont

from handright import Template, handwrite

text = "我能吞下玻璃而不伤身体。"
template = Template(
    background=Image.new(mode="1", size=(1024, 2048), color=1),
    font_size=100,
    font=ImageFont.truetype("path/to/my/font.ttf"),
)
images = handwrite(text, template)
for im in images:
    assert isinstance(im, Image.Image)
    im.show()

```
更多信息请参阅[Tutorial][tutorial]。


[tutorial]: https://github.com/Gsllchb/Handright/blob/master/docs/tutorial.md
[PIL]: http://www.pythonware.com/products/pil/
[Pillow]: http://python-pillow.org/
[release-notes]: https://github.com/Gsllchb/Handright/blob/master/docs/release_notes.md
[pypi]: https://pypi.org/project/handright/
[license]: https://github.com/Gsllchb/Handright/blob/master/LICENSE
[contributing]: https://github.com/Gsllchb/Handright/blob/master/.github/CONTRIBUTING.md
