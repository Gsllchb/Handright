""" The core module """
import math
import multiprocessing
import random

import PIL.Image
import PIL.ImageDraw

from ._page import Page

# Chinese, English and other end chars
_DEFAULT_END_CHARS = set("，。》、？；：’”】｝、！％）" + ",.>?;:]}!%)" + "′″℃℉")

# While changing following constants, it is necessary to consider to rewrite the relevant codes.
_INTERNAL_MODE = 'L'  # The mode for internal computation
_WHITE = 255
_BLACK = 0
_AMP = 2  # Amplification for 4X SSAA.


def handwrite(text, template: dict, anti_aliasing: bool = True, worker: int = 0) -> list:
    """
    Handwrite the text with the parameters in the template.

    text: A char iterable

    template: A dict containing following parameters:
        background: A Pillow's Image object
        box: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate
            The module uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner. The function do
            not guarantee the drawn texts will completely in the box.
        font: A Pillow's font object
            NOTE: This function do not use the size attribute of the font object.
        font_size: A int as the average font size in pixel
            NOTE: (box[3] - box[1]) must be greater than font_size.
            NOTE: (box[2] - box[0]) must be greater than font_size.
        color: A str with specific format
            The format is given as 'rgb(red, green, blue)' where the color values are integers in the range 0
            (inclusive) to 255 (inclusive)
            default: 'rgb(0, 0, 0)'
        word_spacing: A int as the average gap between two adjacent chars in pixel
            default: 0
        line_spacing: A int as the average gap between two adjacent lines in pixel
            default: font_size // 5
        font_size_sigma: A float as the sigma of the gauss distribution of the font size
            default: font_size / 256
        word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing
            default: font_size / 256
        line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing
            default: font_size / 256
        is_half_char: A function judging whether or not a char only take up half of its original width
            The function must take a char parameter and return a boolean value.
            default: (lambda c: False)
        is_end_char: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，', '。',
            '》', ')', ']')
            The function must take a char parameter and return a boolean value.
            default: (lambda c: c in _DEFAULT_END_CHARS)
        alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in order
            Both values must be between 0.0 (inclusive) and 1.0 (inclusive).
            default: (0.1, 0.1)

    anti_aliasing: whether or not turn on the anti-aliasing
        default: True

    worker: A int as the number of worker
        if worker is less than or equal to 0, the actual amount of worker would be the number of CPU in the computer
        adding worker.
        default: 0 (use all the available CPUs in the computer)

    Return: A list of drawn images with the same size and mode as the background image

    since 1.0.0
    """
    page_setting = dict()
    page_setting['background'] = template['background']
    page_setting['box'] = template['box']
    page_setting['font_size'] = template['font_size']
    if 'word_spacing' in template:
        page_setting['word_spacing'] = template['word_spacing']
    if 'line_spacing' in template:
        page_setting['line_spacing'] = template['line_spacing']
    if 'font_size_sigma' in template:
        page_setting['font_size_sigma'] = template['font_size_sigma']
    if 'word_spacing_sigma' in template:
        page_setting['word_spacing_sigma'] = template['word_spacing_sigma']
    if 'line_spacing_sigma' in template:
        page_setting['line_spacing_sigma'] = template['line_spacing_sigma']

    template2 = dict()
    template2['page_settings'] = [page_setting, ]
    template2['font'] = template['font']
    if 'color' in template:
        template2['color'] = template['color']
    if 'is_half_char' in template:
        template2['is_half_char'] = template['is_half_char']
    if 'is_end_char' in template:
        template2['is_end_char'] = template['is_end_char']
    if 'alpha' in template:
        template2['alpha'] = template['alpha']

    return handwrite2(text, template2, anti_aliasing, worker)


