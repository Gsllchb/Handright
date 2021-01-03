# coding: utf-8
import copy

import PIL.Image
import PIL.ImageDraw

from handright import *
from tests.util import *

BACKGROUND_COLOR = "white"
WIDTH = 32
HEIGHT = 32
SIZE = (WIDTH, HEIGHT)
SEED = "Handright"


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
        font=get_default_font(2),
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
    for seed in (0, "Handright"):
        ims1 = handwrite(text, template, seed=seed)
        ims2 = handwrite(text, template, seed=seed)
        assert list(ims1) == list(ims2)


def test_line_and_page_breaks():
    text = "哈" * 4
    template = Template(
        background=PIL.Image.new(mode="L", size=(30, 30), color="white"),
        font=get_default_font(12),
        left_margin=3,
        right_margin=3,
        top_margin=3,
        bottom_margin=3,
        word_spacing_sigma=0,
        font_size_sigma=0,
    )
    images = handwrite(text, template)
    assert len(list(images)) == 1


def test_line_separators():
    text1 = "a\nb\nc\n"
    text2 = "a\rb\rc\r"
    text3 = "a\r\nb\r\nc\r\n"
    text4 = "a\rb\nc\r\n"
    text5 = "a\rb\nc\r"
    text6 = "a\r\nb\rc\r"
    text7 = "a\r\nb\nc\n"
    template = get_default_template()
    assert (list(handwrite(text1, template, seed=SEED))
            == list(handwrite(text2, template, seed=SEED))
            == list(handwrite(text3, template, seed=SEED))
            == list(handwrite(text4, template, seed=SEED))
            == list(handwrite(text5, template, seed=SEED))
            == list(handwrite(text6, template, seed=SEED))
            == list(handwrite(text7, template, seed=SEED)))
