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
    assert list(handwrite("", get_default_template())) == []


def test_blank_text():
    temp = get_default_template()
    images = handwrite(" ", temp)
    assert temp.get_background() == next(images)


def test_seed():
    text = get_long_text()
    template = get_default_template()
    for seed in (0, "PyLf"):
        ims1 = handwrite(text, template, seed=seed)
        ims2 = handwrite(text, template, seed=seed)
        assert list(ims1) == list(ims2)


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
    assert len(list(images)) == 1
