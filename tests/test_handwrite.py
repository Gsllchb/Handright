import copy
import unittest

import PIL.Image
import PIL.ImageFont

from pylf import handwrite

BACKGROUND_COLOR = 'rgb(255, 255, 255)'
DEFAULT_SIZE = (500, 500)


class TestHandwrite(unittest.TestCase):

    @staticmethod
    def compare(im1, im2):
        return im1.tobytes() == im2.tobytes()

    @staticmethod
    def get_default_text():
        return "我能吞下玻璃而不伤身体"

    @staticmethod
    def get_default_template():
        """ Get the template without randomness """
        template = dict(
            background=PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color=BACKGROUND_COLOR),
            box=(50, 100, 450, 400),
            font=PIL.ImageFont.truetype("./data/fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"),
            font_size=30,
            font_size_sigma=0,
            line_spacing_sigma=0,
            word_spacing_sigma=0,
            alpha=(0, 0),
        )
        return template

    def test_error_box(self):
        text = self.get_default_text()
        template = self.get_default_template()
        font_size = template['font_size']

        template['box'] = (100, 100, 100 + font_size + 1, 100 + font_size)
        with self.assertRaises(ValueError):
            handwrite(text, template)

        template['box'] = (100, 100, 100 + font_size, 100 + font_size + 1)
        with self.assertRaises(ValueError):
            handwrite(text, template, anti_aliasing=False)

        template['box'] = (100, 100, 100 + font_size, 100 + font_size)
        with self.assertRaises(ValueError):
            handwrite(text, template)

    def test_error_alpha(self):
        text = self.get_default_text()
        template = self.get_default_template()

        template['alpha'] = (-1, 0)
        with self.assertRaises(ValueError):
            handwrite(text, template)

        template['alpha'] = (-1, -1)
        with self.assertRaises(ValueError):
            handwrite(text, template, anti_aliasing=False)

        template['alpha'] = (0, -1)
        with self.assertRaises(ValueError):
            handwrite(text, template)

        template['alpha'] = (2, 0)
        with self.assertRaises(ValueError):
            handwrite(text, template)

        template['alpha'] = (2, 2)
        with self.assertRaises(ValueError):
            handwrite(text, template)

        template['alpha'] = (0, 2)
        with self.assertRaises(ValueError):
            handwrite(text, template, anti_aliasing=False)

        template['alpha'] = (-1, 2)
        with self.assertRaises(ValueError):
            handwrite(text, template, anti_aliasing=False)

        template['alpha'] = (2, -1)
        with self.assertRaises(ValueError):
            handwrite(text, template)

    def test_side_effect(self):
        text = self.get_default_text()
        template = self.get_default_template()
        template_clone = copy.copy(template)
        handwrite(text, template)
        self.assertEqual(text, self.get_default_text())
        self.assertEqual(template, template_clone)

        text = self.get_default_text()
        template = self.get_default_template()
        template_clone = copy.copy(template)
        handwrite(text, template, anti_aliasing=False)
        self.assertEqual(text, self.get_default_text())
        self.assertEqual(template, template_clone)

    def test_null_text(self):
        self.assertEqual(handwrite('', self.get_default_template()), [])

    def test_text_iterable(self):
        template = self.get_default_template()

        text = self.get_default_text()
        ims1 = handwrite(text, template)

        text = list(self.get_default_text())
        ims2 = handwrite(text, template)
        for im1, im2 in zip(ims1, ims2):
            self.assertTrue(self.compare(im1, im2))

        text = tuple(self.get_default_text())
        ims2 = handwrite(text, template)
        for im1, im2 in zip(ims1, ims2):
            self.assertTrue(self.compare(im1, im2))

        text = (c for c in self.get_default_text())
        ims2 = handwrite(text, template)
        for im1, im2 in zip(ims1, ims2):
            self.assertTrue(self.compare(im1, im2))

    def test_outside_box(self):
        text = self.get_default_text()
        template = self.get_default_template()
        template['box'] = (-100, -100, 0, 0)
        ims = handwrite(text, template, anti_aliasing=False)
        for im in ims:
            self.assertEqual(im, template['background'])

    def test_randomness(self):
        text = self.get_default_text()
        template = self.get_default_template()
        ims1 = handwrite(text, template)
        ims2 = handwrite(text, template)
        for im1, im2 in zip(ims1, ims2):
            self.assertTrue(self.compare(im1, im2))

        ims1 = handwrite(text, template, anti_aliasing=False)
        ims2 = handwrite(text, template, anti_aliasing=False)
        for im1, im2 in zip(ims1, ims2):
            self.assertTrue(self.compare(im1, im2))

    def test_color(self):
        text = self.get_default_text()
        template = self.get_default_template()
        colors = {
            'black': 'rgb(0, 0, 0)',
            'red': 'rgb(255, 0, 0)',
            'green': 'rgb(0, 255, 0)',
            'blue': 'rgb(0, 0, 255)',
            'white': 'rgb(255, 255, 255)'
        }
        for k, v in colors.items():
            template['color'] = v
            ims = handwrite(text, template)
            assert len(ims) == 1
            # ims[0].save("./data/images/test_color_{}.png".format(k))
            self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_color_{}.png".format(k))))

    def test_oversized_box(self):
        text = self.get_default_text()
        template = self.get_default_template()
        background = template['background']
        template['box'] = (-100, -50, background.width + 100, background.height + 50)
        ims = handwrite(text * 10, template)
        assert len(ims) == 1
        # ims[0].save("./data/images/test_oversized_box.png")
        self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_oversized_box.png")))

    def test_is_half_char(self):
        text = "，，，，，，，，。。。。。。。。。。。"
        template = self.get_default_template()
        template['is_half_char'] = lambda c: c in '，。'
        ims = handwrite(text, template)
        assert len(ims) == 1
        # ims[0].save("./data/images/test_is_half_char.png")
        self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_is_half_char.png")))

    def test_is_end_char(self):
        text = self.get_default_text()
        template = self.get_default_template()
        template['is_end_char'] = lambda c: False
        ims = handwrite(text * 5, template)
        assert len(ims) == 1
        # ims[0].save("./data/images/test_is_end_char.png")
        self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_is_end_char.png")))

    def test_abundant_output(self):
        text = self.get_default_text()
        template = self.get_default_template()
        ims = handwrite(text * 66, template, worker=1)
        for i, im in enumerate(ims):
            # im.save("./data/images/test_abundant_output{}.png".format(i))
            self.assertTrue(self.compare(im, PIL.Image.open("./data/images/test_abundant_output{}.png".format(i))))

    def test_mode(self):
        text = self.get_default_text()
        template = self.get_default_template()
        # Due to various reasons
        # Except: LAB, HSV, F, CMYK, RGBa, 1, I, RGBA, YCbCr, RGBX

        png_modes = ('LA',)
        for mode in png_modes:
            template['background'] = PIL.Image.new(mode=mode, size=DEFAULT_SIZE, color=BACKGROUND_COLOR)
            ims = handwrite(text, template, anti_aliasing=False)
            assert len(ims) == 1
            # ims[0].save("./data/images/test_mode_{}.png".format(mode))
            self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_mode_{}.png".format(mode))))

        bmp_modes = ('L', 'RGB')
        for mode in bmp_modes:
            template['background'] = PIL.Image.new(mode=mode, size=DEFAULT_SIZE, color=BACKGROUND_COLOR)
            ims = handwrite(text, template, anti_aliasing=False)
            assert len(ims) == 1
            # ims[0].save("./data/images/test_mode_{}.bmp".format(mode))
            self.assertTrue(self.compare(ims[0], PIL.Image.open("./data/images/test_mode_{}.bmp".format(mode))))


if __name__ == '__main__':
    unittest.main()
