import PIL.Image
import PIL.ImageFont
from util import *

from pylf import *


BACKGROUND_COLOR = 'rgb(255, 255, 255)'
DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)


def test_one_background():
    background = PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color=BACKGROUND_COLOR)
    box = (50, 100, DEFAULT_WIDTH - 50, DEFAULT_HEIGHT - 100)
    font = get_default_font()
    font_size = 30
    font_size_sigma = 0

    text = get_long_text()
    template = dict(background=background, box=box, font=font, font_size=font_size, font_size_sigma=font_size_sigma)
    template2 = dict(
        page_settings=[dict(background=background, box=box, font_size=font_size, font_size_sigma=font_size_sigma), ],
        font=font,
    )
    for anti_aliasing in (True, False):
        images1 = handwrite(text, template, anti_aliasing=anti_aliasing)
        images2 = handwrite2(text, template2, anti_aliasing=anti_aliasing)
        for im1, im2 in zip(images1, images2):
            im1.show()
            im2.show()
            assert compare_histogram(im1, im2) < THRESHOLD
