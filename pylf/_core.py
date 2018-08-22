# coding: utf-8
"""The core module"""
import multiprocessing
import random

from pylf import _page
from pylf import _numeric_ordered_set as _nos

# While changing following constants, it is necessary to consider to rewrite the relevant codes.
_INTERNAL_MODE = '1'  # The mode for internal computation
_WHITE = 1
_BLACK = 0

_NEWLINE = '\n'


def handwrite(text: str, backgrounds: tuple, margins: tuple, line_spacings: tuple, font_sizes: tuple,
              word_spacings: tuple, line_spacing_sigmas: tuple, font_size_sigmas: tuple, word_spacing_sigmas: tuple,
              font, color: str, is_half_char_fn, is_end_char_fn, perturb_x_sigmas: tuple, perturb_y_sigmas: tuple,
              worker: int, seed) -> list:
    pages = _draw_text(text=text, sizes=tuple(i.size for i in backgrounds), margins=margins,
                       line_spacings=line_spacings, font_sizes=font_sizes, word_spacings=word_spacings,
                       line_spacing_sigmas=line_spacing_sigmas, font_size_sigmas=font_size_sigmas,
                       word_spacing_sigmas=word_spacing_sigmas, font=font, is_half_char_fn=is_half_char_fn,
                       is_end_char_fn=is_end_char_fn, seed=seed)
    if not pages:
        return pages

    renderer = _Renderer(backgrounds, color, perturb_x_sigmas, perturb_y_sigmas, seed)
    with multiprocessing.Pool(min(worker, len(pages))) as pool:
        images = pool.map(renderer, pages)

    return images


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

            top, bottom, left, right = margin["top"], margin["bottom"], margin["left"], margin["right"]

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

    def __init__(self, backgrounds: tuple, color: str, perturb_x_sigmas: tuple, perturb_y_sigmas: tuple, seed):
        assert len(backgrounds) == len(perturb_x_sigmas) == len(perturb_y_sigmas)
        self._period = len(backgrounds)
        self._backgrounds = backgrounds
        self._color = color
        self._perturb_x_sigmas = perturb_x_sigmas
        self._perturb_y_sigmas = perturb_y_sigmas
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
        strokes = self._extract_strokes(page.image)
        x_sigma = self._perturb_x_sigmas[page.num % self._period]
        y_sigma = self._perturb_y_sigmas[page.num % self._period]
        canvas = self._backgrounds[page.num % self._period].copy()
        self._draw_strokes(canvas, strokes, x_sigma, y_sigma)
        return canvas

    @staticmethod
    def _extract_strokes(bitmap) -> _nos.NumericOrderedSet:
        # TODO
        pass

    @staticmethod
    def _draw_strokes(canvas, strokes: _nos.NumericOrderedSet, x_sigma: float, y_sigma: float) -> None:
        # TODO
        pass