def handwrite2(text, template2: dict, anti_aliasing: bool = True, worker: int = 0) -> list:
    """
    The 'periodic' version of handwrite. See also handwrite.

    text: A char iterable

    template2: A dict containing following parameters:
        page_settings: A list of dict containing the following parameters. Each of these dict will be applied cyclically
            to each page.
            background: A Pillow's Image object
            box: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate
                The module uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner. The function
                do not guarantee the drawn texts will completely in the box.
            font_size: A int as the average font size in pixel
                NOTE: (box[3] - box[1]) must be greater than font_size.
                NOTE: (box[2] - box[0]) must be greater than font_size.
            word_spacing: A int as the average gap between two adjacent chars in pixel
                default: 0
            line_spacing: A int as the average gap between two adjacent lines in pixel
                default: font_size // 5
            font_size_sigma: A float as the sigma of the gauss distribution of the font size
                default: font_size / 256
            word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing
                default: font_size / 256
            line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing
                default: font_size / 256
        font: A Pillow's font object
            NOTE: This function do not use the size attribute of the font object.
        color: A str with specific format
            The format is given as 'rgb(red, green, blue)' where the color values are integers in the range 0
            (inclusive) to 255 (inclusive)
            default: 'rgb(0, 0, 0)'
        is_half_char: A function judging whether or not a char only take up half of its original width
            The function must take a char parameter and return a boolean value.
            default: (lambda c: False)
        is_end_char: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，', '。',
            '》', ')', ']')
            The function must take a char parameter and return a boolean value.
            default: (lambda c: c in _DEFAULT_END_CHARS)
        alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in order
            Both values must be between 0.0 (inclusive) and 1.0 (inclusive).
            default: (0.1, 0.1)

    anti_aliasing: whether or not turn on the anti-aliasing
        default: True

    worker: A int as the number of worker
        if worker is less than or equal to 0, the actual amount of worker would be the number of CPU in the computer
        adding worker.
        default: 0 (use all the available CPUs in the computer)

    Return: A list of drawn images with the same size and mode as the corresponding background images

    since 1.1.0
    """
    page_settings = template2['page_settings']
    for page_setting in page_settings:
        font_size = page_setting['font_size']
        page_setting.setdefault('word_spacing', 0)
        page_setting.setdefault('line_spacing', font_size // 5)
        page_setting.setdefault('font_size_sigma', font_size / 256)
        page_setting.setdefault('word_spacing_sigma', font_size / 256)
        page_setting.setdefault('line_spacing_sigma', font_size / 256)

    return _handwrite(
        text,
        page_settings,
        template2['font'],
        template2.get('color', 'rgb(0, 0, 0)'),
        template2.get('is_half_char', lambda c: False),
        template2.get('is_end_char', lambda c: c in _DEFAULT_END_CHARS),
        template2.get('alpha', (0.1, 0.1)),
        anti_aliasing,
        worker if worker > 0 else multiprocessing.cpu_count() + worker
    )


def _handwrite(
        text: str,
        page_settings: list,
        font,
        color: str,
        is_half_char,
        is_end_char,
        alpha: tuple,
        anti_aliasing: bool,
        worker: int
) -> list:
    pages = _draw_text(text, page_settings, font, is_half_char, is_end_char, anti_aliasing)
    if not pages:
        return pages
    renderer = _Renderer(page_settings, color, alpha, anti_aliasing)
    with multiprocessing.Pool(min(worker, len(pages))) as pool:
        images = pool.map(renderer, pages)
    return images


def _draw_text(
        text: str,
        page_settings: list,
        font,
        is_half_char,
        is_end_char,
        anti_aliasing: bool
) -> list:
    """
    Draw the text randomly in black images with white color
    NOTE: (box[3] - box[1]) must be greater corresponding than font_size.
    NOTE: (box[2] - box[0]) must be greater corresponding than font_size.
    """
    # Avoid dead loops
    for page_setting in page_settings:
        if not page_setting['box'][3] - page_setting['box'][1] > page_setting['font_size']:
            raise ValueError("(box[3] - box[1]) must be greater than corresponding font_size.")
        if not page_setting['box'][2] - page_setting['box'][0] > page_setting['font_size']:
            raise ValueError("(box[2] - box[0]) must be greater than corresponding font_size.")

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
            page = Page(_INTERNAL_MODE, size, _BLACK, index)
            draw = page.draw
            y = upper
            try:
                while y < lower - font_size:
                    x = left
                    while True:
                        if char == '\n':
                            char = next(chars)
                            break
                        if x >= right - font_size and not is_end_char(char):
                            break
                        actual_font_size = max(int(random.gauss(font_size, font_size_sigma)), 0)
                        xy = (x, int(random.gauss(y, line_spacing_sigma)))
                        font = font.font_variant(size=actual_font_size)
                        offset = _draw_char(draw, char, xy, font)
                        x_step = word_spacing + offset * (0.5 if is_half_char(char) else 1)
                        x += int(random.gauss(x_step, word_spacing_sigma))
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
    """ A helper function of _draw_text """
    size = tuple(i * _AMP for i in page_setting['background'].size) \
        if anti_aliasing else page_setting['background'].size
    box = tuple(i * _AMP for i in page_setting['box']) if anti_aliasing else page_setting['box']
    font_size = page_setting['font_size'] * _AMP if anti_aliasing else page_setting['font_size']
    word_spacing = page_setting['word_spacing'] * _AMP if anti_aliasing else page_setting['word_spacing']
    line_spacing = page_setting['line_spacing'] * _AMP if anti_aliasing else page_setting['line_spacing']
    font_size_sigma = page_setting['font_size_sigma'] * _AMP if anti_aliasing else page_setting['font_size_sigma']
    word_spacing_sigma = page_setting['word_spacing_sigma'] * _AMP \
        if anti_aliasing else page_setting['word_spacing_sigma']
    line_spacing_sigma = page_setting['line_spacing_sigma'] * _AMP \
        if anti_aliasing else page_setting['line_spacing_sigma']
    return (size, box, font_size, word_spacing, line_spacing, font_size_sigma, line_spacing_sigma,
            word_spacing_sigma)


def _draw_char(draw, char: str, xy: tuple, font) -> int:
    """ Draw a single char with the parameters and white color, and return the offset """
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer:
    """ A function-like object rendering the foreground that was drawn text and returning rendered image """

    def __init__(
            self,
            page_settings: list,
            color: str,
            alpha: tuple,
            anti_aliasing: bool
    ):
        self._page_settings = page_settings
        self._color = color
        self._alpha = alpha
        self._anti_aliasing = anti_aliasing
        self._random = random.Random()

    def __call__(self, page: Page):
        self._random.seed()
        self._perturb(page)
        if self._anti_aliasing:
            self._downscale(page)
        return self._merge(page)

    def _perturb(self, page: Page) -> None:
        """
        'perturb' the image and generally make the glyphs from same chars, if any, seem different
        NOTE: self._alpha[0] must be between 0 (inclusive) and 1 (inclusive).
        NOTE: self._alpha[1] must be between 0 (inclusive) and 1 (inclusive).
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
            x0 = self._random.randrange(-wavelength, page.width)
            for j in range(max(0, -x0), min(wavelength, page.width - x0)):
                offset = int(alpha_x * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self._slide_x(matrix, x0 + j, offset, page.height)

        for i in range((page.height + wavelength) // wavelength + 1):
            y0 = self._random.randrange(-wavelength, page.height)
            for j in range(max(0, -y0), min(wavelength, page.height - y0)):
                offset = int(alpha_y * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self._slide_y(matrix, y0 + j, offset, page.width)

    @staticmethod
    def _slide_x(matrix, x: int, offset: int, height: int) -> None:
        """ Slide one given column """
        for i in range(height - offset):
            matrix[x, i] = matrix[x, i + offset]
        for i in range(height - offset, height):
            matrix[x, i] = _BLACK

    @staticmethod
    def _slide_y(matrix, y: int, offset: int, width: int) -> None:
        """ Slide one given row """
        for i in range(width - offset):
            matrix[i, y] = matrix[i + offset, y]
        for i in range(width - offset, width):
            matrix[i, y] = _BLACK

    @staticmethod
    def _downscale(page: Page) -> None:
        """ Downscale the image for 4X SSAA """
        page.image = page.image.resize(size=(page.width // _AMP, page.height // _AMP), resample=PIL.Image.BOX)

    def _merge(self, page: Page):
        """ Merge the foreground and the background and return merged raw image """
        res = self._page_settings[page.index % len(self._page_settings)]['background'].copy()
        draw = PIL.ImageDraw.Draw(res)
        draw.bitmap(xy=(0, 0), bitmap=page.image, fill=self._color)
        return res
