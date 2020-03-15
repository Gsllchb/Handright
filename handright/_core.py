# coding: utf-8
import itertools
import random

import math

from handright._exceptions import *
from handright._template import *
from handright._util import *

# While changing following constants, it is necessary to consider to rewrite the
# relevant codes.
_INTERNAL_MODE = "1"  # The mode for internal computation
_WHITE = 1
_BLACK = 0

_LF = "\n"
_CR = "\r"
_CRLF = "\r\n"

_UNSIGNED_INT32_TYPECODE = "L"
_MAX_INT16_VALUE = 0xFFFF
_STROKE_END = 0xFFFFFFFF


def handwrite(
        text: str,
        template: Union[Template, Sequence[Template]],
        seed: Hashable = None,
        mapper: Callable[[Callable, Iterable], Iterable] = map,
) -> Iterable[PIL.Image.Image]:
    """Handwrite `text` with the configurations in `template`, and return an
    Iterable of Pillow's Images.

    `template` could be a Template instance or a Sequence of Template
    instances. If pass a Template Sequence, the inside Template instances will
    be applied cyclically to the output pages.

    `seed` could be used for reproducibility.

    A different implementation of map built-in function (only accept one
    Iterable though) could be passed to `mapper` to boost the page rendering
    process, e.g. `multiprocessing.Pool.map`.

    Throw BackgroundTooLargeError, if the width or height of `background` in
    `template` exceeds 65,534.
    Throw LayoutError, if the settings are conflicting, which makes it
    impossible to layout the `text`.
    """
    if isinstance(template, Template):
        templates = (template,)
    else:
        templates = template
    pages = _draft(text, templates, seed)
    renderer = _Renderer(templates, seed)
    return mapper(renderer, pages)


def _draft(text, templates, seed=None) -> Iterator[Page]:
    text = _preprocess_text(text)
    template_iter = itertools.cycle(templates)
    num_iter = itertools.count()
    rand = random.Random(x=seed)
    start = 0
    while start < len(text):
        template = next(template_iter)
        page = Page(_INTERNAL_MODE, template.get_size(), _BLACK, next(num_iter))
        start = _draw_page(page, text, start, template, rand)
        yield page


def _preprocess_text(text: str) -> str:
    return text.replace(_CRLF, _LF).replace(_CR, _LF)


def _check_template(page, template) -> None:
    if page.height() < (template.get_top_margin() + template.get_line_spacing()
                        + template.get_bottom_margin()):
        msg = "for (height < top_margin + line_spacing + bottom_margin)"
        raise LayoutError(msg)
    if template.get_font_size() > template.get_line_spacing():
        msg = "for (font_size > line_spacing)"
        raise LayoutError(msg)
    if page.width() < (template.get_left_margin() + template.get_font_size()
                       + template.get_right_margin()):
        msg = "for (width < left_margin + font_size + right_margin)"
        raise LayoutError(msg)
    if template.get_word_spacing() <= -template.get_font_size() // 2:
        msg = "for (word_spacing <= -font_size // 2)"
        raise LayoutError(msg)


def _draw_page(page, text, start: int, template, rand: random.Random) -> int:
    _check_template(page, template)

    width = page.width()
    height = page.height()

    font = template.get_font()
    top_margin = template.get_top_margin()
    bottom_margin = template.get_bottom_margin()
    left_margin = template.get_left_margin()
    right_margin = template.get_right_margin()
    line_spacing = template.get_line_spacing()
    font_size = template.get_font_size()
    word_spacing = template.get_word_spacing()
    end_chars = template.get_end_chars()
    line_spacing_sigma = template.get_line_spacing_sigma()
    font_size_sigma = template.get_font_size_sigma()
    word_spacing_sigma = template.get_word_spacing_sigma()

    draw = page.draw()
    y = top_margin + line_spacing - font_size
    while y <= height - bottom_margin - font_size:
        x = left_margin
        while True:
            if text[start] == _LF:
                start += 1
                if start == len(text):
                    return start
                break
            if (x > width - right_margin - font_size
                    and text[start] not in end_chars):
                break
            xy = (round(x), round(rand.gauss(y, line_spacing_sigma)))
            actual_font_size = max(
                round(rand.gauss(font_size, font_size_sigma)), 0
            )
            if actual_font_size != font.size:
                font = font.font_variant(size=actual_font_size)
            offset = _draw_char(draw, text[start], xy, font)
            x += rand.gauss(word_spacing + offset, word_spacing_sigma)
            start += 1
            if start == len(text):
                return start
        y += line_spacing
    return start


