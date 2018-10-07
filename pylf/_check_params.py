# coding: utf-8
"""Check the parameters of public interfaces"""
import collections.abc
import numbers

import PIL.Image


_MAX_IMAGE_SIDE_LENGTH = 0xFFFF - 1  # 65534


def check_params(text, template2, worker, seed) -> None:
    _check_text(text)
    _check_template2(template2)
    _check_worker(worker)
    _check_seed(seed)


def _check_text(text) -> None:
    if not isinstance(text, str):
        raise TypeError("'text' must be str")


def _check_template2(template2) -> None:
    if not isinstance(template2, collections.abc.Mapping):
        raise TypeError("'template2' must be Mapping")

    length = len(template2["backgrounds"])
    if length <= 0:
        raise ValueError("The length of 'backgrounds' must be at least 1")

    if not (length == len(template2["margins"]) == len(template2["line_spacings"]) == len(template2["font_sizes"])):
        raise ValueError("'backgrounds', 'margins', 'line_spacings' and 'font_sizes' must have the same length")

    # check backgrounds
    if not all(isinstance(b, PIL.Image.Image) for b in template2["backgrounds"]):
        raise TypeError("'background' must be Pillow's Image")
    if not all(b.width <= _MAX_IMAGE_SIDE_LENGTH for b in template2["backgrounds"]):
        raise ValueError("The width of background cannot exceed {}".format(_MAX_IMAGE_SIDE_LENGTH))
    if not all(b.height <= _MAX_IMAGE_SIDE_LENGTH for b in template2["backgrounds"]):
        raise ValueError("The height of background cannot exceed {}".format(_MAX_IMAGE_SIDE_LENGTH))

    # check margins
    for m in template2["margins"]:
        for key in ("top", "bottom", "left", "right"):
            if not isinstance(m[key], numbers.Integral):
                raise TypeError("'margin[\"{}\"]' must be Integral".format(key))
            if m[key] < 0:
                raise ValueError("'margin[\"{}\"]' must be at least 0".format(key))

    # check line_spacings
    if not all(isinstance(ls, numbers.Integral) for ls in template2["line_spacings"]):
        raise TypeError("'line_spacing' must be Integral")
    if not all(ls >= 1 for ls in template2["line_spacings"]):
        raise ValueError("'line_spacing' must be at least 1")
    if not all(b.height >= m["top"] + ls + m["bottom"] for b, m, ls
               in zip(template2["backgrounds"], template2["margins"], template2["line_spacings"])):
        raise ValueError("'margin[\"top\"] + line_spacing + margin[\"bottom\"]'"
                         " can not be greater than background's height")

    # check font_sizes
    if not all(isinstance(fs, numbers.Integral) for fs in template2["font_sizes"]):
        raise TypeError("'line_spacing' must be Integral")
    if not all(fs >= 1 for fs in template2["font_sizes"]):
        raise ValueError("'font_size' must be at least 1")
    if not all(fs <= ls for fs, ls in zip(template2["font_sizes"], template2["line_spacings"])):
        raise ValueError("'font_size' can not be greater than 'line_spacing'")

    if not all(b.width >= m["left"] + fs + m["right"] for b, m, fs
               in zip(template2["backgrounds"], template2["margins"], template2["font_sizes"])):
        raise ValueError("'margin[\"left\"] + font_size + margin[\"right\"]'"
                         " can not be greater than background's width")

    # check word_spacings
    if "word_spacings" in template2:
        if len(template2["word_spacings"]) != length:
            raise ValueError("'word_spacings' and 'backgrounds' must have the same length")
        if not all(isinstance(ws, numbers.Integral) for ws in template2["word_spacings"]):
            raise TypeError("'word_spacing' must be Integral")
        if not all(ws > -fs // 2 for ws, fs in zip(template2["word_spacings"], template2["font_sizes"])):
            raise ValueError("'word_spacing' must be greater than (-font_size // 2)")

    # TODO: check font

    # check color
    if "color" in template2 and not isinstance(template2["color"], str):
        raise TypeError("'color' must be str")

    # check *_sigmas
    for sigmas in ("line_spacing_sigmas", "font_size_sigmas", "word_spacing_sigmas", "perturb_x_sigmas",
                   "perturb_y_sigmas", "perturb_theta_sigmas"):
        if sigmas in template2:
            if len(template2[sigmas]) != length:
                raise ValueError("'{}' and 'backgrounds' must have the same length".format(sigmas))
            if not all(isinstance(s, numbers.Real) for s in template2[sigmas]):
                raise TypeError("'{}' must be Real".format(sigmas[:-1]))
            if not all(s >= 0.0 for s in template2[sigmas]):
                raise ValueError("'{}' must be at least 0.0")

    # check *_fn
    for fn in ("is_half_char_fn", "is_end_char_fn"):
        if fn in template2 and not isinstance(template2[fn], collections.abc.Callable):
            raise TypeError("'{}' must be Callable".format(fn))


def _check_worker(worker) -> None:
    if worker is None:
        return
    if not isinstance(worker, numbers.Integral):
        raise TypeError("'worker' must be Integral or None")
    if worker <= 0:
        raise ValueError("'worker' must be at least 1")


def _check_seed(seed) -> None:
    if not isinstance(seed, collections.abc.Hashable):
        raise TypeError("'seed' must be Hashable")
