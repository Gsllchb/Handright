# coding: utf-8
"""A lightweight Python library for simulating Chinese handwriting

Vision: Reveal the nature of Chinese handwriting and use it to implement
beautiful, simple and easy-to-use interfaces.

Algorithm: Randomly perturb each character as a whole in horizontal position,
vertical position and font size. Then, Randomly perturb each stroke of a
character in horizontal position, vertical position and rotation angle.

Implementation: Develop on the top of Pillow and use multiprocessing for
internal parallel acceleration.

Homepage: https://github.com/Gsllchb/PyLf
"""
import multiprocessing
from typing import *

import PIL.Image

from pylf import _check_params
from pylf import _core
from pylf._exceptions import LayoutError

__all__ = (
    "handwrite",
    "handwrite2",
    "DEFAULT_HALF_CHARS",
    "DEFAULT_END_CHARS",
    "LayoutError",
)
__version__ = "3.3.1"

_CHECK_PARAMETERS = True

DEFAULT_HALF_CHARS = frozenset("")
# Chinese, English and other end chars
DEFAULT_END_CHARS = frozenset(
    "，。》、？；：’”】｝、！％）"
    ",.>?;:]}!%)"
    "′″℃℉"
)

_DEFAULT_WORD_SPACING = 0
_DEFAULT_COLOR = "black"
_DEFAULT_PERTURB_THETA_SIGMA = 0.07


def handwrite(
        text: str,
        template: Mapping[str, Any],
        *,
        worker: Optional[int] = None,
        seed: Hashable = None
) -> List[PIL.Image.Image]:
    """Handwrite the text with the parameters in the template.

    Args:
        text: A str.

        template: A dict-like object containing following parameters.

            background: A Pillow's Image instance. The mode must be one of "1",
            "L", "RGB" and "RGBA". The width and the height of the image cannot
            exceed 65534.

            margin: A dict-like object. margin["top"], margin["bottom"],
            margin["left"] and margin["right"] are used together to define the
            handwritten area in background. (unit: pixel)

            line_spacing: The average gap between two adjacent lines. (unit:
            pixel)

            font_size: Average font size. (unit: pixel)

            word_spacing: The average gap between two adjacent chars. This value
            must be greater than (-font_size // 2). Default: 0. (unit: pixel)

            font: A Pillow's font instance. The size attribute of the font
            instance will be ignored here.

            color: A Pillow's color name. More info: https://pillow.readthedocs.io/en/5.2.x/reference/ImageColor.html#color-names
            Default: "black".

            line_spacing_sigma: The sigma of the gauss distribution of line
            spacing. Default: font_size / 32.

            font_size_sigma: The sigma of the gauss distribution of font size.
            Default: font_size / 64.

            word_spacing_sigma: The sigma of the gauss distribution of word
            spacing. Default: font_size / 32.

            is_half_char_fn: A function judging whether or not a char only take
            up half of its original width. The function must take a char
            parameter and return a bool value. Default:
            (lambda c: c in DEFAULT_HALF_CHARS).

            is_end_char_fn: A function judging whether or not a char cannot be
            in the beginning of the lines (e.g. '，', '。', '》', ')', ']'). It
            must take a char parameter and return a bool value. Default:
            (lambda c: c in DEFAULT_END_CHARS).

            perturb_x_sigma: The sigma of the gauss distribution of the
            horizontal position of strokes. Default: font_size / 32.

            perturb_y_sigma: The sigma of the gauss distribution of the vertical
            position of strokes. Default: font_size / 32.

            perturb_theta_sigma: The sigma of the gauss distribution of the
            rotation of strokes. Default: 0.07.

        worker: The maximum number of concurrently running jobs. Especially,
        when worker equals 1, it will use a single-threaded algorithm instead.
        Recommended not to be greater than multiprocessing.cpu_count(). Default:
        multiprocessing.cpu_count().

        seed: The seed for internal random generators. Default: None.

    Returns:
        A list of drawn images with the same size and mode as background image.

    Example:
    >>> from PIL import Image, ImageFont
    >>> from pylf import handwrite
    >>>
    >>>
    >>> if __name__ == '__main__':
    >>>     template = {
    >>>         "background": Image.new(
    >>>             mode="1",
    >>>             size=(2000, 2000),
    >>>             color="white"
    >>>         ),
    >>>         "margin": {
    >>>             "left": 150,
    >>>             "right": 150,
    >>>             "top": 200,
    >>>             "bottom": 200
    >>>         },
    >>>         "line_spacing": 150,
    >>>         "font_size": 100,
    >>>         "font": ImageFont.truetype("path/to/my/font.ttf")
    >>>     }
    >>>     for image in handwrite("我能吞下玻璃而不伤身体。", template):
    >>>         image.show()
    >>>
    """
    template2 = dict(template)

    template2["backgrounds"] = (template["background"],)
    template2["margins"] = (template["margin"],)
    template2["line_spacings"] = (template["line_spacing"],)
    template2["font_sizes"] = (template["font_size"],)

    if "word_spacing" in template:
        template2["word_spacings"] = (template["word_spacing"],)

    if "line_spacing_sigma" in template:
        template2["line_spacing_sigmas"] = (template["line_spacing_sigma"],)
    if "font_size_sigma" in template:
        template2["font_size_sigmas"] = (template["font_size_sigma"],)
    if "word_spacing_sigma" in template:
        template2["word_spacing_sigmas"] = (template["word_spacing_sigma"],)

    if "perturb_x_sigma" in template:
        template2["perturb_x_sigmas"] = (template["perturb_x_sigma"],)
    if "perturb_y_sigma" in template:
        template2["perturb_y_sigmas"] = (template["perturb_y_sigma"],)
    if "perturb_theta_sigma" in template:
        template2["perturb_theta_sigmas"] = (template["perturb_theta_sigma"],)

    return handwrite2(text, template2, worker=worker, seed=seed)


