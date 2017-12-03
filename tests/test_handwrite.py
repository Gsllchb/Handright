from PIL import Image, ImageFont
from pylf import handwrite
import unittest

image = Image.open("./data/pictures/background.png")
template = {
    'background': image,
    'box': (100, 150, image.width - 100, image.height - 100),
    'font': ImageFont.truetype("./data/fonts/Gsllchb_lf.ttf"),
    'font_size': 30,
    'font_size_sigma': 1,
    'line_spacing': 30,
    'line_spacing_sigma': 1,
    'word_spacing': 0,
    'word_spacing_sigma': 1,
    'is_half_char': lambda c: c.isdigit() or c in ('!', '.', '?', ',', '，', '。'),
    'is_end_char': lambda c: c in ('!', '.', '?', ',', '，', '。')
}
text = """我能吞下玻璃而不伤身体。"""


class TestHandwrite(unittest.TestCase):

    @staticmethod
    def __copy():
        return str(text), dict(template)

    def test_exception(self):
        txt, tmp = self.__copy()
        font_size = tmp['font_size']

        tmp['box'] = (100, 100, 100 + font_size + 1, 100 + font_size)
        with self.assertRaises(ValueError):
            handwrite(txt, tmp)

        tmp['box'] = (100, 100, 100 + font_size, 100 + font_size + 1)
        with self.assertRaises(ValueError):
            handwrite(txt, tmp)

        tmp['box'] = (100, 100, 100 + font_size, 100 + font_size )
        with self.assertRaises(ValueError):
            handwrite(txt, tmp)

    def test_side_effect(self):
        txt, tmp = self.__copy()
        handwrite(txt, tmp)
        self.assertEqual(txt, text)
        self.assertEqual(tmp, template)

    def test_null_text(self):
        tmp = self.__copy()[1]
        self.assertEqual(handwrite('', tmp), [])

    def test_by_naked_eyes(self):
        import os
        print('Test by naked eyes:')
        prompt = "{}\npass test? [Y/N] \n"
        tmp = self.__copy()[1]
        dir_path, dir_names, file_names = list(os.walk("./data/texts"))[0]
        for filename in file_names:
            with open("{}/{}".format(dir_path, filename)) as f:
                txt = f.read()
            images = handwrite(txt, tmp)
            for im in images:
                im.show()
            self.assertTrue(input(prompt.format(filename)).upper() == 'Y')

        txt = "测试关闭SSAA抗锯齿的效果"
        images = handwrite(txt, tmp, anti_aliasing=False)
        for im in images:
            im.show()
        self.assertTrue(input(prompt.format(txt)).upper() == 'Y')

        txt = "测试‘box’比背景图大的情况。"
        tmp = self.__copy()[1]
        tmp['box'] = (-100, -100, im.width + 100, im.height + 100)
        images = handwrite(txt * 100, tmp)
        for im in images:
            im.show()
        self.assertTrue(input(prompt.format(txt)).upper() == 'Y')

        tmp = self.__copy()[1]
        cases = {
            '黑色': (0, 0, 0),
            '白色': (255, 255, 255),
            '红色': (255, 0, 0),
            '绿色': (0, 255, 0),
            '蓝色': (0, 0, 255),
            'color: (-1, -1, -1)': (-1, -1, -1),
            'color: (1000, 1000, 1000)': (1000, 1000, 1000),
        }
        for (k, v) in cases.items():
            print(k, v)
            tmp['color'] = v
            images = handwrite(k, tmp)
            for im in images:
                im.show()
        self.assertTrue(input(prompt.format("测试颜色")).upper() == 'Y')


if __name__ == '__main__':
    unittest.main()
