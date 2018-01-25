# *Windows*用户必读
*Windows*用户在使用*PyLf*以及其它任何基于[*multiprocessing*](https://docs.python.org/3.6/library/multiprocessing.html)
的module时，均须将代码写成类似于如下形式：

    from multiprocessing import freeze_support
    
    def main():
        ...
        
    if __name__ == '__main__':
        freeze_support()
        main()


亦即[README.md](../README.md)中`Walk through`中的代码须写成如下形式：

    from PIL import Image, ImageFont
    from pylf import handwrite
    from multiprocessing import freeze_support
    
    def main():
        # 设置模板的参数
        template = {
            # 设置背景图片（图片的大小应大于‘box’所限定的范围）
            'background': Image.new(mode='RGB', size=(800, 1000), color='rgb(255, 255, 255)'),  
            # 限定“手写”的范围的左、上、右、下边界的坐标（以左上角为坐标原点）
            'box': (100, 200, 700, 800),
            # 设置字体
            'font': ImageFont.truetype("./something.ttf"),  
            'font_size': 10,
        }
        text = "我能吞下玻璃而不伤身体。"
        images = handwrite(text, template)
        for image in images:
            image.show()

    if __name__ == '__main__':
        freeze_support()
        main()

更多信息：[17.2. multiprocessing — Process-based parallelism](https://docs.python.org/3.6/library/multiprocessing.html#module-multiprocessing)
