# PyLf
___A lightweight Python library for simulating Chinese handwriting___

[![version](https://img.shields.io/pypi/v/PyLf.svg)][pypi-homepage]
[![python](https://img.shields.io/pypi/pyversions/PyLf.svg)][pypi-homepage]
[![implementation](https://img.shields.io/pypi/implementation/PyLf.svg)][pypi-homepage]
[![gitter](https://badges.gitter.im/Python-PyLf/PyLf.svg)](https://gitter.im/Python-PyLf/PyLf)
[![license](https://img.shields.io/github/license/Gsllchb/PyLf.svg)][license-link]
[![Build Status](https://travis-ci.org/Gsllchb/PyLf.svg?branch=master)](https://travis-ci.org/Gsllchb/PyLf)

[Tutorial][tutorial-link] |
[Examples][examples-homepage] |
[Release Notes][release-notes-link] |
[Contributing][contributing-link]

![](https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v2/out/slogan.png)


## Vision
Reveal the nature of Chinese handwriting and use it to implement beautiful, simple and easy-to-use interfaces.


## Algorithm & Implementation
首先，在水平位置、竖直位置和字体大小三个自由度上，对每个字的整体做随机扰动。随后，在水平位置、竖直位置和旋转角度三个自由度上，对每个字的每个笔画做随机扰动。

目前，PyLf基于[Pillow][Pillow-homepage]开发，并在内部使用[multiprocessing](https://docs.python.org/3.4/library/multiprocessing.html)做并行加速。


## Installation
由于PyLf的依赖项[Pillow][Pillow-homepage]会与[PIL][PIL-homepage]发生冲突，因此如若您已安装[PIL][PIL-homepage]，请先**手动卸载**：
```console
pip uninstall PIL
```
安装PyLf：
```console
pip install pylf
```


## Quick Start
```python
from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support  # 非Windows用户可删除此行


def main():
    template = {"background": Image.new(mode="1", size=(2000, 2000), color="white"),
                "margin": {"left": 150, "right": 150, "top": 200, "bottom": 200},
                "line_spacing": 150,
                "font_size": 100,
                "font": ImageFont.truetype("path/to/my/font.ttf")}
    for image in handwrite("我能吞下玻璃而不伤身体。", template):
        image.show()


if __name__ == '__main__':
    freeze_support()  # 非Windows用户可删除此行
    main()

```
请参阅[Tutorial][tutorial-link]。


## Features
|                         特性                        |               相关参数                                   |              
| :-------------------------------------------------- | :------------------------------------------------------ |
| 设置背景                                             | background                                              |
| 设置字体及其大小、颜色                                 | font, font_size, color                                  |
| 设置页边距、行间距、字间距                             | margin, line_spacing, word_spacing                       |
| 调节排版随机化的强弱                                   | font_size_sigma, line_spacing_sigma, word_spacing_sigma |
| 调节笔画随机扰动的强弱                                 | perturb_x_sigma, perturb_y_sigma, perturb_theta_sigma   |
| 设置在行末不换行的字符集（如：'。', '》', ')', ']'）     | is_end_char_fn                                          |
| 设置在排版时只占其宽度一半的字符集（如：'，', '。', '！'） | is_half_char_fn                                         |
| 并行加速                                             | worker                                                  |
| 周期性模板                                            | template2（详情：pylf.handwrite2）                       |


## Examples
**注**：以下某些图片中之所以缺少个别字，是因为所使用生成该图片的字体本身缺少这些字。

* __《荷塘月色》__

示例代码：[article.py](https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/article.py)

<div align="center">
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/荷塘月色/0.png" width="436" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/荷塘月色/1.png" width="436" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/荷塘月色/2.png" width="436" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/荷塘月色/3.png" width="436" />
</div>

* __《从百草园到三味书屋》__

示例代码：[even_odd.py](https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/even_odd.py)

<div align="center">
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/从百草园到三味书屋/0.png" width="174" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/从百草园到三味书屋/1.png" width="174" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/从百草园到三味书屋/2.png" width="174" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/从百草园到三味书屋/3.png" width="174" />
    <img src="https://github.com/Gsllchb/PyLf-examples/blob/master/examples/v1/out/从百草园到三味书屋/4.png" width="174" />
</div>

__欲查看更多示例请前往[PyLf-examples][examples-homepage]。__


[tutorial-link]: https://github.com/Gsllchb/PyLf/blob/master/docs/tutorial.md
[PIL-homepage]: http://www.pythonware.com/products/pil/
[Pillow-homepage]: http://python-pillow.org/
[examples-homepage]: https://github.com/Gsllchb/PyLf-examples
[release-notes-link]: https://github.com/Gsllchb/PyLf/blob/master/docs/release_notes.md
[pypi-homepage]: https://pypi.org/project/pylf/
[license-link]: https://github.com/Gsllchb/PyLf/blob/master/LICENSE
[contributing-link]: https://github.com/Gsllchb/PyLf/blob/master/.github/CONTRIBUTING.md