def _draw_char(draw, char: str, xy: Tuple[int, int], font) -> int:
    """Draws a single char with the parameters and white color, and returns the
    offset."""
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer(object):
    """A callable object rendering the foreground that was drawn text and
    returning rendered image."""

    __slots__ = (
        "_templates",
        "_rand",
        "_hashed_seed",
    )

    def __init__(self, templates, seed=None) -> None:
        self._templates = _to_picklable(templates)
        self._rand = random.Random()
        self._hashed_seed = None
        if seed is not None:
            self._hashed_seed = hash(seed)

    def __call__(self, page) -> PIL.Image.Image:
        if self._hashed_seed is None:
            # avoid different processes sharing the same random state
            self._rand.seed()
        else:
            self._rand.seed(a=self._hashed_seed + page.num)
        return self._perturb_and_merge(page)

    def _perturb_and_merge(self, page) -> PIL.Image.Image:
        template = _get_template(self._templates, page.num)
        canvas = template.get_background().copy()
        bbox = page.image.getbbox()
        if bbox is None:
            return canvas
        strokes = _extract_strokes(page.matrix(), bbox)
        _draw_strokes(canvas.load(), strokes, template, self._rand)
        return canvas


def _to_picklable(templates: Sequence[Template]) -> Sequence[Template]:
    templates = copy_templates(templates)
    for t in templates:
        t.release_font_resource()
    return templates


def _get_template(templates, index):
    return templates[index % len(templates)]


def _extract_strokes(bitmap, bbox: Tuple[int, int, int, int]):
    left, upper, right, lower = bbox
    assert left >= 0 and upper >= 0
    # reserve 0xFFFFFFFF as _STROKE_END
    if right >= _MAX_INT16_VALUE or lower >= _MAX_INT16_VALUE:
        msg = "the width or height of backgrounds can not exceed {}".format(
            _MAX_INT16_VALUE - 1
        )
        raise BackgroundTooLargeError(msg)
    strokes = NumericOrderedSet(
        _UNSIGNED_INT32_TYPECODE,
        privileged=_STROKE_END
    )
    for y in range(upper, lower):
        for x in range(left, right):
            if bitmap[x, y] and strokes.add(_xy(x, y)):
                _extract_stroke(bitmap, (x, y), strokes, bbox)
                strokes.add_privileged()
    return strokes


def _extract_stroke(
        bitmap, start: Tuple[int, int], strokes, bbox: Tuple[int, int, int, int]
) -> None:
    """Helper function of _extract_strokes() which uses depth first search to
    find the pixels of a glyph."""
    left, upper, right, lower = bbox
    stack = [start, ]
    while stack:
        x, y = stack.pop()
        if y - 1 >= upper and bitmap[x, y - 1] and strokes.add(_xy(x, y - 1)):
            stack.append((x, y - 1))
        if y + 1 < lower and bitmap[x, y + 1] and strokes.add(_xy(x, y + 1)):
            stack.append((x, y + 1))
        if x - 1 >= left and bitmap[x - 1, y] and strokes.add(_xy(x - 1, y)):
            stack.append((x - 1, y))
        if x + 1 < right and bitmap[x + 1, y] and strokes.add(_xy(x + 1, y)):
            stack.append((x + 1, y))


def _draw_strokes(bitmap, strokes, template, rand) -> None:
    stroke = []
    min_x = _MAX_INT16_VALUE
    min_y = _MAX_INT16_VALUE
    max_x = 0
    max_y = 0
    for xy in strokes:
        if xy == _STROKE_END:
            center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
            _draw_stroke(bitmap, stroke, template, center, rand)
            min_x = _MAX_INT16_VALUE
            min_y = _MAX_INT16_VALUE
            max_x = 0
            max_y = 0
            stroke.clear()
            continue
        x, y = _x_y(xy)
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        stroke.append((x, y))


def _draw_stroke(
        bitmap,
        stroke: Sequence[Tuple[int, int]],
        template,
        center: Tuple[float, float],
        rand
) -> None:
    dx = rand.gauss(0, template.get_perturb_x_sigma())
    dy = rand.gauss(0, template.get_perturb_y_sigma())
    theta = rand.gauss(0, template.get_perturb_theta_sigma())
    for x, y in stroke:
        new_x, new_y = _rotate(center, x, y, theta)
        new_x = round(new_x + dx)
        new_y = round(new_y + dy)
        width, height = template.get_size()
        if 0 <= new_x < width and 0 <= new_y < height:
            bitmap[new_x, new_y] = template.get_fill()


def _rotate(
        center: Tuple[float, float], x: float, y: float, theta: float
) -> Tuple[float, float]:
    if theta == 0:
        return x, y
    new_x = ((x - center[0]) * math.cos(theta)
             + (y - center[1]) * math.sin(theta)
             + center[0])
    new_y = ((y - center[1]) * math.cos(theta)
             - (x - center[0]) * math.sin(theta)
             + center[1])
    return new_x, new_y


def _xy(x: int, y: int) -> int:
    return (x << 16) | y


def _x_y(xy: int) -> Tuple[int, int]:
    return xy >> 16, xy & 0xFFFF
