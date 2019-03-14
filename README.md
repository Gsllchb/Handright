# PyLf
___A lightweight Python library for simulating Chinese handwriting___

[![released version](https://img.shields.io/pypi/v/PyLf.svg)][pypi]
[![python version](https://img.shields.io/pypi/pyversions/PyLf.svg)][pypi]
[![implementation](https://img.shields.io/pypi/implementation/PyLf.svg?label=impl)][pypi]
[![license](https://img.shields.io/github/license/Gsllchb/PyLf.svg)][license]
[![build status](https://travis-ci.org/Gsllchb/PyLf.svg?branch=master)](https://travis-ci.org/Gsllchb/PyLf)
[![downloads](https://img.shields.io/pypi/dm/PyLf.svg)](https://pypistats.org/packages/pylf)

[Tutorial][tutorial] |
[Examples][examples] |
[Release Notes][release-notes] |
[Contributing][contributing] |
[Donation](https://gsllchb.github.io/donation/)

![](https://github.com/Gsllchb/PyLf/blob/master/docs/images/slogan.png)

## Vision
Reveal the nature of Chinese handwriting and use it to implement beautiful, simple and easy-to-use interfaces.

## Algorithm & Implementation
首先，在水平位置、竖直位置和字体大小三个自由度上，对每个字的整体做随机扰动。随后，在水平位置、竖直位置和旋转角度三个自由度上，对每个字的每个笔画做随机扰动。

目前，PyLf基于[Pillow][Pillow]开发，并在内部使用[multiprocessing](https://docs.python.org/3.4/library/multiprocessing.html)做并行加速。

## Installation
```console
pip install pylf
```

## Quick Start
```python
from PIL import Image, ImageFont
from pylf import handwrite


if __name__ == '__main__':
    template = {
        "background": Image.new(mode="1", size=(2000, 2000), color="white"),
        "margin": {"left": 150, "right": 150, "top": 200, "bottom": 200},
        "line_spacing": 150,
        "font_size": 100,
        "font": ImageFont.truetype("path/to/my/font.ttf")
    }
    for image in handwrite("我能吞下玻璃而不伤身体。", template):
        image.show()
```
对于简单的手写任务，您可以使用更易用的CLI工具。请尝试在终端中运行`pylf --help`。

更多信息请参阅[Tutorial][tutorial]。

## Features
| 特性                                        | 相关参数                                                  |
|:------------------------------------------- |:------------------------------------------------------- |
| 设置背景                                     | background                                              |
| 设置字体及其大小、颜色                         | font, font_size, color                                  |
| 设置页边距、行间距、字间距                     | margin, line_spacing, word_spacing                       |
| 调节排版随机化的强弱                           | font_size_sigma, line_spacing_sigma, word_spacing_sigma |
| 调节笔画随机扰动的强弱                         | perturb_x_sigma, perturb_y_sigma, perturb_theta_sigma   |
| 设置在行末不换行的字符集（如：`。》)]`）         | is_end_char_fn                                          |
| 设置在排版时只占其宽度一半的字符集（如：`，。！`） | is_half_char_fn                                         |
| 并行加速                                     | worker                                                   |
| 周期性模板                                    | template2（详情：pylf.handwrite2）                       |

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
