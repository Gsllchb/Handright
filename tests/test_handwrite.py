# coding: utf-8
import copy
import multiprocessing

from PIL import Image as image
from PIL import ImageDraw as image_draw

from pylf import handwrite
from tests.util import *

BACKGROUND_COLOR = "white"
DEFAULT_WIDTH = 2000
DEFAULT_HEIGHT = 2000
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
SEED = "PyLf"
THRESHOLD = 0.01


def get_default_template() -> dict:
    template = {"background": image.new(mode='RGB', size=DEFAULT_SIZE, color=BACKGROUND_COLOR),
                "margin": {"left": 200, "top": 376, "right": 200, "bottom": 400},
                "line_spacing": 144,
                "font": get_default_font(),
                "font_size": 120,
                "font_size_sigma": 0}
    return template


def test_side_effect():
    text = get_short_text()
    template = get_default_template()
    template_clone = copy.copy(template)
    handwrite(text, template)
    assert text == get_short_text()
    assert template == template_clone


def test_null_text():
    assert handwrite('', get_default_template()) == []


def test_text_iterable():
    template = get_default_template()

    text = get_short_text()
    ims1 = handwrite(text, template, seed=SEED)

    text = list(get_short_text())
    ims2 = handwrite(text, template, seed=SEED)
    for im1, im2 in zip(ims1, ims2):
        assert im1 == im2

    text = tuple(get_short_text())
    ims2 = handwrite(text, template, seed=SEED)
    for im1, im2 in zip(ims1, ims2):
        assert im1 == im2

    text = (c for c in get_short_text())
    ims2 = handwrite(text, template, seed=SEED)
    for im1, im2 in zip(ims1, ims2):
        assert im1 == im2


def test_randomness():
    text = get_short_text()
    template = get_default_template()
    ims1 = handwrite(text, template)
    ims2 = handwrite(text, template)
    for im1, im2 in zip(ims1, ims2):
        assert diff_histogram(im1, im2) < THRESHOLD


def test_mode_and_color():
    text = get_short_text()
    template = get_default_template()
    for mode in ('L', 'RGB'):
        for background_color in ('rgb(0, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 255, 255)'):
            template['background'] = image.new(mode=mode, size=DEFAULT_SIZE, color=background_color)
            for color in ('rgb(0, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 255, 255)'):
                template['color'] = color
                standard_image = template['background'].copy()
                image_draw.Draw(standard_image).text(xy=(template["margin"]["left"] + 1, template["margin"]["top"] + 1),
                                                     text=text, fill=color,
                                                     font=template['font'].font_variant(size=template['font_size']))

                images = handwrite(text, template)
                assert len(images) == 1
                assert diff_histogram(standard_image, images[0]) < THRESHOLD


def test_font_size():
    text = get_short_text()
    template = get_default_template()
    template['color'] = 'black'
    for font_size in (1, 10, 30):
        standard_image = template['background'].copy()
        image_draw.Draw(standard_image).text(xy=(template["margin"]["left"] + 1, template["margin"]["top"] + 1),
                                             text=text, fill=template['color'],
                                             font=template['font'].font_variant(size=font_size))

        template['font_size'] = font_size
        images = handwrite(text, template)
        assert len(images) == 1
        assert diff_histogram(standard_image, images[0]) < THRESHOLD


def test_is_half_char_fn():
    text = '。' * 30
    template = get_default_template()
    template["color"] = "black"
    template['is_half_char_fn'] = lambda c: True
    images = handwrite(text, template)
    assert len(images) == 1
    standard_image = template['background'].copy()
    image_draw.Draw(standard_image).multiline_text(xy=(template["margin"]["left"] + 1, template["margin"]["top"] + 1),
                                                   text=('。' * 6 + '\n') * 5, fill=template['color'],
                                                   font=template['font'].font_variant(size=template['font_size']))
    assert diff_histogram(standard_image, images[0]) < THRESHOLD


def test_is_end_char_fn():
    text = '。' * 30
    template = get_default_template()
    template['color'] = "black"
    template['is_end_char_fn'] = lambda c: False
    images = handwrite(text, template)
    assert len(images) == 1
    standard_image = template['background'].copy()
    image_draw.Draw(standard_image).multiline_text(xy=(template["margin"]["left"] + 1, template["margin"]["top"] + 1),
                                                   text=('。' * 6 + '\n') * 5, fill=template['color'],
                                                   font=template['font'].font_variant(size=template['font_size']))
    assert diff_histogram(standard_image, images[0]) < THRESHOLD


def test_worker():
    text = get_short_text()
    template = get_default_template()
    template['color'] = 'rgb(0, 0, 0)'
    standard_image = template['background'].copy()
    image_draw.Draw(standard_image).text(xy=(template["margin"]["left"] + 1, template["margin"]["top"] + 1),
                                         text=text, fill=template['color'],
                                         font=template['font'].font_variant(size=template['font_size']))
    cpu_count = multiprocessing.cpu_count()
    workers = {1, cpu_count // 2, cpu_count, 2 * cpu_count}
    workers.discard(0)
    for worker in workers:
        images = handwrite((text + '\n' * 8) * max(worker, cpu_count), template, worker=worker)
        for i in images:
            assert diff_histogram(standard_image, i) < THRESHOLD


def test_seed():
    text = get_short_text() * 50
    template = get_default_template()
    worker = 2
    for seed in ("PyLf", 0.5, 666):
        ims1 = handwrite(text, template, worker=worker, seed=seed)
        ims2 = handwrite(text, template, worker=worker, seed=seed)
        for im1, im2 in zip(ims1, ims2):
            assert im1 == im2
