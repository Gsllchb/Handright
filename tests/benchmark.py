from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support
import time


def main():
    case = '我能吞下玻璃而不伤身体。\n'
    im = Image.open("./data/pictures/design.jpg")
    template = {
        'background': im,
        'box': (200, 400, im.width-200, im.height-400),
        'color': (0, 0, 0),
        'font': ImageFont.truetype("./data/fonts/Gsllchb_lf.ttf"),
        'font_size': 80,
        'font_size_sigma': 2,
        'line_spacing': 400,
        'line_spacing_sigma': 1,
        'word_spacing': 0,
        'word_spacing_sigma': 2,
        'is_half_char': lambda c: c.isdigit() or c in ('!', '.', '?', ',', '，', '。'),
        'is_end_char': lambda c: c in ('!', '.', '?', ',', '，', '。')
    }
    print('case \t char \t image \t time')
    for i in range(1, 35):
        start = time.clock()
        images = handwrite(case * i, template, worker=4)
        # for im in images:
        #     im.show()
        print('#{}: \t {} \t {} \t {}'.format(i, len(case) * i, len(images), time.clock() - start))

if __name__ == '__main__':
    freeze_support()
    main()