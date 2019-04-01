# coding: utf-8
"""The core module"""
import itertools
import math
import multiprocessing
import random
from typing import *

import PIL.Image
import PIL.ImageColor

from pylf import _exceptions
from pylf import _numeric_ordered_set as _nos
from pylf import _page

# While changing following constants, it is necessary to consider to rewrite the
# relevant codes.
_INTERNAL_MODE = "1"  # The mode for internal computation
_WHITE = 1
_BLACK = 0

_NEWLINE = "\n"

_UNSIGNED_INT32_TYPECODE = "L"
_MAX_INT16_VALUE = 0xFFFF
_STROKE_END = 0xFFFFFFFF


def handwrite(
        text: str,
        backgrounds: Sequence[PIL.Image.Image],
        top_margins: Sequence[int],
        bottom_margins: Sequence[int],
        left_margins: Sequence[int],
        right_margins: Sequence[int],
        line_spacings: Sequence[int],
        font_sizes: Sequence[int],
        word_spacings: Sequence[int],
        line_spacing_sigmas: Sequence[float],
        font_size_sigmas: Sequence[float],
        word_spacing_sigmas: Sequence[float],
        font,
        color: str,
        is_half_char_fn: Callable[[str], bool],
        is_end_char_fn: Callable[[str], bool],
        perturb_x_sigmas: Sequence[float],
        perturb_y_sigmas: Sequence[float],
        perturb_theta_sigmas: Sequence[float],
        worker: int,
        seed: Hashable,
) -> List[PIL.Image.Image]:
    pages = _draw_pages(
        text=text,
        sizes=tuple(i.size for i in backgrounds),
        top_margins=top_margins,
        bottom_margins=bottom_margins,
        left_margins=left_margins,
        right_margins=right_margins,
        line_spacings=line_spacings,
        font_sizes=font_sizes,
        word_spacings=word_spacings,
        line_spacing_sigmas=line_spacing_sigmas,
        font_size_sigmas=font_size_sigmas,
        word_spacing_sigmas=word_spacing_sigmas,
        font=font,
        is_half_char_fn=is_half_char_fn,
        is_end_char_fn=is_end_char_fn,
        seed=seed,
    )

    renderer = _Renderer(
        backgrounds=backgrounds,
        color=color,
        perturb_x_sigmas=perturb_x_sigmas,
        perturb_y_sigmas=perturb_y_sigmas,
        perturb_theta_sigmas=perturb_theta_sigmas,
        seed=seed,
    )
    if worker == 1:
        return list(map(renderer, pages))
    mp_context = multiprocessing.get_context()
    with mp_context.Pool(worker) as pool:
        return pool.map(renderer, pages)


def _draw_pages(
        text: str,
        sizes: Sequence[Tuple[int, int]],
        top_margins: Sequence[int],
        bottom_margins: Sequence[int],
        left_margins: Sequence[int],
        right_margins: Sequence[int],
        line_spacings: Sequence[int],
        font_sizes: Sequence[int],
        word_spacings: Sequence[int],
        line_spacing_sigmas: Sequence[float],
        font_size_sigmas: Sequence[float],
        word_spacing_sigmas: Sequence[float],
        font,
        is_half_char_fn: Callable[[str], bool],
        is_end_char_fn: Callable[[str], bool],
        seed: Hashable,
) -> Iterator[_page.Page]:
    sizes = itertools.cycle(sizes)
    top_margins = itertools.cycle(top_margins)
    bottom_margins = itertools.cycle(bottom_margins)
    left_margins = itertools.cycle(left_margins)
    right_margins = itertools.cycle(right_margins)
    line_spacings = itertools.cycle(line_spacings)
    font_sizes = itertools.cycle(font_sizes)
    word_spacings = itertools.cycle(word_spacings)
    line_spacing_sigmas = itertools.cycle(line_spacing_sigmas)
    font_size_sigmas = itertools.cycle(font_size_sigmas)
    word_spacing_sigmas = itertools.cycle(word_spacing_sigmas)
    nums = itertools.count()

    rand = random.Random(x=seed)
    start = 0
    while start < len(text):
        page = _page.Page(_INTERNAL_MODE, next(sizes), _BLACK, next(nums))
        start = _draw_page(
            page,
            text,
            start,
            top_margin=next(top_margins),
            bottom_margin=next(bottom_margins),
            left_margin=next(left_margins),
            right_margin=next(right_margins),
            line_spacing=next(line_spacings),
            font_size=next(font_sizes),
            word_spacing=next(word_spacings),
            line_spacing_sigma=next(line_spacing_sigmas),
            font_size_sigma=next(font_size_sigmas),
            word_spacing_sigma=next(word_spacing_sigmas),
            font=font,
            is_half_char_fn=is_half_char_fn,
            is_end_char_fn=is_end_char_fn,
            rand=rand,
        )
        yield page


