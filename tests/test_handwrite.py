import copy

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import pytest
from util import *

from pylf import handwrite

THESHOLD = 10.0

BACKGROUND_COLOR = 'rgb(255, 255, 255)'
DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)


def get_default_template():
    template = dict(
        background=PIL.Image.new(mode='RGB', size=DEFAULT_SIZE, color=BACKGROUND_COLOR),
        box=(50, 100, DEFAULT_WIDTH - 50, DEFAULT_HEIGHT - 100),
        font=get_default_font(),
        font_size=30,
        font_size_sigma=0
    )
    return template


def test_error_box():
    text = get_short_text()
    template = get_default_template()
    font_size = template['font_size']

    template['box'] = (100, 100, 100 + font_size + 1, 100 + font_size)
    with pytest.raises(ValueError):
        handwrite(text, template)

    template['box'] = (100, 100, 100 + font_size, 100 + font_size + 1)
    with pytest.raises(ValueError):
        handwrite(text, template, anti_aliasing=False)

    template['box'] = (100, 100, 100 + font_size, 100 + font_size)
    with pytest.raises(ValueError):
        handwrite(text, template)


def test_error_alpha():
    text = get_short_text()
    template = get_default_template()

    template['alpha'] = (-1, 0)
    with pytest.raises(ValueError):
        handwrite(text, template)

    template['alpha'] = (-1, -1)
    with pytest.raises(ValueError):
        handwrite(text, template, anti_aliasing=False)

    template['alpha'] = (0, -1)
    with pytest.raises(ValueError):
        handwrite(text, template)

    template['alpha'] = (2, 0)
    with pytest.raises(ValueError):
        handwrite(text, template)

    template['alpha'] = (2, 2)
    with pytest.raises(ValueError):
        handwrite(text, template)

    template['alpha'] = (0, 2)
    with pytest.raises(ValueError):
        handwrite(text, template, anti_aliasing=False)

    template['alpha'] = (-1, 2)
    with pytest.raises(ValueError):
        handwrite(text, template, anti_aliasing=False)

    template['alpha'] = (2, -1)
    with pytest.raises(ValueError):
        handwrite(text, template)


def test_side_effect():
    for anti_aliasing in (True, False):
        text = get_short_text()
        template = get_default_template()
        template_clone = copy.copy(template)
        handwrite(text, template, anti_aliasing=anti_aliasing)
        assert text == get_short_text()
        assert template == template_clone


def test_null_text():
    assert handwrite('', get_default_template()) == []


def test_text_iterable():
    template = get_default_template()

    text = get_short_text()
    ims1 = handwrite(text, template, anti_aliasing=False)

    text = list(get_short_text())
    ims2 = handwrite(text, template, anti_aliasing=False)
    for im1, im2 in zip(ims1, ims2):
        assert compare_histogram(im1, im2) < THESHOLD

    text = tuple(get_short_text())
    ims2 = handwrite(text, template, anti_aliasing=False)
    for im1, im2 in zip(ims1, ims2):
        assert compare_histogram(im1, im2) < THESHOLD

    text = (c for c in get_short_text())
    ims2 = handwrite(text, template, anti_aliasing=False)
    for im1, im2 in zip(ims1, ims2):
        assert compare_histogram(im1, im2) < THESHOLD


def test_outside_box():
    text = get_short_text()
    template = get_default_template()
    for box in (
            (-2 * DEFAULT_WIDTH, 0, -DEFAULT_WIDTH, DEFAULT_HEIGHT),
            (0, -2 * DEFAULT_HEIGHT, DEFAULT_WIDTH, -DEFAULT_HEIGHT),
            (2 * DEFAULT_WIDTH, 0, 3 * DEFAULT_WIDTH, DEFAULT_HEIGHT),
            (0, 2 * DEFAULT_HEIGHT, DEFAULT_WIDTH, 3 * DEFAULT_HEIGHT),
            (-2 * DEFAULT_WIDTH, -2 * DEFAULT_HEIGHT, -DEFAULT_WIDTH, -DEFAULT_HEIGHT)
    ):
        template['box'] = box
        for anti_aliasing in (True, False):
            ims = handwrite(text, template, anti_aliasing=anti_aliasing)
            for im in ims:
                assert absolute_equal(im, template['background'])


