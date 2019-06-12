# Tutorial
本文讲述如何生成并打印出足以媲美真人手写的文档。

### 排版参数关系图
![](images/params_visualizing.png)

### 字体大小（font_size）
为了发挥出PyLf的优异效果，您需要设置较大的字体大小。往往设置越大的字体大小，生成的字形越平滑，锯齿越少。但是越大的字体大小往往需要越大的背景图片，计算量和内存占用也就越大。推荐从`80`开始尝试。

### 字体填充（fill）
强烈建议若无特殊需要不要使用除纯黑外的其它颜色。黑色是打印机中最常见的颜色，它有对应颜色的墨水。而灰色和除个别颜色外的彩色都是需要多种颜色墨水和背景的白色调和形成的。

### 字体（font）
推荐使用的字体本身也是仿手写的字体。

### 背景（background）
因为新版本需要设置较大的字体大小，所以舞台（背景图片）也要更大。

如果您使用空背景，可以使用Pillow生成合适大小的背景，对于黑白打印
```python
from PIL import Image
background = Image.new(mode="1", size=(2048, 2048), color=1)
```
如果字体为灰色，`mode`可改为`"L"`。如果字体为彩色，`mode`可改为`CMYK`。

然而，大多数情况下我们使用的是自定义背景。往往我们要用的背景图片又不够大，此时我们需要对图片做适当的放大处理。
```python
width, height = background.size
background = background.resize(
    (width * 2, height * 2), resample=Image.LANCZOS
)
```
另外，如果您使用的是彩色背景，但最终又是黑白打印，推荐将背景图片提前转换为灰度图片以减少计算开销。
```python
background = background.convert(mode="L")
```

### 字间距（word_spacing）
有时，即使`word_spacing == 0`也会遇到字间距不够小的情况。此时，您可以将`word_spacing`设为负数以使得字间距更小。

### 随机参数（*_sigma)
虽然上述随机参数是可选参数，但是仍建议您不要使用默认值，而是根据所需模仿手写特点设置合适的值。

## 并行加速（mapper)
`mapper`是在页面渲染过程中使用的映射函数。其默认使用内置的`map`函数。您可以将其更换为其它更高效的实现，例如：
```python
from multiprocessing import Pool

from pylf import *

if __name__ == "__main__":
    text = "我能吞下玻璃而不伤身体。"
    template = ...
    with Pool() as p:
        images = handwrite(text, template, mapper=p.map)
    ...

```
