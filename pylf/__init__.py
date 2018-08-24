# coding: utf-8
"""PyLf is a lightweight Python library for simulating Chinese handwriting. It introduces a great deal of randomness in
the process of Chinese handwriting to simulate the uncertainty of glyphs written by human beings. Currently, PyLf is
built on the top of Pillow library.
"""
import multiprocessing
from collections import abc

from PIL import Image

from pylf import _core

__version__ = "1.4.0"

_CHECK_PARAMETERS = True

# Chinese, English and other end chars
_DEFAULT_END_CHARS = frozenset("，。》、？；：’”】｝、！％）" + ",.>?;:]}!%)" + "′″℃℉")

_DEFAULT_WORD_SPACING = 0
_DEFAULT_COLOR = "black"
_DEFAULT_IS_HALF_CHAR_FN = lambda c: False
_DEFAULT_IS_END_CHAR_FN = lambda c: c in _DEFAULT_END_CHARS
_DEFAULT_PERTURB_THETA_SIGMA = 1.0  # TODO: tune this value


def handwrite(text: str, template: dict, *, worker: int = multiprocessing.cpu_count(), seed=None) -> list:
    """Handwrite the text with the parameters in the template.

    Args:
        text: A char iterable.

        template: A dict-like object containing following parameters.

            background: A Pillow's Image instance. Recommended mode: "1", "L", "RGB".

            margin: TODO

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

            perturb_x_sigma: TODO

            perturb_y_sigma: TODO

            perturb_theta_sigma: TODO

        worker: A int as the number of worker. Default: multiprocessing.cpu_count().

        seed: The seed of the internal random generators. Default: None.

    Returns:
        A list of drawn images with the same size and mode as the background image.
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

    if "perturb_x_sigma" in template:
        template2["perturb_x_sigmas"] = (template["perturb_x_sigma"], )
    if "perturb_y_sigma" in template:
        template2["perturb_y_sigmas"] = (template["perturb_y_sigma"], )
    if "perturb_theta_sigma" in template:
        template2["perturb_theta_sigmas"] = (template["perturb_theta_sigma"], )

    return handwrite2(text, template2, worker=worker, seed=seed)


def handwrite2(text: str, template2: dict, *, worker: int = multiprocessing.cpu_count(), seed=None) -> list:
    """The 'periodic' version of handwrite. See also handwrite().
    TODO
    """
    if _CHECK_PARAMETERS:
        _check_parameters(text, template2, worker, seed)

    font_sizes = template2["font_sizes"]

    word_spacings = template2.get("word_spacings", tuple(_DEFAULT_WORD_SPACING for _ in font_sizes))

    line_spacing_sigmas = template2.get("line_spacing_sigmas", tuple(i / 256 for i in font_sizes))
    font_size_sigmas = template2.get("font_size_sigmas", tuple(i / 256 for i in font_sizes))
    word_spacing_sigmas = template2.get("word_spacing_sigmas", tuple(i / 256 for i in font_sizes))

    color = template2.get("color", _DEFAULT_COLOR)

    is_half_char_fn = template2.get("is_half_char_fn", _DEFAULT_IS_HALF_CHAR_FN)
    is_end_char_fn = template2.get("is_end_char_fn", _DEFAULT_IS_END_CHAR_FN)

    perturb_x_sigmas = template2.get("perturb_x_sigmas", tuple(i / 500 for i in font_sizes))
    perturb_y_sigmas = template2.get("perturb_y_sigmas", tuple(i / 500 for i in font_sizes))
    perturb_theta_sigmas = template2.get("perturb_theta_sigmas",
                                         tuple(_DEFAULT_PERTURB_THETA_SIGMA for _ in font_sizes))

    return _core.handwrite(text=text,
                           backgrounds=template2["backgrounds"],
                           margins=template2["margins"],
                           line_spacings=template2["line_spacings"],
                           font_sizes=template2["font_sizes"],
                           word_spacings=word_spacings,
                           line_spacing_sigmas=line_spacing_sigmas,
                           font_size_sigmas=font_size_sigmas,
                           word_spacing_sigmas=word_spacing_sigmas,
                           font=template2["font"],
                           color=color,
                           is_half_char_fn=is_half_char_fn,
                           is_end_char_fn=is_end_char_fn,
                           perturb_x_sigmas=perturb_x_sigmas,
                           perturb_y_sigmas=perturb_y_sigmas,
                           perturb_theta_sigmas=perturb_theta_sigmas,
                           worker=worker,
                           seed=seed)


########################################################################################################################
#                                              Parameter checking                                                      #
########################################################################################################################
def _check_parameters(text, template2, worker, seed) -> None:
    _check_text(text)
    _check_template2(template2)
    _check_worker(worker)
    _check_seed(seed)


def _check_text(text) -> None:
    if not isinstance(text, abc.Iterable):
        raise TypeError("'text' must be char iterable")


def _check_template2(template2) -> None:
    if not isinstance(template2, abc.Mapping):
        raise TypeError("'template2' must be mapping")

    length = len(template2["backgrounds"])
    if length <= 0:
        raise ValueError("The length of 'backgrounds' must be at least 1")

    if not (length == len(template2["margins"]) == len(template2["line_spacings"]) == len(template2["font_sizes"])):
        raise ValueError("'backgrounds', 'margins', 'line_spacings' and 'font_sizes' must have the same length")

    for b in template2["backgrounds"]:
        if not isinstance(b, Image.Image):
            raise TypeError("'background' must be Pillow's image")

    for m in template2["margins"]:
        for key in ("top", "bottom", "left", "right"):
            if not isinstance(m[key], int):
                raise TypeError("'margin[\"{}\"]' must be int".format(key))
            if m[key] < 0:
                raise ValueError("'margin[\"{}\"]' must be at least 0".format(key))

    for b, m, ls in zip(template2["backgrounds"], template2["margins"], template2["line_spacings"]):
        if not isinstance(ls, int):
            raise TypeError("'line_spacing' must be int")
        if ls <= 0:
            raise ValueError("'line_spacing' must be at least 1")
        if b.size[1] < m["top"] + ls + m["bottom"]:
            raise ValueError("'margin[\"top\"] + line_spacing + margin[\"bottom\"]' "
                             "can not be greater than background's height")

    for b, m, ls, fs in zip(template2["backgrounds"], template2["margins"], template2["line_spacings"],
                            template2["font_sizes"]):
        if not isinstance(fs, int):
            raise TypeError("'font_size' must be int")
        if fs <= 0:
            raise ValueError("'font_size' must be at least 1")
        if fs > ls:
            raise ValueError("'font_size' can not be greater than 'line_spacing'")
        if b.size[0] < m["left"] + fs + m["right"]:
            raise ValueError("'margin[\"left\"] + font_size + margin[\"right\"]' "
                             "can not be greater than background's width")

    if "word_spacings" in template2:
        if len(template2["word_spacings"]) != length:
            raise ValueError("'word_spacings' and 'backgrounds' must have the same length")
        for ws in template2["word_spacings"]:
            if not isinstance(ws, int):
                raise TypeError("'word_spacing' must be int")
            if ws < 0:
                raise ValueError("'word_spacing' must be at least 0")

    # TODO: check font

    if "color" in template2:
        if not isinstance(template2["color"], str):
            raise TypeError("'color' must be str")

    for sigmas in ("line_spacing_sigmas", "font_size_sigmas", "word_spacing_sigmas", "perturb_x_sigmas",
                   "perturb_y_sigmas", "perturb_theta_sigmas"):
        if sigmas in template2:
            if len(template2[sigmas]) != length:
                raise ValueError("'{}' and 'backgrounds' must have the same length".format(sigmas))
            for s in template2[sigmas]:
                if not isinstance(s, (int, float)):
                    raise TypeError("'{}' must be int or float".format(sigmas[:-1]))
                if s < 0:
                    raise ValueError("'{}' must be at least 0")

    for fn in ("is_half_char_fn", "is_end_char_fn"):
        if fn in template2:
            if not callable(template2[fn]):
                raise TypeError("'{}' must be callable".format(fn))


def _check_worker(worker) -> None:
    if not isinstance(worker, int):
        raise TypeError("'worker' must be int")
    if worker <= 0:
        raise ValueError("'worker' must be at least 1")


def _check_seed(seed) -> None:
    if not isinstance(seed, abc.Hashable):
        raise TypeError("'seed' must be hashable")
