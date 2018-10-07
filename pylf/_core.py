# coding: utf-8
"""The core module"""
import math
import multiprocessing
import random

import PIL.ImageColor

from pylf import _numeric_ordered_set as _nos
from pylf import _page

# While changing following constants, it is necessary to consider to rewrite the relevant codes.
_INTERNAL_MODE = '1'  # The mode for internal computation
_WHITE = 1
_BLACK = 0

_NEWLINE = '\n'

_UNSIGNED_INT32 = 'L'
_MAX_INT16_VALUE = 0xFFFF
_STROKE_END = 0xFFFFFFFF

_MULTIPROCESSING_THRESHOLD = 2


def handwrite(text: str, backgrounds: tuple, margins: tuple, line_spacings: tuple, font_sizes: tuple,
              word_spacings: tuple, line_spacing_sigmas: tuple, font_size_sigmas: tuple, word_spacing_sigmas: tuple,
              font, color: str, is_half_char_fn, is_end_char_fn, perturb_x_sigmas: tuple, perturb_y_sigmas: tuple,
              perturb_theta_sigmas: tuple, worker: int, seed) -> list:
    pages = _draw_text(text=text, sizes=tuple(i.size for i in backgrounds), margins=margins,
                       line_spacings=line_spacings, font_sizes=font_sizes, word_spacings=word_spacings,
                       line_spacing_sigmas=line_spacing_sigmas, font_size_sigmas=font_size_sigmas,
                       word_spacing_sigmas=word_spacing_sigmas, font=font, is_half_char_fn=is_half_char_fn,
                       is_end_char_fn=is_end_char_fn, seed=seed)

    renderer = _Renderer(backgrounds=backgrounds, color=color, perturb_x_sigmas=perturb_x_sigmas,
                         perturb_y_sigmas=perturb_y_sigmas, perturb_theta_sigmas=perturb_theta_sigmas, seed=seed)
    if len(pages) < _MULTIPROCESSING_THRESHOLD:
        return list(map(renderer, pages))
    mp_context = multiprocessing.get_context()
    with mp_context.Pool(min(worker, len(pages))) as pool:
        return pool.map(renderer, pages)


def _draw_text(text: str, sizes: tuple, margins: tuple, line_spacings: tuple, font_sizes: tuple, word_spacings: tuple,
               line_spacing_sigmas: tuple, font_size_sigmas: tuple, word_spacing_sigmas: tuple, font, is_half_char_fn,
               is_end_char_fn, seed) -> list:
    assert (len(sizes) == len(margins) == len(line_spacings) == len(font_sizes) == len(word_spacings)
            == len(line_spacing_sigmas) == len(font_size_sigmas) == len(word_spacing_sigmas))

    rand = random.Random(x=seed)
    period = len(sizes)

    iterator = iter(text)
    pages = []
    try:
        char = next(iterator)
        index = 0
        while True:
            width, height = sizes[index % period]
            margin = margins[index % period]

            line_spacing = line_spacings[index % period]
            font_size = font_sizes[index % period]
            word_spacing = word_spacings[index % period]

            line_spacing_sigma = line_spacing_sigmas[index % period]
            font_size_sigma = font_size_sigmas[index % period]
            word_spacing_sigma = word_spacing_sigmas[index % period]

            top = margin["top"]
            bottom = margin["bottom"]
            left = margin["left"]
            right = margin["right"]

            page = _page.Page(mode=_INTERNAL_MODE, size=(width, height), color=_BLACK, num=index)
            draw = page.draw

            y = top + line_spacing - font_size
            try:
                while y < height - bottom - font_size:
                    x = left
                    while True:
                        if char == _NEWLINE:
                            char = next(iterator)
                            break
                        if x >= width - right - font_size and not is_end_char_fn(char):
                            break
                        xy = (int(x), int(rand.gauss(y, line_spacing_sigma)))
                        font = font.font_variant(size=max(int(rand.gauss(font_size, font_size_sigma)), 0))
                        offset = _draw_char(draw, char, xy, font)
                        dx = word_spacing + offset * (0.5 if is_half_char_fn(char) else 1)
                        x += rand.gauss(dx, word_spacing_sigma)
                        char = next(iterator)
                    y += line_spacing
                pages.append(page)
            except StopIteration:
                pages.append(page)
                raise StopIteration()
            index += 1
    except StopIteration:
        return pages


