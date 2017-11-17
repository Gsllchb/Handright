"""
Test handwrite by naked eye.
"""
from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support
import os


def main():
    template = {
        'background': Image.open("./data/pictures/design.jpg"),
        'box': (100, 400, 1500, 2000),
        'color': (0, 0, 0),
        'font': ImageFont.truetype("./data/fonts/HYYiNingLiJ.ttf"),
        'font_size': 40,
        'font_size_sigma': 2,
        'line_spacing': 40,
        'line_spacing_sigma': 1,
        'word_spacing': 20,
        'word_spacing_sigma': 2,
        'is_half_char': lambda c: c.isalpha() or c.isdigit() or c in (',', '.'),
        'is_end_char': lambda c: c in ('!', '.', '?')
    }
    dir_path, dir_names, file_names = list(os.walk("./data/texts"))[0]
    for filename in file_names:
        with open("{}/{}".format(dir_path, filename)) as f:
            text = f.read()
        images = handwrite(text, template)
        for image in images:
            image.show()
        input("""{} has been written.
        press ENTER to continues""".format(filename))


if __name__ == '__main__':
    freeze_support()
    main()
