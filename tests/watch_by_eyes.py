""" Test the results with your eyes """
import os
import pathlib
import unittest

import PIL.Image
import PIL.ImageFont

from pylf import handwrite


def get_path(path: str) -> str:
    return os.path.split(os.path.realpath(__file__))[0] + '/' + path


class TestByNakedEyes(unittest.TestCase):
    def test_articles(self):
        print('Test by naked eyes:')
        template = dict(
            background=PIL.Image.open(get_path("data/backgrounds/letter.png")),
            box=(68, 130, 655, 925),
            font=PIL.ImageFont.truetype(get_path(
                "data/fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf")),
            font_size=27,
            line_spacing=6
        )
        for file in pathlib.Path(get_path("data/texts")).iterdir():
            print(file)
            with file.open() as f:
                text = f.read()
            images = handwrite(text, template)
            for im in images:
                im.show()
            self.assertTrue(input("Like it? [Y/N] ").upper() == 'Y')


if __name__ == '__main__':
    unittest.main()
