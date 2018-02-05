# PyLf
[License](LICENSE) |
[Installation](docs/Installation.md) |
[API Reference](docs/API-Reference.md) |
[Release Notes](NEWS.md)

![](examples/out/motto.png)

PyLf是一个轻量级模仿中文手写的Python库，其通过在处理过程中大量引入随机性来模仿汉字书写。

## Quickstart

    from PIL import Image, ImageFont
    from pylf import handwrite
    from multiprocessing import freeze_support  # 非Windows用户可删除此行
    
    
    def main():
        template = dict(
            background=Image.new(mode='RGB', size=(800, 1000), color='rgb(255, 255, 255)'),
            box=(100, 200, 700, 800),
            font=ImageFont.truetype("./something.ttf"),
            font_size=50,
        )
        text = "我能吞下玻璃而不伤身体。"
        images = handwrite(text, template)
        for image in images:
            image.show()
    
    
    if __name__ == '__main__':
        freeze_support()  # 非Windows用户可删除此行
        main()


## Examples

* __“我能吞下玻璃而不伤身体。”__ <br>

示例代码：[examples/motto.py](examples/motto.py)

![](examples/out/motto.png)

* __《荷塘月色》__ <br>

**注**：该图片中之所以缺少个别字，是因为所使用生成该图片的字体本身缺少这些字。

示例代码：[examples/article.py](examples/article.py)

![](examples/out/荷塘月色/0.png)
![](examples/out/荷塘月色/1.png)
![](examples/out/荷塘月色/2.png)
![](examples/out/荷塘月色/3.png)

## Contributing

 * [Contributor Covenant Code of Conduct](docs/CODE_OF_CONDUCT.md)
 * [Issue Template](docs/ISSUE_TEMPLATE.md)
 