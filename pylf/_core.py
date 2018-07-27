# -*- coding: utf-8 -*-
"""The core module"""
import math
import multiprocessing
import random

from PIL import Image as image
from PIL import ImageDraw as image_draw

from pylf import _page

# While changing following constants, it is necessary to consider to rewrite the relevant codes.
_INTERNAL_MODE = 'L'  # The mode for internal computation
_WHITE = 255
_BLACK = 0
_AMP = 2  # Amplification for 4X SSAA.

_NEWLINE = '\n'


def handwrite(text: str, page_settings: tuple, font, color: str, is_half_char, is_end_char, alpha: tuple,
              anti_aliasing: bool, worker: int, seed) -> list:
    """Do the real stuffs for handwriting simulating."""
    pages = _draw_text(text, page_settings, font, is_half_char, is_end_char, anti_aliasing, seed)
    if not pages:
        return pages
    renderer = _Renderer(page_settings, color, alpha, anti_aliasing, seed)
    with multiprocessing.Pool(min(worker, len(pages))) as pool:
        images = pool.map(renderer, pages)
    return images


def _draw_text(text: str, page_settings: tuple, font, is_half_char, is_end_char, anti_aliasing: bool, seed) -> list:
    """Draws the text randomly in black images with white color. Note that (box[3] - box[1]) and (box[2] - box[0]) both
    must be greater than corresponding font_size.
    """
    # Avoid dead loops
    for page_setting in page_settings:
        if not page_setting['box'][3] - page_setting['box'][1] > page_setting['font_size']:
            raise ValueError("(box[3] - box[1]) must be greater than corresponding font_size.")
        if not page_setting['box'][2] - page_setting['box'][0] > page_setting['font_size']:
            raise ValueError("(box[2] - box[0]) must be greater than corresponding font_size.")

    rand = random.Random(x=seed)
    length = len(page_settings)
    chars = iter(text)
    pages = []
    try:
        char = next(chars)
        index = 0
        while True:
            (size, box, font_size, word_spacing, line_spacing, font_size_sigma, line_spacing_sigma,
             word_spacing_sigma) = _parse_page_setting(page_settings[index % length], anti_aliasing)
            left, upper, right, lower = box
            page = _page.Page(_INTERNAL_MODE, size, _BLACK, index)
            draw = page.draw
            y = upper
            try:
                while y < lower - font_size:
                    x = left
                    while True:
                        if char == _NEWLINE:
                            char = next(chars)
                            break
                        if x >= right - font_size and not is_end_char(char):
                            break
                        actual_font_size = max(int(rand.gauss(font_size, font_size_sigma)), 0)
                        xy = (x, int(rand.gauss(y, line_spacing_sigma)))
                        font = font.font_variant(size=actual_font_size)
                        offset = _draw_char(draw, char, xy, font)
                        x_step = word_spacing + offset * (0.5 if is_half_char(char) else 1)
                        x += int(rand.gauss(x_step, word_spacing_sigma))
                        char = next(chars)
                    y += line_spacing + font_size
                pages.append(page)
            except StopIteration:
                pages.append(page)
                raise StopIteration()
            index += 1
    except StopIteration:
        return pages


def _parse_page_setting(page_setting: dict, anti_aliasing: bool) -> tuple:
    """A helper function of _draw_text"""
    size = (tuple(i * _AMP for i in page_setting['background'].size)
            if anti_aliasing else page_setting['background'].size)
    box = tuple(i * _AMP for i in page_setting['box']) if anti_aliasing else page_setting['box']
    font_size = page_setting['font_size'] * _AMP if anti_aliasing else page_setting['font_size']
    word_spacing = page_setting['word_spacing'] * _AMP if anti_aliasing else page_setting['word_spacing']
    line_spacing = page_setting['line_spacing'] * _AMP if anti_aliasing else page_setting['line_spacing']
    font_size_sigma = page_setting['font_size_sigma'] * _AMP if anti_aliasing else page_setting['font_size_sigma']
    word_spacing_sigma = (page_setting['word_spacing_sigma'] * _AMP
                          if anti_aliasing else page_setting['word_spacing_sigma'])
    line_spacing_sigma = (page_setting['line_spacing_sigma'] * _AMP
                          if anti_aliasing else page_setting['line_spacing_sigma'])
    return size, box, font_size, word_spacing, line_spacing, font_size_sigma, line_spacing_sigma, word_spacing_sigma


