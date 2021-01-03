# coding: utf-8
from typing import *

import PIL.Image
import PIL.ImageColor

from handright import *
from tests.util import *

WIDTH = 32
HEIGHT = 32
SIZE = (WIDTH, HEIGHT)
SEED = "Handright"


def get_default_templates() -> Tuple[Template, Template]:
    template1 = Template(
        background=PIL.Image.new(mode="RGB", size=SIZE, color="white"),
        left_margin=3,
        top_margin=6,
        right_margin=3,
        bottom_margin=6,
        line_spacing=2,
        font=get_default_font(2),
    )
    template2 = Template(
        background=PIL.Image.new(
            mode="RGB", size=SIZE, color="rgb(0, 128, 255)"
        ),
        left_margin=3,
        top_margin=7,
        right_margin=3,
        bottom_margin=6,
        line_spacing=1,
        font=get_default_font(1),
    )
    return template1, template2


def test_one_background():
    text = get_long_text()
    template = Template(
        background=PIL.Image.new(mode="RGB", size=SIZE, color="white"),
        left_margin=3,
        top_margin=6,
        right_margin=3,
        bottom_margin=6,
        line_spacing=2,
        font=get_default_font(2),
    )
    images1 = handwrite(text, template, seed=SEED)
    images2 = handwrite(text, (template,), seed=SEED)
    assert list(images1) == list(images2)


def test_seed():
    text = get_long_text()
    templates = get_default_templates()
    images1 = handwrite(text, templates, seed=SEED)
    images2 = handwrite(text, templates, seed=SEED)
    assert list(images1) == list(images2)

    images1 = handwrite(text, templates, seed=None)
    images2 = handwrite(text, templates, seed=None)
    assert not list(images1) == list(images2)


def test_mapper():
    text = get_long_text()
    templates = get_default_templates()
    images1 = handwrite(text, templates, seed=SEED)
    from multiprocessing import Pool
    with Pool() as p:
        images2 = handwrite(text, templates, seed=SEED, mapper=p.map)
    assert list(images1) == list(images2)


def test_1_image():
    text = get_long_text()
    templates = get_default_templates()

    background = PIL.Image.new("L", SIZE, color="white")
    templates[0].set_background(background)
    templates[1].set_background(background)

    templates[0].set_fill()
    templates[1].set_fill()

    criterion = handwrite(text, templates, seed=SEED)
    criterion = [image.convert("1") for image in criterion]

    background = PIL.Image.new("1", SIZE, color="white")
    templates[0].set_background(background)
    templates[1].set_background(background)

    images = handwrite(text, templates, seed=SEED)
    assert criterion == list(images)


def test_l_image():
    text = get_long_text()

    templates = get_default_templates()
    templates[0].set_background(PIL.Image.new("RGB", SIZE, color="yellow"))
    templates[1].set_background(PIL.Image.new("RGB", SIZE, color="black"))
    fill = (120, 100, 0)
    templates[0].set_fill(fill)
    templates[1].set_fill(fill)
    criterion = handwrite(text, templates, seed=SEED)
    criterion = [image.convert("L") for image in criterion]

    templates[0].set_background(PIL.Image.new("L", SIZE, color="yellow"))
    templates[1].set_background(PIL.Image.new("L", SIZE, color="black"))
    fill = PIL.ImageColor.getcolor("rgb{}".format(fill), mode="L")
    templates[0].set_fill(fill)
    templates[1].set_fill(fill)
    images = handwrite(text, templates, seed=SEED)
    assert criterion == list(images)


def test_rgba_image():
    text = get_long_text()
    templates = get_default_templates()
    fill = (255, 0, 0)
    templates[0].set_fill(fill)
    templates[1].set_fill(fill)
    templates[0].set_background(PIL.Image.new("RGB", SIZE, color="white"))
    templates[1].set_background(PIL.Image.new("RGB", SIZE, color="pink"))
    criterion = handwrite(text, templates, seed=SEED)

    fill = (255, 0, 0, 0)
    templates[0].set_fill(fill)
    templates[1].set_fill(fill)
    templates[0].set_background(PIL.Image.new("RGBA", SIZE, color="white"))
    templates[1].set_background(PIL.Image.new("RGBA", SIZE, color="pink"))
    images = handwrite(text, templates, seed=SEED)
    images = [image.convert("RGB") for image in images]
    assert list(criterion) == images


def test_rgb_image():
    # Test by human beings' naked eyes.
    # Please run watch.py
    pass
