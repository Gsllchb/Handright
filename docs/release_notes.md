# Release Notes
以下**粗体部分**标注不后向兼容的改动。

## v8.0.0 (2022-1-9)
* __Bump pillow from `>= 8.1.1, < 9` to `>= 8.3.2, < 10`.__
* __Drop Python3.6 support, add Python3.10 support.__

## v7.0.0 (2021-4-4)
* __移除Template.font_size参数，字体大小改为使用Template.font.size承载。__
* __依赖变更`pillow >= 8.1.1, < 9`__
* 【试验特性】新增Template.features，支持额外特性配置，目前支持特性：网格布局。

## v6.0.0 (2020-10-18)
* 提供对Python3.9的支持
* __停止对Python3.5的支持__
* __Pillow的依赖范围修改为`>= 8.0.0, < 9`。__

## v5.5.0 (2020-3-21)
* 优化API文档：适配pydoc，提供更详细的概述，以及给出各异常触发条件的明确描述。

## v5.4.0 (2020-1-31)
* __*Pillow*的依赖范围修改为`>= 6.2.1, < 8`。__
* 提供更详细的异常错误信息。
* 优化性能。
* 微调排版算法。

## v5.3.0 (2019-12-1)
* 新增对Python3.8的官方支持。
* 新增对换行符CR（`\r`）和CRLF（`\r\n`）的支持。
* 修改Handright库docstring的描述。
* 更新作者信息。

## v5.2.0 (2019-10-20)
* 优化function annotations。
* 类`Template`添加`release_font_resource`和`__repr__`方法，`__slots__`属性。

## v5.1.0 (2019-8-10)
* 为模板类`Template`添加新方法`get_size()`。

## v5.0.0 (2019-7-21)
* __将项目名由`PyLf`改为`Handright`，包名由`pylf`改为`handright`。__

## v4.1.0 (2019-7-7)
* 为`line_spacing`提供缺省值，取值`font_size`。

## v4.0.0 (2019-6-12)
__本次大更新重构了接口，但核心算法并未改变。__
* __创建模板类`Template`，用于管理模板相关参数。__
* __修改`handwrite()`的接口，使其接收`Template`类的实例。__
* __将`handwrite2()`合并入`handwrite()`__
* __废除参数`worker`，并添加新参数`mapper`。__
* __移除参数`is_half_char_fn`以及相对应的常量`DEFAULT_HALF_CHARS`__
* __将参数`is_end_char_fn`替换为新参数`end_chars`，废除常量`DEFAULT_END_CHARS`。__
* __将参数`color`替换为新参数`fill`__
* __取消背景图片的`mode`限制，提供对全部`mode`的支持。__
* __移除CLI工具__
* __停止对PyPy的官方支持__
* 取消`seed`必须以`keyword`形式传入的限制
* 创建PyLf的基异常类`Error`，并将`LayoutError`改为直接继承自该异常类。
* 创建新异常类`BackgroundTooLargeError`

## v3.4.0 (2019-5-1)
* Pillow版本限制放宽至`>= 5, < 7`

## v3.3.2 (2019-4-8)
* 修复已知的bug

## v3.3.1 (2019-4-5)
* 细微优化function annotation

## v3.3.0 (2019-3-16)
* 提供对PyPy的官方支持

## v3.2.3 (2019-3-8)
* 每行最大字符数限制由80改为120。
* 修复在某些边界条件下，换行和换页过早的问题。

## v3.2.2 (2019-2-13)
* 将`LICENSE.txt`嵌入到二进制发行版中。

## v3.2.1 (2019-1-11)
* 将Pyyaml版本限制改为`>= 3.13, < 5`
* 轻微提升性能。
* 硬编码CLI工具的程序名。

## v3.2.0 (2018-12-31)
* 为简单的手写任务推出CLI工具。请尝试在命令行中运行`pylf --help`。
* 添加新常量`DEFAULT_HALF_CHARS`和`DEFAULT_END_CHARS`

## v3.1.0 (2018-11-26)
* Issue `UserWarning` while `worker > multiprocessing.cpu_count()`
* 完善文档

