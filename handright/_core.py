# coding: utf-8
import itertools
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


def _check_template(page, tpl) -> None:
    if page.height() < (tpl.get_top_margin() + tpl.get_line_spacing()
                        + tpl.get_bottom_margin()):
        msg = "for (height < top_margin + line_spacing + bottom_margin)"
        raise LayoutError(msg)
    if tpl.get_font().size > tpl.get_line_spacing():
        msg = "for (font.size > line_spacing)"
        raise LayoutError(msg)
    if page.width() < (tpl.get_left_margin() + tpl.get_font().size
                       + tpl.get_right_margin()):
        msg = "for (width < left_margin + font.size + right_margin)"
        raise LayoutError(msg)
    if tpl.get_word_spacing() <= -tpl.get_font().size // 2:
        msg = "for (word_spacing <= -font.size // 2)"
        raise LayoutError(msg)


def _draw_page(
        page, text, start: int, tpl: Template, rand: random.Random
) -> int:
    _check_template(page, tpl)

    width = page.width()
    height = page.height()
    top_margin = tpl.get_top_margin()
    bottom_margin = tpl.get_bottom_margin()
    left_margin = tpl.get_left_margin()
    right_margin = tpl.get_right_margin()
    line_spacing = tpl.get_line_spacing()
    font_size = tpl.get_font().size
    end_chars = tpl.get_end_chars()

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
            if Feature.GRID_LAYOUT in tpl.get_features():
                x = _grid_layout(draw, x, y, text[start], tpl, rand)
            else:
                x = _flow_layout(draw, x, y, text[start], tpl, rand)
            start += 1
            if start == len(text):
                return start
        y += line_spacing
    return start


def _flow_layout(
        draw, x, y, char, tpl: Template, rand: random.Random
) -> float:
    xy = (round(x), round(gauss(rand, y, tpl.get_line_spacing_sigma())))
    font = _get_font(tpl, rand)
    offset = _draw_char(draw, char, xy, font)
    x += gauss(
        rand,
        tpl.get_word_spacing() + offset,
        tpl.get_word_spacing_sigma()
    )
    return x


def _grid_layout(
        draw, x, y, char, tpl: Template, rand: random.Random
) -> float:
    xy = (round(gauss(rand, x, tpl.get_word_spacing_sigma())),
          round(gauss(rand, y, tpl.get_line_spacing_sigma())))
    font = _get_font(tpl, rand)
    _ = _draw_char(draw, char, xy, font)
    x += tpl.get_word_spacing() + tpl.get_font().size
    return x


def _get_font(tpl: Template, rand: random.Random):
    font = tpl.get_font()
    actual_font_size = max(round(
        gauss(rand, font.size, tpl.get_font_size_sigma())
    ), 0)
    if actual_font_size != font.size:
        return font.font_variant(size=actual_font_size)
    return font


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


def _draw_strokes(bitmap, strokes, tpl, rand) -> None:
    stroke = []
    min_x = _MAX_INT16_VALUE
    min_y = _MAX_INT16_VALUE
    max_x = 0
    max_y = 0
    for xy in strokes:
        if xy == _STROKE_END:
            center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
            _draw_stroke(bitmap, stroke, tpl, center, rand)
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
        tpl: Template,
        center: Tuple[float, float],
        rand
) -> None:
    dx = gauss(rand, 0, tpl.get_perturb_x_sigma())
    dy = gauss(rand, 0, tpl.get_perturb_y_sigma())
    theta = gauss(rand, 0, tpl.get_perturb_theta_sigma())
    for x, y in stroke:
        new_x, new_y = _rotate(center, x, y, theta)
        new_x = round(new_x + dx)
        new_y = round(new_y + dy)
        width, height = tpl.get_size()
        if 0 <= new_x < width and 0 <= new_y < height:
            bitmap[new_x, new_y] = tpl.get_fill()


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
