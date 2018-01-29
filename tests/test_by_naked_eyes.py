""" Test the results with your eyes """
import pathlib
import unittest

import PIL.Image
import PIL.ImageFont

import pylf


class TestByNakedEyes(unittest.TestCase):
    def test_articles(self):
        print('Test by naked eyes:')
        template = dict(
            background=PIL.Image.open("./data/backgrounds/letter.png"),
            box=(68, 130, 655, 925),
            font=PIL.ImageFont.truetype(
                "./data/fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"),
            font_size=27,
            line_spacing=6
        )
        for file in pathlib.Path("./data/texts").iterdir():
            print(file)
            with file.open() as f:
                text = f.read()
            images = pylf.handwrite(text, template)
            for im in images:
                im.show()
            self.assertTrue(input("Like it? [Y/N] ").upper() == 'Y')


if __name__ == '__main__':
    unittest.main()
