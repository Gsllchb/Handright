# coding: utf-8
"""Check the parameters of public interfaces"""
import collections.abc
import numbers

import PIL.Image


_SUPPORTED_MODES = ("1", "L", "RGB", "RGBA")
_MAX_IMAGE_SIDE_LENGTH = 0xFFFF - 1
assert 0xFFFF - 1 == 65534


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

    if not (
        length
        == len(template2["margins"])
        == len(template2["line_spacings"])
        == len(template2["font_sizes"])
    ):
        raise ValueError(
            "'backgrounds', 'margins', 'line_spacings' and 'font_sizes'"
            " must have the same length"
        )

    _check_backgrounds(template2["backgrounds"])
    _check_margins(template2["margins"])
    _check_line_spacings(template2["line_spacings"])
    _check_font_sizes(template2["font_sizes"])

    if "word_spacings" in template2:
        if len(template2["word_spacings"]) != length:
            raise ValueError(
                "'word_spacings' and 'backgrounds' must have the same length"
            )
        _check_word_spacings(template2["word_spacings"])

    _check_font(template2["font"])

    if "color" in template2:
        _check_color(template2["color"])

    if "line_spacing_sigmas" in template2:
        if len(template2["line_spacing_sigmas"]) != length:
            raise ValueError(
                "'line_spacing_sigmas' and 'backgrounds'"
                " must have the same length"
            )
        _check_line_spacing_sigmas(template2["line_spacing_sigmas"])

    if "font_size_sigmas" in template2:
        if len(template2["font_size_sigmas"]) != length:
            raise ValueError(
                "'font_size_sigmas' and 'backgrounds' must have the same length"
            )
        _check_font_size_sigmas(template2["font_size_sigmas"])

    if "word_spacing_sigmas" in template2:
        if len(template2["word_spacing_sigmas"]) != length:
            raise ValueError(
                "'word_spacing_sigmas' and 'backgrounds'"
                " must have the same length"
            )
        _check_word_spacing_sigmas(template2["word_spacing_sigmas"])

    if "perturb_x_sigmas" in template2:
        if len(template2["perturb_x_sigmas"]) != length:
            raise ValueError(
                "'perturb_x_sigmas' and 'backgrounds' must have the same length"
            )
        _check_perturb_x_sigmas(template2["perturb_x_sigmas"])

    if "perturb_y_sigmas" in template2:
        if len(template2["perturb_y_sigmas"]) != length:
            raise ValueError(
                "'perturb_y_sigmas' and 'backgrounds' must have the same length"
            )
        _check_perturb_y_sigmas(template2["perturb_y_sigmas"])

    if "perturb_theta_sigmas" in template2:
        if len(template2["perturb_theta_sigmas"]) != length:
            raise ValueError(
                "'perturb_theta_sigmas' and 'backgrounds'"
                " must have the same length"
            )
        _check_perturb_theta_sigmas(template2["perturb_theta_sigmas"])

    if "is_half_char_fn" in template2:
        _check_is_half_char_fn(template2["is_half_char_fn"])

    if "is_end_char_fn" in template2:
        _check_is_end_char_fn(template2["is_end_char_fn"])


def _check_backgrounds(backgrounds) -> None:
    if not all(isinstance(b, PIL.Image.Image) for b in backgrounds):
        raise TypeError("Background must be Pillow's Image")
    for b in backgrounds:
        if b.mode not in _SUPPORTED_MODES:
            raise NotImplementedError(
                "'{}' mode is not supported yet. Currently supported modes are"
                " {}. See how to convert a image's mode: "
                "https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert".format(
                    b.mode, str(_SUPPORTED_MODES)[1:-1]
                )
            )
    if not all(b.width <= _MAX_IMAGE_SIDE_LENGTH for b in backgrounds):
        raise ValueError(
            "The width of background cannot exceed "
            "{}".format(_MAX_IMAGE_SIDE_LENGTH)
        )
    if not all(b.height <= _MAX_IMAGE_SIDE_LENGTH for b in backgrounds):
        raise ValueError(
            "The height of background cannot exceed "
            "{}".format(_MAX_IMAGE_SIDE_LENGTH)
        )


def _check_margins(margins) -> None:
    for m in margins:
        for key in ("top", "bottom", "left", "right"):
            if not isinstance(m[key], numbers.Integral):
                raise TypeError("{} margin must be Integral".format(key))
            if m[key] < 0:
                raise ValueError("{} margin must be at least 0".format(key))


def _check_line_spacings(line_spacings) -> None:
    if not all(isinstance(ls, numbers.Integral) for ls in line_spacings):
        raise TypeError("Line spacing must be Integral")
    if not all(ls >= 1 for ls in line_spacings):
        raise ValueError("Line spacing must be at least 1")


def _check_font_sizes(font_sizes) -> None:
    if not all(isinstance(fs, numbers.Integral) for fs in font_sizes):
        raise TypeError("Font size must be Integral")
    if not all(fs >= 1 for fs in font_sizes):
        raise ValueError("Font size must be at least 1")


def _check_word_spacings(word_spacings) -> None:
    if not all(isinstance(ws, numbers.Integral) for ws in word_spacings):
        raise TypeError("Word spacing must be Integral")


def _check_font(font) -> None:
    # FIXME
    pass


def _check_color(color) -> None:
    if not isinstance(color, str):
        raise TypeError("'color' must be str")


def _check_line_spacing_sigmas(line_spacing_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in line_spacing_sigmas):
        raise TypeError("'line_spacing_sigma' must be Real")
    if not all(s >= 0.0 for s in line_spacing_sigmas):
        raise ValueError("'line_spacing_sigma' must be at least 0.0")


def _check_font_size_sigmas(font_size_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in font_size_sigmas):
        raise TypeError("'font_size_sigma' must be Real")
    if not all(s >= 0.0 for s in font_size_sigmas):
        raise ValueError("'font_size_sigma' must be at least 0.0")


def _check_word_spacing_sigmas(word_spacing_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in word_spacing_sigmas):
        raise TypeError("'word_spacing_sigma' must be Real")
    if not all(s >= 0.0 for s in word_spacing_sigmas):
        raise ValueError("'word_spacing_sigma' must be at least 0.0")


def _check_perturb_x_sigmas(perturb_x_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in perturb_x_sigmas):
        raise TypeError("'perturb_x_sigma' must be Real")
    if not all(s >= 0.0 for s in perturb_x_sigmas):
        raise ValueError("'perturb_x_sigma' must be at least 0.0")


def _check_perturb_y_sigmas(perturb_y_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in perturb_y_sigmas):
        raise TypeError("'perturb_y_sigma' must be Real")
    if not all(s >= 0.0 for s in perturb_y_sigmas):
        raise ValueError("'perturb_y_sigma' must be at least 0.0")


def _check_perturb_theta_sigmas(perturb_theta_sigmas) -> None:
    if not all(isinstance(s, numbers.Real) for s in perturb_theta_sigmas):
        raise TypeError("'perturb_theta_sigma' must be Real")
    if not all(s >= 0.0 for s in perturb_theta_sigmas):
        raise ValueError("'perturb_theta_sigma' must be at least 0.0")


def _check_is_half_char_fn(is_half_char_fn) -> None:
    if not callable(is_half_char_fn):
        raise TypeError("'is_half_char_fn' must be Callable")


def _check_is_end_char_fn(is_end_char_fn) -> None:
    if not callable(is_end_char_fn):
        raise TypeError("'is_end_char_fn' must be Callable")


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