## v3.0.0 (2018-10-26)
本次更新是多个不后向兼容的小更新与其余更新的集合。
* __添加异常类`pylf.LayoutError`，当传入有关排版的参数不合理，程序无法根据这些参数进行排版时取代原异常`ValueError`抛出。__
* 使用[typing](https://docs.python.org/3/library/typing.html)描述接口，提供对[mypy](https://github.com/python/mypy)的支持。
* __当背景图片的`mode`不是`1`, `L`, `RGB`和`RGBA`之一时，将抛出`NotImplementedError`。__
* 当`worker == 1`时，改为使用单线程算法。
* __`text`的类型改为仅可以为`str`__
* 修复当使用非灰度背景，设置字体颜色为彩色时，生成图片中字迹为灰色的漏洞。
* 修复异常信息中的bug，并使异常信息更友好
* 去除示例代码中的`freeze_support()`。
* `worker`改为可为`None`，此时`worker`取默认值。
* 提供更恰当的参数检查
* Local multiprocessing context is used.
* 细微修改示例代码

## v2.1.0 (2018-9-20)
* 大幅提升生成图片只有一张时的性能

## v2.0.0 (2018-8-30)
本版本使用了全新的扰动算法，在消除之前扰动算法弊端的同时，使生成图片达到了令人惊艳的逼真效果。其次，本版本对接口做了重新设计，使得接口的易用性和可读性更高，但也不可避免地**破坏了后向兼容性**。另外，为了对打印更加友好，废除了抗锯齿特性。因此为了获得与之前同等或更高的效果，您需要使用更高分辨率的背景图片或对原来的背景图片进行适当的放大处理。
* __使用全新扰动算法，废除旧扰动算法相关参数`alpha`，添加新扰动算法相关参数perturb_x_sigma、perturb_y_sigma和perturb_theta_sigma，详情请看API文档。__
* __取消对Python3.4的支持__
* __大幅调整`template2`的内部结构，详情请看API文档。__
* __参数`line_spacing`的含义由相邻两行的间隙（某行字的上端与其上一行字的下端的距离）改为相邻两行的间距（某行字的上端与其上一行字的上端的距离）；并移除其默认值，使之不再是可选参数。__
* __参数`is_half_char`和`is_end_char`分别改名为`is_half_char_fn`和`is_end_char_fn`。__
* __移除参数`box`，取而代之以新参数`margin`来限定手写区域, 详情请看API文档。__
* __废除参数`worker`可为非正数的特性，但默认值保持不变。__
* __废除抗锯齿特性，移除可选参数`anti_aliasing`。__
* __`handwrite()`和`handwrite2()`的可选参数（即：`worker`和`seed`）改为强制以keyword的形式传入__
* __为使排版更合理，调整竖直方向上的排版方式。由`margin["top"] + font_size + GAP + ... + font_size + GAP + margin["bottom"]`的方式改为`margin["top"] + GAP +font_size + ... + GAP + font_size + margin["bottom"]`的方式，其中`GAP`为相邻两行字间的间隙宽度。__
* __增加`word_spacing`必须大于`-font_size // 2`的限制。__
* 添加参数检查，提供更友好的异常信息。
* 提供更详尽的文档。

## v1.4.0 (2018-7-30)
* 参数`seed`的类型由必须为`int`改为可为任一`hashable`。
* 提供参数`color`对所有[Pillow Color Name](https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names)的支持。
* 完善文档
* 轻微提升`handwrite()`和`handwrite2()`的性能

## v1.3.0 (2018-7-23)
* 移除source distribution中的`docs`文件夹
* __提供对Python3.7的支持，为此依赖项由`pillow >= 5.0.0, < 6`改为`pillow >= 5.2.0, < 6`。__

## v1.2.0 (2018-6-1)
* 函数`handwrite`和`handwrite2`添加新可选参数`seed`，使得在设置了`seed`的情况下，结果具有可重复性。
* docstring改为Google风格。
* 添加对Python3.4的支持。
* 取消Python版本必须小于3.7的限制（但目前尚不对Python3.7及以上版本做任何官方支持）。
* 提供对pydoc更好的支持。
* 所有Python源文件显式标注为使用UTF-8编码。

## v1.1.4 (2018-5-14)
* 添加安装依赖项`setuptools>=38.6.0`
* description改为README.md的内容
* 修复当`template['font_size'] == 0`时触发`ZeroDivisionError`的漏洞

## v1.1.3 (2018-3-30)
* 修复`setup.py`中的细微问题

## v1.1.2 (2018-3-25)
* 轻微提高当`worker`大于生成图片数时的性能
* 轻微提高在使用`is_end_char`默认参数下的性能

## v1.1.1 (2018-2-26)
* 将所需Python版本由`>=3.5, <3.8`改为`>=3.5, <3.7`, 以解决PyLf依赖项Pillow无法在某些平台上安装的问题。

## v1.1.0 (2018-2-25)
* 添加`pylf.handwrite2`，以使得满足背景图片需周期性变化的需求。详情请参阅 _Reference_。
* 改进下采样算法，使得在打开抗锯齿的情况下有更好的性能。注意：在同样的参数下(排除了随机性)，该新版本生成的图片与上一版本生成的图片并不会严格完全相同，但是人眼难以察觉出该区别。

## v1.0.0 (2018-1-25)
本版本对核心算法做了大幅改动，一方面使得效果更为逼真，另一方面使得性能得到大幅提升而内存占用大幅降低；但也使得接口发生了**不兼容**的改动。同时，本次更新也使得接口易用性得到大幅的提高。
* __`template`中的参数`color`由`tuple`类型改为特定格式的`str`__
* __废除`template`中的参数`x_amplitude`、`y_amplitude`、`x_wavelength`、`y_wavelength`、`x_lambd`和`y_lambd`__
* __将依赖项由`pillow >= 4.3.0`改为`5.0.0 <= pillow < 6`__
* 将`font_size / 256`作为`template`中`font_size_sigma`、`word_spacing_sigma`和`line_spacing_sigma`参数的缺省值
* __`template`添加新的参数`alpha`__
* 大幅提高性能，大幅减少内存占用
* __将`line_spacing`的含义改为两临近行间的间隙（即上一行字的下端和下一行字的上端的距离）的大小（以像素为单位），并将`font_size // 5`作为其缺省值__
* 完善文档

## v0.5.2 (2017-12-30)
* 将`0`作为`word_spacing`的缺省值
* 修复当生成图片数超过`worker`时文字出现大范围重叠的漏洞。

## v0.5.1 (2017-12-14)
* fix [#2](https://github.com/Gsllchb/PyLf/issues/2)

## v0.5.0 (2017-12-14)
* 改进算法使得参数`text`可为`iterable`

## v0.4.0 (2017-12-5)
* Add `ValueError` raised by `handwrite` to prevent dead loop in some corner cases
* 完善文档
* 将黑色作为`template`的缺省颜色
* __字体宽度从由`font_size`决定改为由每个字符自己的信息决定__
* 将`lambda c: False`作为`is_half_char`的缺省值
* 将是否在常见非开头字符集中作为`is_end_char`的缺省值
