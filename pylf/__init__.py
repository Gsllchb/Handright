# coding: utf-8
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
_DEFAULT_IS_HALF_CHAR_FN = lambda c: False
_DEFAULT_IS_END_CHAR_FN = lambda c: c in _DEFAULT_END_CHARS
_DEFAULT_ALPHA = (0.1, 0.1)


def handwrite(text: str, template: dict, *, worker: int = multiprocessing.cpu_count(), seed=None) -> list:
    """Handwrite the text with the parameters in the template.

    Args:
        text: A char iterable.

        template: A dict-like object containing following parameters.

            background: A Pillow's Image instance.

            margin: #TODO

            line_spacing: A int as the average gap between two adjacent lines in pixel.

            font_size: A int as the average font size in pixel.

            word_spacing: A int as the average gap between two adjacent chars in pixel. Default: 0.

            font: A Pillow's font instance. Note that this function do not use the size attribute of the font instance.

            color: A str as Pillow's color name. More info: https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names
            Default: "black".

            line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing. Default:
            font_size / 256.

            font_size_sigma: A float as the sigma of the gauss distribution of the font size. Default: font_size / 256.

            word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing. Default:
            font_size / 256.

            is_half_char_fn: A function judging whether or not a char only take up half of its original width. The function
            must take a char parameter and return a boolean value. Default: (lambda c: False).

            is_end_char_fn: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，',
            '。', '》', ')', ']'). The function must take a char parameter and return a boolean value. Default:
            (lambda c: c in _DEFAULT_END_CHARS).

            alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in
            order. Both values must be between 0.0 (inclusive) and 1.0 (inclusive). Default: (0.1, 0.1).

        worker: A int as the number of worker. Default: multiprocessing.cpu_count().

        seed: The seed of the internal random generators. Default: None.

    Returns:
        A list of drawn images with the same size and mode as the background image.

    Raises:
        ValueError: When the parameters are not be set properly.
    """
    template2 = dict(template)
    template2["backgrounds"] = (template["background"], )
    template2["margins"] = (template["margin"], )
    template2["line_spacings"] = (template["line_spacing"], )
    template2["font_sizes"] = (template["font_size"], )
    if "word_spacing" in template:
        template2["word_spacings"] = (template["word_spacing"], )
    if "line_spacing_sigma" in template:
        template2["line_spacing_sigmas"] = (template["line_spacing_sigma"], )
    if "font_size_sigma" in template:
        template2["font_size_sigmas"] = (template["font_size_sigma"], )
    if "word_spacing_sigma" in template:
        template2["word_spacing_sigmas"] = (template["word_spacing_sigma"], )
    return handwrite2(text, template2, worker=worker, seed=seed)


def handwrite2(text: str, template2: dict, *, worker: int = multiprocessing.cpu_count(), seed=None) -> list:
    """The 'periodic' version of handwrite. See also handwrite().
    TODO
    """
    word_spacings = template2.get("word_spacings", tuple(_DEFAULT_WORD_SPACING for _ in template2["backgrounds"]))
    line_spacing_sigmas = template2.get("line_spacing_sigmas", tuple(i / 256 for i in template2["font_sizes"]))
    font_size_sigmas = template2.get("font_size_sigmas", tuple(i / 256 for i in template2["font_sizes"]))
    word_spacing_sigmas = template2.get("word_spacing_sigmas", tuple(i / 256 for i in template2["font_sizes"]))
    color = template2.get("color", _DEFAULT_COLOR)
    is_half_char_fn = template2.get("is_half_char_fn", _DEFAULT_IS_HALF_CHAR_FN)
    is_end_char_fn = template2.get("is_end_char_fn", _DEFAULT_IS_END_CHAR_FN)
    alpha = template2.get("alpha", _DEFAULT_ALPHA)
    return _core.handwrite(text=text, backgrounds=template2["backgrounds"], margins=template2["margins"],
                           line_spacings=template2["line_spacings"], font_sizes=template2["font_sizes"],
                           word_spacings=word_spacings, line_spacing_sigmas=line_spacing_sigmas,
                           font_size_sigmas=font_size_sigmas, word_spacing_sigmas=word_spacing_sigmas,
                           font=template2["font"], color=color, is_half_char_fn=is_half_char_fn,
                           is_end_char_fn=is_end_char_fn, alpha=alpha, worker=worker, seed=seed)
