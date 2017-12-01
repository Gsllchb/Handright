from PIL import Image, ImageFont
from pylf import handwrite
import unittest

image = Image.open("./data/pictures/background.png")
template = {
    'background': image,
    'box': (100, 150, image.width - 100, image.height - 100),
    'color': (0, 0, 0),
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
            handwrite(text, tmp)

        tmp['box'] = (100, 100, 100 + font_size, 100 + font_size + 1)
        with self.assertRaises(ValueError):
            handwrite(text, tmp)

        tmp['box'] = (100, 100, 100 + font_size, 100 + font_size )
        with self.assertRaises(ValueError):
            handwrite(text, tmp)

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
        prompt = "{}\nTest by naked eyes. pass test? [Y/N] \n"
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
        tmp['box'] = (-100, -100, im.width + 100, im.height + 100)
        images = handwrite(txt * 100, tmp)
        for im in images:
            im.show()
        self.assertTrue(input(prompt.format(txt)).upper() == 'Y')


if __name__ == '__main__':
    unittest.main()
