# PyLf
___A lightweight Python library for simulating Chinese handwriting___

[![released version](https://img.shields.io/pypi/v/PyLf.svg)][pypi]
[![python version](https://img.shields.io/pypi/pyversions/PyLf.svg)][pypi]
[![license](https://img.shields.io/github/license/Gsllchb/PyLf.svg)][license]
[![build status](https://travis-ci.org/Gsllchb/PyLf.svg?branch=master)](https://travis-ci.org/Gsllchb/PyLf)
[![downloads](https://img.shields.io/pypi/dm/PyLf.svg)](https://pypistats.org/packages/pylf)

[Tutorial][tutorial] |
[Examples][examples] |
[Release Notes][release-notes] |
[Contributing][contributing]

![](https://github.com/Gsllchb/PyLf/blob/master/docs/images/slogan.png)

## Vision
Reveal the nature of Chinese handwriting and use it to implement beautiful, simple and easy-to-use interfaces.

## Algorithm
首先，在水平位置、竖直位置和字体大小三个自由度上，对每个字的整体做随机扰动。随后，在水平位置、竖直位置和旋转角度三个自由度上，对每个字的每个笔画做随机扰动。

## Installation
```console
pip install pylf
```

## Quick Start
```python
from PIL import Image, ImageFont

from pylf import *

text = "我能吞下玻璃而不伤身体。"
template = Template(
    background=Image.new(mode="1", size=(1024, 2048), color=1),
    line_spacing=150,
    font_size=100,
    font=ImageFont.truetype("path/to/my/font.ttf"),
)
for image in handwrite(text, template):
    image.show()

```
更多信息请参阅[Tutorial][tutorial]。

## Gallery
* [前出师表.py](https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v3/%E5%89%8D%E5%87%BA%E5%B8%88%E8%A1%A8.py)

![前出师表](https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v3/out/%E5%89%8D%E5%87%BA%E5%B8%88%E8%A1%A8.png)


[tutorial]: https://github.com/Gsllchb/PyLf/blob/master/docs/tutorial.md
[PIL]: http://www.pythonware.com/products/pil/
[Pillow]: http://python-pillow.org/
[examples]: https://github.com/Gsllchb/PyLf-examples
[release-notes]: https://github.com/Gsllchb/PyLf/blob/master/docs/release_notes.md
[pypi]: https://pypi.org/project/pylf/
[license]: https://github.com/Gsllchb/PyLf/blob/master/LICENSE
[contributing]: https://github.com/Gsllchb/PyLf/blob/master/.github/CONTRIBUTING.md