def _draw_char(draw, char: str, xy: tuple, font) -> int:
    """Draws a single char with the parameters and white color, and returns the offset."""
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer(object):
    """A function-like object rendering the foreground that was drawn text and returning rendered image."""

    def __init__(self, page_settings: tuple, color: str, alpha: tuple, anti_aliasing: bool, seed):
        self._page_settings = page_settings
        self._color = color
        self._alpha = alpha
        self._anti_aliasing = anti_aliasing
        self._rand = random.Random()
        if seed is None:
            self._hashed_seed = None
        else:
            self._hashed_seed = hash(seed)

    def __call__(self, page: _page.Page):
        if self._hashed_seed is None:
            self._rand.seed()  # avoid different processes sharing the same random state
        else:
            self._rand.seed(a=self._hashed_seed + page.index)
        self._perturb(page)
        if self._anti_aliasing:
            self._downscale(page)
        return self._merge(page)

    def _perturb(self, page: _page.Page) -> None:
        """'perturbs' the image and generally makes the glyphs from same chars, if any, seems different. Note that
        self._alpha[0] and self._alpha[1] both must be between 0 (inclusive) and 1 (inclusive).
        """
        if not 0 <= self._alpha[0] <= 1:
            raise ValueError("alpha[0] must be between 0 (inclusive) and 1 (inclusive).")
        if not 0 <= self._alpha[1] <= 1:
            raise ValueError("alpha[1] must be between 0 (inclusive) and 1 (inclusive).")

        wavelength = 2 * self._page_settings[page.index % len(self._page_settings)]['font_size']
        if wavelength == 0:
            return
        alpha_x, alpha_y = self._alpha
        matrix = page.matrix

        for i in range((page.width + wavelength) // wavelength + 1):
            x0 = self._rand.randrange(-wavelength, page.width)
            for j in range(max(0, -x0), min(wavelength, page.width - x0)):
                offset = int(alpha_x * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self._slide_x(matrix, x0 + j, offset, page.height)

        for i in range((page.height + wavelength) // wavelength + 1):
            y0 = self._rand.randrange(-wavelength, page.height)
            for j in range(max(0, -y0), min(wavelength, page.height - y0)):
                offset = int(alpha_y * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self._slide_y(matrix, y0 + j, offset, page.width)

    @staticmethod
    def _slide_x(matrix, x: int, offset: int, height: int) -> None:
        """Slides one given column."""
        for i in range(height - offset):
            matrix[x, i] = matrix[x, i + offset]
        for i in range(height - offset, height):
            matrix[x, i] = _BLACK

    @staticmethod
    def _slide_y(matrix, y: int, offset: int, width: int) -> None:
        """Slides one given row."""
        for i in range(width - offset):
            matrix[i, y] = matrix[i + offset, y]
        for i in range(width - offset, width):
            matrix[i, y] = _BLACK

    @staticmethod
    def _downscale(page: _page.Page) -> None:
        """Downscales the image for 4X SSAA."""
        page.image = page.image.resize(size=(page.width // _AMP, page.height // _AMP), resample=image.BOX)

    def _merge(self, page: _page.Page):
        """Merges the foreground and the background and returns merged raw image."""
        res = self._page_settings[page.index % len(self._page_settings)]['background'].copy()
        draw = image_draw.Draw(res)
        draw.bitmap(xy=(0, 0), bitmap=page.image, fill=self._color)
        return res
