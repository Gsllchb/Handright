# coding: utf-8
import copy
import multiprocessing

import PIL.Image
import PIL.ImageDraw

from pylf import *
from tests.util import *

BACKGROUND_COLOR = "white"
WIDTH = 32
HEIGHT = 32
SIZE = (WIDTH, HEIGHT)
SEED = "PyLf"


def get_default_template():
    template = Template(
        background=PIL.Image.new(
            mode="RGB",
            size=SIZE,
            color=BACKGROUND_COLOR
        ),
        left_margin=3,
        top_margin=6,
        right_margin=3,
        bottom_margin=6,
        line_spacing=2,
        font=get_default_font(),
        font_size=2,
        font_size_sigma=0,
    )
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


def test_blank_text():
    temp = get_default_template()
    images = handwrite(" ", temp)
    assert temp.get_background() == images[0]


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
            assert prev_images == images
        prev_images = images


def test_seed():
    text = get_long_text()
    template = get_default_template()
    for seed in (0, "PyLf"):
        ims1 = handwrite(text, template, seed=seed)
        ims2 = handwrite(text, template, seed=seed)
        assert ims1 == ims2


def test_line_and_page_breaks():
    text = "哈" * 4
    template = Template(
        background=PIL.Image.new(mode="L", size=(30, 30), color="white"),
        font=get_default_font(),
        left_margin=3,
        right_margin=3,
        top_margin=3,
        bottom_margin=3,
        line_spacing=12,
        font_size=12,
        word_spacing_sigma=0,
        font_size_sigma=0,
    )
    images = handwrite(text, template)
    assert len(images) == 1


def test_result():
    assert isinstance(handwrite("", get_default_template()), list)
    assert isinstance(handwrite(get_short_text(), get_default_template()), list)
    assert isinstance(handwrite(get_long_text(), get_default_template()), list)