def test_randomness():
    text = get_short_text()
    template = get_default_template()
    ims1 = handwrite(text, template)
    ims2 = handwrite(text, template)
    for im1, im2 in zip(ims1, ims2):
        assert compare_histogram(im1, im2) < THESHOLD

    ims1 = handwrite(text, template, anti_aliasing=False)
    ims2 = handwrite(text, template, anti_aliasing=False)
    for im1, im2 in zip(ims1, ims2):
        assert compare_histogram(im1, im2) < THESHOLD


def test_mode_and_color():
    text = get_short_text()
    template = get_default_template()
    for mode in ('L', 'RGB', 'RGBA'):
        for background_color in ('rgb(0, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 255, 255)', 'rgb(250, 128, 1)'):
            template['background'] = PIL.Image.new(mode=mode, size=DEFAULT_SIZE, color=background_color)
            for color in ('rgb(0, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 255, 255)', 'rgb(250, 128, 1)'):
                template['color'] = color
                standard_image = template['background'].copy()
                PIL.ImageDraw.Draw(standard_image).text(
                    xy=(template['box'][0], template['box'][1]),
                    text=text,
                    fill=color,
                    font=template['font'].font_variant(size=template['font_size'])
                )

                images = handwrite(text, template, anti_aliasing=False)
                assert len(images) == 1
                assert compare_histogram(standard_image, images[0]) < THESHOLD
                images = handwrite(text, template)
                assert len(images) == 1
                assert compare_histogram(standard_image, images[0]) < THESHOLD


def test_font_size():
    text = get_short_text()
    template = get_default_template()
    template['color'] = 'rgb(0, 0, 0)'
    for font_size in (0, 1, 10, 30):
        standard_image = template['background'].copy()
        PIL.ImageDraw.Draw(standard_image).text(
            xy=(template['box'][0], template['box'][1]),
            text=text,
            fill=template['color'],
            font=template['font'].font_variant(size=font_size)
        )

        template['font_size'] = font_size
        images = handwrite(text, template, anti_aliasing=False)
        assert len(images) == 1
        assert compare_histogram(standard_image, images[0]) < THESHOLD
        images = handwrite(text, template)
        assert len(images) == 1
        assert compare_histogram(standard_image, images[0]) < THESHOLD


def test_is_half_char():
    text = '。' * 30
    template = get_default_template()
    template['color'] = 'rgb(0, 0, 0)'
    template['is_half_char'] = lambda c: True
    images = handwrite(text, template, anti_aliasing=False)
    assert len(images) == 1
    standard_image = template['background'].copy()
    PIL.ImageDraw.Draw(standard_image).multiline_text(
        xy=(template['box'][0], template['box'][1]),
        text=('。' * 6 + '\n') * 5,
        fill=template['color'],
        font=template['font'].font_variant(size=template['font_size'])
    )
    assert compare_histogram(standard_image, images[0]) < THESHOLD


def test_is_end_char():
    text = '。' * 30
    template = get_default_template()
    template['color'] = 'rgb(0, 0, 0)'
    template['is_end_char'] = lambda c: True
    images = handwrite(text, template, anti_aliasing=False)
    assert len(images) == 1
    standard_image = template['background'].copy()
    PIL.ImageDraw.Draw(standard_image).multiline_text(
        xy=(template['box'][0], template['box'][1]),
        text=('。' * 6 + '\n') * 5,
        fill=template['color'],
        font=template['font'].font_variant(size=template['font_size'])
    )
    assert compare_histogram(standard_image, images[0]) >= THESHOLD


def test_multiprocessing():
    text = get_short_text()
    template = get_default_template()
    template['color'] = 'rgb(0, 0, 0)'
    standard_image = template['background'].copy()
    PIL.ImageDraw.Draw(standard_image).text(
        xy=(template['box'][0], template['box'][1]),
        text=text,
        fill=template['color'],
        font=template['font'].font_variant(size=template['font_size'])
    )
    images = handwrite((text + '\n' * 8) * 6, template, worker=2, anti_aliasing=False)
    for image in images:
        image.show()
        assert compare_histogram(standard_image, image) < THESHOLD
