# PyLf
![](examples/out/motto.png)

PyLf是一个轻量级模仿中文手写的Python库，其通过在处理过程中大量引入随机性来模仿汉字书写。


## Installation
由于PyLf的依赖项[Pillow][Pillow-homepage]会与[PIL][PIL-homepage]发生冲突，如若您已安装[PIL][PIL-homepage]，请先**手动卸载**：
```commandline
pip uninstall PIL
```
此外如若您并未安装[setuptools][setuptools-homepage],请先**手动安装**：
```commandline
pip install setuptools
```
安装PyLf：
```commandline
pip install pylf
```


## Quickstart
```python
from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support  # 非Windows用户可删除此行


def main():
    template = dict(
        background=Image.new(mode='RGB', size=(800, 1000), color='rgb(255, 255, 255)'),
        box=(100, 200, 700, 800),
        font=ImageFont.truetype("YOUR FONT PATH"),  # 填入您所使用字体文件的路径
        font_size=50,
    )
    text = "我能吞下玻璃而不伤身体。"
    images = handwrite(text, template)
    for image in images:
        image.show()


if __name__ == '__main__':
    freeze_support()  # 非Windows用户可删除此行
    main()
    
```
如以上代码所示，函数`pylf.handwrite`是整个PyLf库的核心。而模板`template`则是本库的一个重要概念。模板包含着在手写模仿过程中所需的背景、排版设置、
字体、随机性强度等参数。这些参数通常因背景图和用户书写习惯的不同而不同。有关`handwrite`和`template`的更多可选参数请参阅
[API Reference](docs/API-Reference.md)。一般情况下，在第一次使用某个背景时，您需要根据自己的手写特征创建特定的模板（往往需要经历不断的调试）。

另外，请您在更新PyLf后及时参阅[Release Notes](NEWS.md)，以了解新版本的变化，特别是在主版本更新的时候（其中往往蕴含着不后向兼容的改动）。


## Examples
**注**：以下某些图片中之所以缺少个别字，是因为所使用生成该图片的字体本身缺少这些字。

* __《荷塘月色》__ <br>

示例代码：[examples/article.py](examples/article.py)

![](examples/out/荷塘月色.png)


* __《从百草园到三味书屋》__ <br>

示例代码：[examples/even_odd.py](examples/even_odd.py)

![](examples/out/从百草园到三味书屋.png)

# More
* [Windows用户需知](docs/more/Windows用户需知.md)


[PIL-homepage]: http://www.pythonware.com/products/pil/
[Pillow-homepage]: https://python-pillow.org/
[setuptools-homepage]: https://pypi.python.org/pypi/setuptools