def _draw_char(draw, char: str, xy: tuple, font) -> int:
    """Draws a single char with the parameters and white color, and returns the offset."""
    assert len(char) == 1
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer(object):
    """A function-like object rendering the foreground that was drawn text and returning rendered image."""
    __slots__ = ("_period", "_backgrounds", "_color", "_perturb_x_sigmas", "_perturb_y_sigmas", "_perturb_theta_sigmas",
                 "_rand", "_hashed_seed")

    def __init__(self, backgrounds: tuple, color: str, perturb_x_sigmas: tuple, perturb_y_sigmas: tuple,
                 perturb_theta_sigmas: tuple, seed):
        assert len(backgrounds) == len(perturb_x_sigmas) == len(perturb_y_sigmas) == len(perturb_theta_sigmas)
        self._period = len(backgrounds)
        self._backgrounds = backgrounds
        self._color = color
        self._perturb_x_sigmas = perturb_x_sigmas
        self._perturb_y_sigmas = perturb_y_sigmas
        self._perturb_theta_sigmas = perturb_theta_sigmas
        self._rand = random.Random()
        if seed is None:
            self._hashed_seed = None
        else:
            self._hashed_seed = hash(seed)

    def __call__(self, page: _page.Page):
        if self._hashed_seed is None:
            self._rand.seed()  # avoid different processes sharing the same random state
        else:
            self._rand.seed(a=self._hashed_seed + page.num)
        return self._perturb_and_merge(page)

    def _perturb_and_merge(self, page: _page.Page):
        strokes = _extract_strokes(page.matrix, page.image.getbbox())

        x_sigma = self._perturb_x_sigmas[page.num % self._period]
        y_sigma = self._perturb_y_sigmas[page.num % self._period]
        theta_sigma = self._perturb_theta_sigmas[page.num % self._period]
        canvas = self._backgrounds[page.num % self._period].copy()
        fill = PIL.ImageColor.getcolor(self._color, page.image.mode)

        _draw_strokes(canvas, strokes, fill, x_sigma=x_sigma, y_sigma=y_sigma, theta_sigma=theta_sigma, rand=self._rand)
        return canvas


def _extract_strokes(bitmap, bbox: tuple) -> _nos.NumericOrderedSet:
    left, upper, right, lower = bbox
    assert left >= 0 and upper >= 0
    assert right <= _MAX_INT16_VALUE and lower < _MAX_INT16_VALUE  # reserve 0xFFFFFFFF as _STROKE_END
    strokes = _nos.NumericOrderedSet(_UNSIGNED_INT32, privileged=_STROKE_END)
    for y in range(upper, lower):
        for x in range(left, right):
            if bitmap[x, y] and strokes.add(_xy(x, y)):
                _dfs(bitmap, (x, y), strokes, bbox)
                strokes.add(_STROKE_END)
    return strokes


def _dfs(bitmap, start: tuple, strokes: _nos.NumericOrderedSet, bbox: tuple) -> None:
    """Helper function of _extract_strokes() which uses depth first search to find the pixels of a glyph."""
    left, upper, right, lower = bbox
    stack = []
    stack.append(start)
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


def _xy(x: int, y: int) -> int:
    return (x << 16) + y


def _x_y(xy: int) -> tuple:
    return xy >> 16, xy & 0xFFFF


def _draw_strokes(canvas, strokes: _nos.NumericOrderedSet, fill, x_sigma: float, y_sigma: float,
                  theta_sigma: float, rand) -> None:
    bitmap = canvas.load()
    width, height = canvas.size
    stroke = []
    min_x, min_y = _MAX_INT16_VALUE, _MAX_INT16_VALUE
    max_x, max_y = 0, 0
    for xy in strokes:
        if xy == _STROKE_END:
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            dx = rand.gauss(0, x_sigma)
            dy = rand.gauss(0, y_sigma)
            theta = rand.gauss(0, theta_sigma)
            for x, y in stroke:
                new_x, new_y = _rotate(center_x, center_y, x, y, theta)
                new_x += dx
                new_y += dy
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                bitmap[new_x, new_y] = fill  # bitmap's index can be float

            min_x, min_y = _MAX_INT16_VALUE, _MAX_INT16_VALUE
            max_x, max_y = 0, 0
            stroke.clear()
            continue
        x, y = _x_y(xy)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        stroke.append((x, y))


def _rotate(center_x: float, center_y: float, x: float, y: float, theta: float) -> tuple:
    new_x = (x - center_x) * math.cos(theta) + (y - center_y) * math.sin(theta) + center_x
    new_y = (y - center_y) * math.cos(theta) - (x - center_x) * math.sin(theta) + center_y
    return new_x, new_y
