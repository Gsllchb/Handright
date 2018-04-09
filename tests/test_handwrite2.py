import os
import unittest

import PIL.Image
import PIL.ImageFont

from pylf import handwrite2


def get_path(path: str) -> str:
    return os.path.split(os.path.realpath(__file__))[0] + '/' + path


class TestHandwrite2(unittest.TestCase):

    @staticmethod
    def compare(im1, im2):
        return im1.tobytes() == im2.tobytes()

    @staticmethod
    def get_default_text():
        with open(get_path("data/texts/荷塘月色.txt")) as f:
            return f.read()

    @staticmethod
    def get_default_template2():
        """ Get the template2 without randomness """
        template2 = dict(
            page_settings=[
                dict(
                    background=PIL.Image.open(get_path("data/backgrounds/会议记录/even.png")),
                    box=(333, 1245, 2151, 3010),
                    font_size=95,
                    line_spacing=23,
                    font_size_sigma=0,
                    line_spacing_sigma=0,
                    word_spacing_sigma=0
                ),
                dict(
                    background=PIL.Image.open(get_path("data/backgrounds/会议记录/odd.png")),
                    box=(333, 535, 2151, 3010),
                    font_size=95,
                    line_spacing=23,
                    font_size_sigma=0,
                    line_spacing_sigma=0,
                    word_spacing_sigma=0
                ),
            ],
            font=PIL.ImageFont.truetype(get_path(
                "data/fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf")),
            alpha=(0, 0),
        )
        return template2

    def test_even_odd(self):
        text = self.get_default_text()
        template2 = self.get_default_template2()
        ims = handwrite2(text, template2, anti_aliasing=False)
        for i, im in enumerate(ims):
            # im.save(get_path("data/images/test_even_odd{}.png".format(i)))
            self.assertTrue(self.compare(im, PIL.Image.open(get_path("data/images/test_even_odd{}.png".format(i)))))


if __name__ == '__main__':
    unittest.main()