def handwrite2(
        text: str,
        template2: Mapping[str, Any],
        *,
        worker: Optional[int] = None,
        seed: Hashable = None
) -> List[PIL.Image.Image]:
    """The 'periodic' version of handwrite. See also handwrite().
    The parameters of handwrite2() and handwrite() are similar. The difference
    is that some of the parameters in the template of handwrite() are replaced
    with their plural form in template2. These 'plural' parameters become a
    sequence of the corresponding original parameters. And these 'plural'
    parameters in template2 will be use periodically in the sequence of
    handwritten images.

    The original parameters and their corresponding 'plural' parameters as well
    as their default values, if any, are listed below.
    background -> backgrounds
    margin -> margins
    line_spacing -> line_spacings
    font_size -> font_sizes
    word_spacing -> word_spacings (Default: a list of 0)
    line_spacing_sigma -> line_spacing_sigmas (Default: [i / 32 for i in font_sizes])
    font_size_sigma -> font_size_sigmas (Default: [i / 64 for i in font_sizes])
    word_spacing_sigma -> word_spacing_sigmas (Default: [i / 32 for i in font_sizes])
    perturb_x_sigma -> perturb_x_sigmas (Default: [i / 32 for i in font_sizes])
    perturb_y_sigma -> perturb_y_sigmas (Default: [i / 32 for i in font_sizes])
    perturb_theta_sigma -> perturb_theta_sigmas (Default: a list of 0.07)

    Note that, all of these 'plural' parameters must have the same length.

    Example:
    >>> from PIL import Image, ImageFont
    >>> from pylf import handwrite2
    >>>
    >>>
    >>> if __name__ == '__main__':
    >>>     template2 = {
    >>>         "backgrounds": [
    >>>             Image.new(mode="1", size=(2000, 2000), color="white"),
    >>>             Image.new(mode="RGB", size=(1000, 3000), color="green")
    >>>         ],
    >>>         "margins": [
    >>>             {"left": 150, "right": 150, "top": 200, "bottom": 200},
    >>>             {"left": 100, "right": 100, "top": 300, "bottom": 300}
    >>>         ],
    >>>         "line_spacings": [150, 200],
    >>>         "font_sizes": [100, 90],
    >>>         "font": ImageFont.truetype("path/to/my/font.ttf")
    >>>     }
    >>>     for image in handwrite2("我能吞下玻璃而不伤身体。" * 30, template2):
    >>>         image.show()
    >>>
    """
    if _CHECK_PARAMETERS:
        _check_params.check_params(text, template2, worker, seed)

    font_sizes = template2["font_sizes"]

    word_spacings = template2.get(
        "word_spacings",
        tuple(_DEFAULT_WORD_SPACING for _ in font_sizes)
    )

    line_spacing_sigmas = template2.get(
        "line_spacing_sigmas",
        tuple(i / 32 for i in font_sizes)
    )
    font_size_sigmas = template2.get(
        "font_size_sigmas",
        tuple(i / 64 for i in font_sizes)
    )
    word_spacing_sigmas = template2.get(
        "word_spacing_sigmas",
        tuple(i / 32 for i in font_sizes)
    )

    color = template2.get("color", _DEFAULT_COLOR)

    is_half_char_fn = template2.get(
        "is_half_char_fn",
        lambda c: c in DEFAULT_HALF_CHARS,
    )
    is_end_char_fn = template2.get(
        "is_end_char_fn",
        lambda c: c in DEFAULT_END_CHARS,
    )

    perturb_x_sigmas = template2.get(
        "perturb_x_sigmas",
        tuple(i / 32 for i in font_sizes)
    )
    perturb_y_sigmas = template2.get(
        "perturb_y_sigmas",
        tuple(i / 32 for i in font_sizes)
    )
    perturb_theta_sigmas = template2.get(
        "perturb_theta_sigmas",
        tuple(_DEFAULT_PERTURB_THETA_SIGMA for _ in font_sizes)
    )

    if worker is None:
        worker = multiprocessing.cpu_count()

    return _core.handwrite(
        text=text,
        # If template2["backgrounds"] is already a tuple, CPython will share it
        # instead of creating a new copy of it.
        backgrounds=tuple(template2["backgrounds"]),
        top_margins=tuple(m["top"] for m in template2["margins"]),
        bottom_margins=tuple(m["bottom"] for m in template2["margins"]),
        left_margins=tuple(m["left"] for m in template2["margins"]),
        right_margins=tuple(m["right"] for m in template2["margins"]),
        line_spacings=tuple(template2["line_spacings"]),
        font_sizes=tuple(font_sizes),
        word_spacings=tuple(word_spacings),
        line_spacing_sigmas=tuple(line_spacing_sigmas),
        font_size_sigmas=tuple(font_size_sigmas),
        word_spacing_sigmas=tuple(word_spacing_sigmas),
        font=template2["font"],
        color=color,
        is_half_char_fn=is_half_char_fn,
        is_end_char_fn=is_end_char_fn,
        perturb_x_sigmas=tuple(perturb_x_sigmas),
        perturb_y_sigmas=tuple(perturb_y_sigmas),
        perturb_theta_sigmas=tuple(perturb_theta_sigmas),
        worker=worker,
        seed=seed,
    )
