# Release Notes
本文档是为了让用户了解新版本的变化而撰写。新特性的添加、旧特性的删除、重大bug的修复以及不兼容性的变化等需要用户知道的重大变化在下文中将使用粗体标注。对于一般用户而言，仅需查看粗体部分即可。但还是建议闲得没事、充满好奇心或想全面了解新版本的用户看完所有新变化。


## unreleased
本版本对接口做了重新设计，使得接口的易用性和可读性更高，但也不可避免地**破坏了后向兼容性**。其次，为了对打印更加友好，废除了抗锯齿特性。因此为了获得与之前同等或更高的效果，您需要使用更高分辨率的背景图片或对原来的背景图片进行适当的放大处理。另外，更重要的是，本版本使用了全新的扰动算法，在消除之前扰动算法弊端的同时，使生成图片更具手写特征。
* __取消对Python3.4的支持__
* __使用全新扰动算法，废除旧扰动算法相关参数`alpha`，添加新扰动算法相关参数perturb_x_sigma、perturb_y_sigma和perturb_theta_sigma，详情请看API文档。__
* __大幅调整`template2`的内部结构，详情请看API文档。__
* __参数`line_spacing`的含义由相邻两行的间隙（某行字的上端与其上一行字的下端的距离）改为相邻两行的间距（某行字的上端与其上一行字的上端的距离）；并移除其默认值，使之不再是可选参数。__
* __参数`is_half_char`和`is_end_char`分别改名为`is_half_char_fn`和`is_end_char_fn`。__
* __移除参数`box`，取而代之以新参数`margin`来限定手写区域, 详情请看API文档。__
* __废除参数`worker`可为非正数的特性，但默认值保持不变。__
* __废除抗锯齿特性，移除可选参数`anti_aliasing`。__
* __`handwrite()`和`handwrite2()`的可选参数（即：`worker`和`seed`）改为强制以keyword的形式传入__
* __为使排版更合理，调整竖直方向上的排版方式。由`margin["top"] + font_size + GAP + ... + font_size + GAP + margin["bottom"]`的方式改为`margin["top"] + GAP + font_size + ... + GAP + font_size + margin["bottom"]`的方式，其中`GAP`为相邻两行字间的间隙宽度。__
* __增加`word_spacing`必须大于`-font_size // 2`的限制。__
* 添加参数检查，提供更友好的异常信息


## v1.4.0 (2018-7-30)
* __参数`seed`的类型由必须为`int`改为可为任一`hashable`__
* __提供参数`color`对所有[Pillow Color Name](https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names)的支持__
* 完善文档
* 轻微提升`handwrite()`和`handwrite2()`的性能


## v1.3.0 (2018-7-23)
* 移除source distribution中的`docs`文件夹
* __提供对Python3.7的支持，为此依赖项由`pillow >= 5.0.0, < 6`改为`pillow >= 5.2.0, < 6`__


## v1.2.0 (2018-6-1)
* __函数`handwrite`和`handwrite2`添加新可选参数`seed`，使得在设置了`seed`的情况下，结果具有可重复性__
* docstring改为Google风格
* 添加对Python3.4的支持
* 取消Python版本必须小于3.7的限制（但目前尚不对Python3.7及以上版本做任何官方支持）
* __提供对pydoc更好的支持__
* 所有Python源文件显式标注为使用UTF-8编码


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
* __添加`pylf.handwrite2`，以使得满足背景图片需周期性变化的需求。详情请参阅 _Reference_。__
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
* __修复当生成图片数超过`worker`时文字出现大范围重叠的漏洞__


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
