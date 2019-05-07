# coding: utf-8
import itertools
import multiprocessing
import random

import math

from pylf._exceptions import *
from pylf._numeric_ordered_set import *
from pylf._page import *
from pylf._template import *

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
        template: Union[Template, Sequence[Template]],
        worker: Optional[int] = None,
        seed: Hashable = None,
) -> List[PIL.Image.Image]:
    if isinstance(template, Template):
        templates = (template,)
    else:
        templates = template
    pages = draft(
        text=text,
        size=tuple(t.get_background().size for t in templates),
        top_margin=tuple(t.get_top_margin() for t in templates),
        bottom_margin=tuple(t.get_bottom_margin() for t in templates),
        left_margin=tuple(t.get_left_margin() for t in templates),
        right_margin=tuple(t.get_right_margin() for t in templates),
        line_spacing=tuple(t.get_line_spacing() for t in templates),
        font_size=tuple(t.get_font_size() for t in templates),
        word_spacing=tuple(t.get_word_spacing() for t in templates),
        line_spacing_sigma=tuple(t.get_line_spacing_sigma() for t in templates),
        font_size_sigma=tuple(t.get_font_size_sigma() for t in templates),
        word_spacing_sigma=tuple(t.get_word_spacing_sigma() for t in templates),
        font=tuple(t.get_font() for t in templates),
        end_chars=tuple(t.get_end_chars() for t in templates),
        seed=seed,
    )

    renderer = Renderer(
        background=tuple(t.get_background() for t in templates),
        fill=tuple(t.get_fill() for t in templates),
        perturb_x_sigma=tuple(t.get_perturb_x_sigma() for t in templates),
        perturb_y_sigma=tuple(t.get_perturb_y_sigma() for t in templates),
        perturb_theta_sigma=tuple(t.get_perturb_theta_sigma() for t in templates),
        seed=seed,
    )
    if worker == 1:
        return list(map(renderer, pages))
    mp_context = multiprocessing.get_context()
    with mp_context.Pool(worker) as pool:
        return pool.map(renderer, pages)


def draft(
        text: str,
        size: Sequence[Tuple[int, int]],
        top_margin: Sequence[int],
        bottom_margin: Sequence[int],
        left_margin: Sequence[int],
        right_margin: Sequence[int],
        line_spacing: Sequence[int],
        font_size: Sequence[int],
        word_spacing: Sequence[int],
        line_spacing_sigma: Sequence[float],
        font_size_sigma: Sequence[float],
        word_spacing_sigma: Sequence[float],
        font: Sequence,
        end_chars: Sequence[str],
        seed: Hashable = None,
) -> Iterator[Page]:
    size = itertools.cycle(size)
    top_margin = itertools.cycle(top_margin)
    bottom_margin = itertools.cycle(bottom_margin)
    left_margin = itertools.cycle(left_margin)
    right_margin = itertools.cycle(right_margin)
    line_spacing = itertools.cycle(line_spacing)
    font_size = itertools.cycle(font_size)
    word_spacing = itertools.cycle(word_spacing)
    line_spacing_sigma = itertools.cycle(line_spacing_sigma)
    font_size_sigma = itertools.cycle(font_size_sigma)
    word_spacing_sigma = itertools.cycle(word_spacing_sigma)
    font = itertools.cycle(font)
    end_chars = itertools.cycle(end_chars)

    num = itertools.count()
    rand = random.Random(x=seed)
    start = 0
    while start < len(text):
        page = Page(_INTERNAL_MODE, next(size), _BLACK, next(num))
        start = _draw_page(
            page,
            text,
            start,
            top_margin=next(top_margin),
            bottom_margin=next(bottom_margin),
            left_margin=next(left_margin),
            right_margin=next(right_margin),
            line_spacing=next(line_spacing),
            font_size=next(font_size),
            word_spacing=next(word_spacing),
            line_spacing_sigma=next(line_spacing_sigma),
            font_size_sigma=next(font_size_sigma),
            word_spacing_sigma=next(word_spacing_sigma),
            font=next(font),
            end_chars=next(end_chars),
            rand=rand,
        )
        yield page


