"""
Test handwrite by naked eye.
"""
from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support
import os
import time
import copy


def main():
    im = Image.open("./data/pictures/design.jpg")
    font = ImageFont.truetype("./data/fonts/Gsllchb_lf.ttf")
    template = {
        'background': im,
        'box': (100, 400, im.width-100, im.height-100),
        'color': (0, 0, 0),
        'font': font,
        'font_size': 40,
        'font_size_sigma': 2,
        'line_spacing': 40,
        'line_spacing_sigma': 1,
        'word_spacing': 0,
        'word_spacing_sigma': 2,
        'is_half_char': lambda c: c.isdigit() or c in ('!', '.', '?', ',', '，', '。'),
        'is_end_char': lambda c: c in ('!', '.', '?', ',', '，', '。')
    }
    template_clone = copy.copy(template)
    text = '我能吞下玻璃而不伤身体。'
    text_clone = copy.deepcopy(text)
    handwrite(text, template)
    assert template == template_clone
    assert text == text_clone


if __name__ == '__main__':
    freeze_support()
    main()