def _draw_page(
        page: _page.Page,
        text: str,
        start: int,
        top_margin: int,
        bottom_margin: int,
        left_margin: int,
        right_margin: int,
        line_spacing: int,
        font_size: int,
        word_spacing: int,
        line_spacing_sigma: float,
        font_size_sigma: float,
        word_spacing_sigma: float,
        font,
        is_half_char_fn: Callable[[str], bool],
        is_end_char_fn: Callable[[str], bool],
        rand: random.Random,
) -> int:
    if page.height < top_margin + line_spacing + bottom_margin:
        msg = "The sum of top margin, line spacing and bottom margin can not be greater than background's height"
        raise _exceptions.LayoutError(msg)
    if font_size > line_spacing:
        msg = "Font size can not be greater than line spacing"
        raise _exceptions.LayoutError(msg)
    if page.width < left_margin + font_size + right_margin:
        msg = "The sum of left margin, font size and right margin can not be greater than background's width"
        raise _exceptions.LayoutError(msg)
    if word_spacing <= -font_size // 2:
        msg = "Word spacing must be greater than (-font_size // 2)"
        raise _exceptions.LayoutError(msg)

    draw = page.draw()
    y = top_margin + line_spacing - font_size
    while y <= page.height - bottom_margin - font_size:
        x = float(left_margin)
        while True:
            if text[start] == _NEWLINE:
                start += 1
                if start == len(text):
                    return start
                break
            if x > page.width - right_margin - font_size and not is_end_char_fn(text[start]):
                break
            xy = (int(x), int(rand.gauss(y, line_spacing_sigma)))
            font = font.font_variant(size=max(int(rand.gauss(font_size, font_size_sigma)), 0))
            offset = _draw_char(draw, text[start], xy, font)
            is_half_char = is_half_char_fn(text[start])
            dx = word_spacing + offset * (0.5 if is_half_char else 1.0)
            x += rand.gauss(dx, word_spacing_sigma)
            start += 1
            if start == len(text):
                return start
        y += line_spacing
    return start