def _draw_page(
        page: Page,
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
        end_chars: str,
        rand: random.Random,
) -> int:
    if page.height() < top_margin + line_spacing + bottom_margin:
        raise LayoutError()
    if font_size > line_spacing:
        raise LayoutError()
    if page.width() < left_margin + font_size + right_margin:
        raise LayoutError()
    if word_spacing <= -font_size // 2:
        raise LayoutError()

    draw = page.draw()
    y = top_margin + line_spacing - font_size
    while y <= page.height() - bottom_margin - font_size:
        x = float(left_margin)
        while True:
            if text[start] == _NEWLINE:
                start += 1
                if start == len(text):
                    return start
                break
            if x > page.width() - right_margin - font_size and text[start] not in end_chars:
                break
            xy = (int(x), int(rand.gauss(y, line_spacing_sigma)))
            font = font.font_variant(size=max(int(rand.gauss(font_size, font_size_sigma)), 0))
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
    if len(char) != 1:
        raise TypeError()
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class Renderer(object):
    """A callable object rendering the foreground that was drawn text and
    returning rendered image."""

    __slots__ = (
        "_period",
        "_background",
        "_fill",
        "_perturb_x_sigma",
        "_perturb_y_sigma",
        "_perturb_theta_sigma",
        "_rand",
        "_hashed_seed",
    )

    def __init__(
            self,
            background: Sequence[PIL.Image.Image],
            fill: Sequence,
            perturb_x_sigma: Sequence[float],
            perturb_y_sigma: Sequence[float],
            perturb_theta_sigma: Sequence[float],
            seed: Hashable = None,
    ) -> None:
        if not (len(background)
                == len(fill)
                == len(perturb_x_sigma)
                == len(perturb_y_sigma)
                == len(perturb_theta_sigma)):
            raise ValueError()
        self._period = len(background)
        self._background = background
        self._fill = fill
        self._perturb_x_sigma = perturb_x_sigma
        self._perturb_y_sigma = perturb_y_sigma
        self._perturb_theta_sigma = perturb_theta_sigma
        self._rand = random.Random()
        self._hashed_seed = None
        if seed is not None:
            self._hashed_seed = hash(seed)

    def __call__(self, page: Page) -> PIL.Image.Image:
        if self._hashed_seed is None:
            # avoid different processes sharing the same random state
            self._rand.seed()
        else:
            self._rand.seed(a=self._hashed_seed + page.num)
        return self._perturb_and_merge(page)

    def _perturb_and_merge(self, page: Page) -> PIL.Image.Image:
        canvas = self._background[page.num % self._period].copy()
        bbox = page.image.getbbox()
        if bbox is None:
            return canvas
        strokes = _extract_strokes(page.matrix(), bbox)
        fill = self._fill[page.num % self._period]
        x_sigma = self._perturb_x_sigma[page.num % self._period]
        y_sigma = self._perturb_y_sigma[page.num % self._period]
        theta_sigma = self._perturb_theta_sigma[page.num % self._period]
        _draw_strokes(
            canvas.load(),
            canvas.size,
            strokes,
            fill=fill,
            x_sigma=x_sigma,
            y_sigma=y_sigma,
            theta_sigma=theta_sigma,
            rand=self._rand,
        )
        return canvas


def _extract_strokes(
        bitmap,
        bbox: Tuple[int, int, int, int]
) -> NumericOrderedSet:
    left, upper, right, lower = bbox
    assert left >= 0 and upper >= 0
    # reserve 0xFFFFFFFF as _STROKE_END
    if right >= _MAX_INT16_VALUE or lower >= _MAX_INT16_VALUE:
        raise BackgroundTooLargeError()
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
        bitmap,
        start: Tuple[int, int],
        strokes: NumericOrderedSet,
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
        strokes: NumericOrderedSet,
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
