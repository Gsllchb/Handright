import PIL.Image
import PIL.ImageFont
from util import *

from pylf import *


DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)


def test_one_background():
    background = PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color='rgb(255, 255, 255)')
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
            assert compare_histogram(im1, im2) < THRESHOLD


def test_even_odd():
    text = get_short_text()
    template2 = dict(
        page_settings=[
            dict(
                background=PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color='rgb(255, 255, 255)'),
                box=(50, 100, DEFAULT_WIDTH - 50, DEFAULT_HEIGHT - 100),
                font_size=30,
                font_size_sigma=0,
                line_spacing=6
            ),
            dict(
                background=PIL.Image.new(mode='RGBA', size=DEFAULT_SIZE, color='rgb(0, 128, 255)'),
                box=(50, 100, DEFAULT_WIDTH - 50, DEFAULT_HEIGHT - 100),
                font_size=20,
                font_size_sigma=0,
                line_spacing=16
            )
        ],
        font=get_default_font(),
        color='rgb(0, 0, 0)'
    )
    standard_images = list()
    for i in range(2):
        standard_image = template2['page_settings'][i]['background'].copy()
        PIL.ImageDraw.Draw(standard_image).text(
            xy=(template2['page_settings'][i]['box'][0], template2['page_settings'][i]['box'][1]),
            text=text,
            fill=template2['color'],
            font=template2['font'].font_variant(size=template2['page_settings'][i]['font_size'])
        )
        standard_images.append(standard_image)

    images2 = handwrite2((text + '\n' * 8) * 6, template2, anti_aliasing=False)
    for i in range(len(images2)):
        assert compare_histogram(images2[i], standard_images[i % 2]) < THRESHOLD