def _draw_char(draw, char: str, xy: Tuple[int, int], font) -> int:
    """Draws a single char with the parameters and white color, and returns the
    offset."""
    assert len(char) == 1
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer(object):
    """A callable object rendering the foreground that was drawn text and
    returning rendered image."""

    __slots__ = (
        "_period",
        "_backgrounds",
        "_color",
        "_perturb_x_sigmas",
        "_perturb_y_sigmas",
        "_perturb_theta_sigmas",
        "_rand",
        "_hashed_seed",
    )

    def __init__(
            self,
            backgrounds: Sequence[PIL.Image.Image],
            color: str,
            perturb_x_sigmas: Sequence[float],
            perturb_y_sigmas: Sequence[float],
            perturb_theta_sigmas: Sequence[float],
            seed: Hashable,
    ) -> None:
        assert len(backgrounds) == len(perturb_x_sigmas) == len(perturb_y_sigmas) == len(perturb_theta_sigmas)
        self._period = len(backgrounds)
        self._backgrounds = backgrounds
        self._color = color
        self._perturb_x_sigmas = perturb_x_sigmas
        self._perturb_y_sigmas = perturb_y_sigmas
        self._perturb_theta_sigmas = perturb_theta_sigmas
        self._rand = random.Random()
        self._hashed_seed = None
        if seed is not None:
            self._hashed_seed = hash(seed)

    def __call__(self, page: _page.Page) -> PIL.Image.Image:
        if self._hashed_seed is None:
            # avoid different processes sharing the same random state
            self._rand.seed()
        else:
            self._rand.seed(a=self._hashed_seed + page.num)
        return self._perturb_and_merge(page)

    def _perturb_and_merge(self, page: _page.Page) -> PIL.Image.Image:
        strokes = _extract_strokes(page.matrix, page.image.getbbox())

        x_sigma = self._perturb_x_sigmas[page.num % self._period]
        y_sigma = self._perturb_y_sigmas[page.num % self._period]
        theta_sigma = self._perturb_theta_sigmas[page.num % self._period]
        canvas = self._backgrounds[page.num % self._period].copy()
        fill = PIL.ImageColor.getcolor(self._color, canvas.mode)

        _draw_strokes(
            canvas.load(),
            canvas.size,
            strokes,
            fill,
            x_sigma=x_sigma,
            y_sigma=y_sigma,
            theta_sigma=theta_sigma,
            rand=self._rand,
        )
        return canvas


def _extract_strokes(
        bitmap,
        bbox: Tuple[int, int, int, int]
) -> _nos.NumericOrderedSet:
    left, upper, right, lower = bbox
    assert left >= 0 and upper >= 0
    # reserve 0xFFFFFFFF as _STROKE_END
    assert right <= _MAX_INT16_VALUE and lower < _MAX_INT16_VALUE
    strokes = _nos.NumericOrderedSet(
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
        bitmap,
        start: Tuple[int, int],
        strokes: _nos.NumericOrderedSet,
        bbox: Tuple[int, int, int, int],
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


def _draw_strokes(
        bitmap,
        size: Tuple[int, int],
        strokes: _nos.NumericOrderedSet,
        fill,
        x_sigma: float,
        y_sigma: float,
        theta_sigma: float,
        rand: random.Random,
) -> None:
    stroke = []
    min_x = _MAX_INT16_VALUE
    min_y = _MAX_INT16_VALUE
    max_x = 0
    max_y = 0
    for xy in strokes:
        if xy == _STROKE_END:
            center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
            _draw_stroke(
                bitmap,
                size,
                stroke,
                center=center,
                fill=fill,
                x_sigma=x_sigma,
                y_sigma=y_sigma,
                theta_sigma=theta_sigma,
                rand=rand,
            )
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
        size: Tuple[int, int],
        stroke: Sequence[Tuple[int, int]],
        center: Tuple[float, float],
        fill,
        x_sigma: float,
        y_sigma: float,
        theta_sigma: float,
        rand: random.Random,
) -> None:
    dx = rand.gauss(0, x_sigma)
    dy = rand.gauss(0, y_sigma)
    theta = rand.gauss(0, theta_sigma)
    for x, y in stroke:
        new_x, new_y = _rotate(center, x, y, theta)
        new_x += dx
        new_y += dy
        if 0 <= new_x < size[0] and 0 <= new_y < size[1]:
            bitmap[int(new_x), int(new_y)] = fill


def _rotate(
        center: Tuple[float, float],
        x: float,
        y: float,
        theta: float
) -> Tuple[float, float]:
    new_x = (x - center[0]) * math.cos(theta) + (y - center[1]) * math.sin(theta) + center[0]
    new_y = (y - center[1]) * math.cos(theta) - (x - center[0]) * math.sin(theta) + center[1]
    return new_x, new_y


def _xy(x: int, y: int) -> int:
    return (x << 16) + y


def _x_y(xy: int) -> Tuple[int, int]:
    return xy >> 16, xy & 0xFFFF
