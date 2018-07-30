# -*- coding: utf-8 -*-
"""PyLf is a lightweight Python library for simulating Chinese handwriting. It introduces a great deal of randomness in
the process of Chinese handwriting to simulate the uncertainty of glyphs written by human beings. Currently, PyLf is
built on the top of Pillow library.
"""
import multiprocessing

from pylf import _core

__version__ = "1.4.0"

# Chinese, English and other end chars
_DEFAULT_END_CHARS = frozenset("，。》、？；：’”】｝、！％）" + ",.>?;:]}!%)" + "′″℃℉")

_DEFAULT_WORD_SPACING = 0
_DEFAULT_COLOR = "black"
_DEFAULT_IS_HALF_CHAR = lambda c: False
_DEFAULT_IS_END_CHAR = lambda c: c in _DEFAULT_END_CHARS
_DEFAULT_ALPHA = (0.1, 0.1)


def handwrite(text: str, template: dict, anti_aliasing: bool = True, worker: int = 0, seed=None) -> list:
    """Handwrite the text with the parameters in the template.

    Args:
        text: A char iterable.

        template: A dict-like object containing following parameters.

            background: A Pillow's Image instance.

            box: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate. The module
            uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner. Note that this function do
            not guarantee the drawn texts will completely in the box.

            font: A Pillow's font instance. Note that this function do not use the size attribute of the font instance.

            font_size: A int as the average font size in pixel. Note that (box[3] - box[1]) and (box[2] - box[0]) both
            must be greater than font_size.

            color: A str as Pillow's color name. More info: https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names
            Default: "black".

            word_spacing: A int as the average gap between two adjacent chars in pixel. Default: 0.

            line_spacing: A int as the average gap between two adjacent lines in pixel. Default: font_size // 5.

            font_size_sigma: A float as the sigma of the gauss distribution of the font size. Default: font_size / 256.

            word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing. Default:
            font_size / 256.

            line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing. Default:
            font_size / 256.

            is_half_char: A function judging whether or not a char only take up half of its original width. The function
            must take a char parameter and return a boolean value. Default: (lambda c: False).

            is_end_char: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，',
            '。', '》', ')', ']'). The function must take a char parameter and return a boolean value. Default:
            (lambda c: c in _DEFAULT_END_CHARS).

            alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in
            order. Both values must be between 0.0 (inclusive) and 1.0 (inclusive). Default: (0.1, 0.1).

        anti_aliasing: Whether or not turn on the anti-aliasing. Default: True.

        worker: A int as the number of worker. if worker is less than or equal to 0, the actual amount of worker would
        be the number of CPU in the computer adding worker. Default: 0.

        seed: The seed of the internal random generators. Default: None.

    Returns:
        A list of drawn images with the same size and mode as the background image.

    Raises:
        ValueError: When the parameters are not be set properly.
    """
    page_setting = {}
    page_setting["background"] = template["background"]
    page_setting["box"] = template["box"]
    page_setting["font_size"] = template["font_size"]
    if "word_spacing" in template:
        page_setting["word_spacing"] = template["word_spacing"]
    if "line_spacing" in template:
        page_setting["line_spacing"] = template["line_spacing"]
    if "font_size_sigma" in template:
        page_setting["font_size_sigma"] = template["font_size_sigma"]
    if "word_spacing_sigma" in template:
        page_setting["word_spacing_sigma"] = template["word_spacing_sigma"]
    if "line_spacing_sigma" in template:
        page_setting["line_spacing_sigma"] = template["line_spacing_sigma"]

    template2 = {}
    template2["page_settings"] = (page_setting, )
    template2["font"] = template["font"]
    if "color" in template:
        template2["color"] = template["color"]
    if "is_half_char" in template:
        template2["is_half_char"] = template["is_half_char"]
    if "is_end_char" in template:
        template2["is_end_char"] = template["is_end_char"]
    if "alpha" in template:
        template2["alpha"] = template["alpha"]

    return handwrite2(text, template2, anti_aliasing=anti_aliasing, worker=worker, seed=seed)


def handwrite2(text: str, template2: dict, anti_aliasing: bool = True, worker: int = 0, seed=None) -> list:
    """The 'periodic' version of handwrite. See also handwrite.

    Args:
        text: A char iterable.

        template2: A dict-like object containing following parameters.

            page_settings: A list-like object of dict-like objects containing the following parameters. Each of these
            dict-like objects will be applied cyclically to each page.

                background: A Pillow's Image instance.

                box: A bounding box as a 4-tuple defining the left, upper, right and lower pixel coordinate. The module
                uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner. This function do not
                guarantee the drawn texts will completely in the box.

                font_size: A int as the average font size in pixel. Note that (box[3] - box[1]) and (box[2] - box[0])
                both must be greater than font_size.

                word_spacing: A int as the average gap between two adjacent chars in pixel. Default: 0.

                line_spacing: A int as the average gap between two adjacent lines in pixel. Default: font_size // 5.

                font_size_sigma: A float as the sigma of the gauss distribution of the font size. Default:
                font_size / 256.

                word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing. Default:
                font_size / 256.

                line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing. Default:
                font_size / 256.

            font: A Pillow's font instance. Note that this function do not use the size attribute of the font object.

            color: A str as Pillow's color name. More info: https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names
            Default: "black".

            is_half_char: A function judging whether or not a char only take up half of its original width. The function
            must take a char parameter and return a boolean value. Default: (lambda c: False).

            is_end_char: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，',
            '。', '》', ')', ']'). The function must take a char parameter and return a boolean value. Default:
            (lambda c: c in _DEFAULT_END_CHARS).

            alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in
            order. Both values must be between 0.0 (inclusive) and 1.0 (inclusive). Default: (0.1, 0.1).

        anti_aliasing: Whether or not turn on the anti-aliasing. Default: True.

        worker: A int as the number of worker. if worker is less than or equal to 0, the actual amount of worker would
        be the number of CPU in the computer adding worker. Default: 0.

        seed: The seed of the internal random generators. Default: None.

    Returns:
        A list of drawn images with the same size and mode as the corresponding background images.

    Raises:
        ValueError: When the parameters are not be set properly.
    """
    page_settings = tuple(template2["page_settings"])
    for page_setting in page_settings:
        font_size = page_setting["font_size"]
        page_setting.setdefault("word_spacing", _DEFAULT_WORD_SPACING)
        page_setting.setdefault("line_spacing", font_size // 5)
        page_setting.setdefault("font_size_sigma", font_size / 256)
        page_setting.setdefault("word_spacing_sigma", font_size / 256)
        page_setting.setdefault("line_spacing_sigma", font_size / 256)

    return _core.handwrite(text=text,
                           page_settings=page_settings,
                           font=template2["font"],
                           color=template2.get("color", _DEFAULT_COLOR),
                           is_half_char=template2.get("is_half_char", _DEFAULT_IS_HALF_CHAR),
                           is_end_char=template2.get("is_end_char", _DEFAULT_IS_END_CHAR),
                           alpha=template2.get("alpha", _DEFAULT_ALPHA),
                           anti_aliasing=anti_aliasing,
                           worker=worker if worker > 0 else multiprocessing.cpu_count() + worker,
                           seed=seed)
