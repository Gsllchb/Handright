# coding: utf-8
import copy
import multiprocessing

import PIL.Image
import PIL.ImageDraw

from pylf import handwrite
from tests.util import *

BACKGROUND_COLOR = "white"
WIDTH = 100
HEIGHT = 100
SIZE = (WIDTH, HEIGHT)
SEED = "PyLf"


def get_default_template() -> dict:
    template = {
        "background": PIL.Image.new(
            mode="RGB",
            size=SIZE,
            color=BACKGROUND_COLOR
        ),
        "margin": {"left": 10, "top": 18, "right": 10, "bottom": 20},
        "line_spacing": 7,
        "font": get_default_font(),
        "font_size": 6,
        "font_size_sigma": 0,
    }
    return template


def test_side_effect():
    text = get_short_text()
    template = get_default_template()
    template_clone = copy.copy(template)
    handwrite(text, template)
    assert text == get_short_text()
    assert template == template_clone


def test_null_text():
    assert handwrite("", get_default_template()) == []


def test_worker():
    text = get_long_text()
    template = get_default_template()
    cpu_count = multiprocessing.cpu_count()
    workers = {1, cpu_count // 2, cpu_count, 2 * cpu_count}
    workers.discard(0)
    workers.discard(1)
    prev_images = None
    for worker in workers:
        images = handwrite(text, template, worker=worker, seed=SEED)
        if prev_images is not None:
            assert len(prev_images) == len(images)
            assert all(im1 == im2 for im1, im2 in zip(prev_images, images))
        prev_images = images


def test_seed():
    text = get_long_text()
    template = get_default_template()
    for seed in (0, "PyLf"):
        ims1 = handwrite(text, template, seed=seed)
        ims2 = handwrite(text, template, seed=seed)
        assert all(im1 == im2 for im1, im2 in zip(ims1, ims2))


def test_result():
    assert isinstance(handwrite("", get_default_template()), list)
    assert isinstance(handwrite(get_short_text(), get_default_template()), list)
    assert isinstance(handwrite(get_long_text(), get_default_template()), list)
