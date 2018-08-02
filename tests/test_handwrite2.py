# coding: utf-8
from PIL import Image as image
from PIL import ImageDraw as image_draw

from util import *
from pylf import *

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
SEED = "PyLf"
THRESHOLD = 0.01


def get_default_template2() -> dict:
    template2 = {"page_settings": [{"background": image.new(mode='RGB', size=DEFAULT_SIZE, color="white"),
                                    "margin": {"left": 50, "top": 94, "right": 50, "bottom": 100},
                                    "line_spacing": 36,
                                    "font_size": 30,
                                    "font_size_sigma": 0},
                                   {"background": image.new(mode='RGBA', size=DEFAULT_SIZE, color='rgb(0, 128, 255)'),
                                    "margin": {"left": 50, "top": 96, "right": 50, "bottom": 100},
                                    "line_spacing": 24,
                                    "font_size": 20,
                                    "font_size_sigma": 0}],
                 "font": get_default_font(),
                 "color": "black"}
    return template2


def test_one_background():
    background = image.new(mode='RGB', size=DEFAULT_SIZE, color="white")
    margin = {"left": 50, "top": 94, "right": 50, "bottom": 100}
    line_spacing = 36
    font = get_default_font()
    font_size = 30
    font_size_sigma = 0

    text = get_long_text()
    template = {"background": background, "margin": margin, "line_spacing": line_spacing, "font": font,
                "font_size": font_size, "font_size_sigma": font_size_sigma}
    template2 = {"page_settings": [{"background": background, "margin": margin, "line_spacing": line_spacing,
                                    "font_size": font_size, "font_size_sigma": font_size_sigma}, ],
                 "font": font}
    images1 = handwrite(text, template, seed=SEED)
    images2 = handwrite2(text, template2, seed=SEED)
    for im1, im2 in zip(images1, images2):
        assert im1 == im2


def test_even_odd():
    text = get_short_text()
    template2 = get_default_template2()
    standard_images = []
    for i in range(2):
        font_size = template2['page_settings'][i]['font_size']
        standard_image = template2['page_settings'][i]['background'].copy()
        xy = (template2['page_settings'][i]['margin']["left"] + 1,
              template2['page_settings'][i]['margin']["top"] + template2['page_settings'][i]['line_spacing']
              - template2['page_settings'][i]["font_size"] + 1)
        image_draw.Draw(standard_image).text(xy=xy, text=text, fill=template2['color'],
                                             font=template2['font'].font_variant(size=font_size))
        standard_images.append(standard_image)

    images2 = handwrite2((text + '\n' * 8) * 6, template2)
    for i in range(len(images2)):
        assert diff_histogram(images2[i], standard_images[i % 2]) < THRESHOLD


def test_seed():
    text = get_short_text() * 50
    template2 = get_default_template2()
    worker = 2
    for seed in (-666, -1, 0, 1, "pylf"):
        ims1 = handwrite2(text, template2, worker=worker, seed=seed)
        ims2 = handwrite2(text, template2, worker=worker, seed=seed)
        for im1, im2 in zip(ims1, ims2):
            assert im1 == im2
