""" The core module """
import math
import multiprocessing
import random

import PIL.Image
import PIL.ImageDraw

# Chinese, English and other end chars
_DEFAULT_END_CHARS = "，。》、？；：’”】｝、！％）" + ",.>?;:]}!%)" + "′″℃℉"

# While changing following constants, it is necessary to consider to rewrite the relevant codes.
_INTERNAL_MODE = 'L'  # The mode for internal computation
_WHITE = 255
_BLACK = 0
_AMP = 2  # Amplification for 4X SSAA.


def handwrite(text, template: dict, anti_aliasing: bool = True, worker: int = 0) -> list:
    """
    Handwrite the text with the parameters in the template
    :param text: A char iterable
    :param template: A dict containing following parameters:
        background: A Pillow's Image object
        box: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate
            NOTE: The module uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner.
            NOTE: The function do NOT guarantee the drawn texts will completely in the box.
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

        Advanced parameters:
        --------------------
        font_size_sigma: A float as the sigma of the gauss distribution of the font size
            default: font_size / 256
        line_spacing_sigma: A float as the sigma of the gauss distribution of the line spacing
            default: font_size / 256
        word_spacing_sigma: A float as the sigma of the gauss distribution of the word spacing
            default: font_size / 256
        is_half_char: A function judging whether or not a char only take up half of its original width
            The function must take a char parameter and return a boolean value.
            The feature is designed for some of Chinese punctuations that only take up the left half of their space
            (e.g. '，', '。', '！', '、').
            default: (lambda c: False)
        is_end_char: A function judging whether or not a char can NOT be in the beginning of the lines (e.g. '，', '。',
            '》', ')', ']')
            The function must take a char parameter and return a boolean value.
            default: (lambda c: c in _DEFAULT_END_CHARS)
        alpha: A tuple of two floats as the degree of the distortion in the horizontal and vertical direction in order
            Both values must be between 0.0 (inclusive) and 1.0 (inclusive).
            default: (0.1, 0.1)
    :param anti_aliasing: whether or not turn on the anti-aliasing
        It will do the anti-aliasing with using 4X SSAA. Generally, to turn off this anti-aliasing option would
        significantly reduce the overall computation.
        default: True
    :param worker: A int as the number of worker
        if worker is less than or equal to 0, the actual amount of worker would be multiprocessing.cpu_count() + worker.
        default: 0 (use all the available CPUs in the computer)
    :return: A list of drawn images with the same size and mode as background image
    """
    template = dict(template)
    font_size = template['font_size']

    if 'color' not in template:
        template['color'] = 'rgb(0, 0, 0)'
    if 'word_spacing' not in template:
        template['word_spacing'] = 0
    if 'line_spacing' not in template:
        template['line_spacing'] = font_size // 5

    if 'font_size_sigma' not in template:
        template['font_size_sigma'] = font_size / 256
    if 'line_spacing_sigma' not in template:
        template['line_spacing_sigma'] = font_size / 256
    if 'word_spacing_sigma' not in template:
        template['word_spacing_sigma'] = font_size / 256

    if 'is_half_char' not in template:
        template['is_half_char'] = lambda c: False
    if 'is_end_char' not in template:
        template['is_end_char'] = lambda c: c in _DEFAULT_END_CHARS

    if 'alpha' not in template:
        template['alpha'] = (0.1, 0.1)

    worker = worker if worker > 0 else multiprocessing.cpu_count() + worker
    return _handwrite(text, template, anti_aliasing, worker)


def _handwrite(text, template: dict, anti_aliasing: bool, worker: int) -> list:
    images = _draw_text(
        text=text,
        size=tuple(_AMP * i for i in template['background'].size) if anti_aliasing else template['background'].size,
        box=tuple(_AMP * i for i in template['box']) if anti_aliasing else template['box'],
        font=template['font'],
        font_size=template['font_size'] * _AMP if anti_aliasing else template['font_size'],
        font_size_sigma=template['font_size_sigma'] * _AMP if anti_aliasing else template['font_size_sigma'],
        line_spacing=template['line_spacing'] * _AMP if anti_aliasing else template['line_spacing'],
        line_spacing_sigma=template['line_spacing_sigma'] * _AMP if anti_aliasing else template['line_spacing_sigma'],
        word_spacing=template['word_spacing'] * _AMP if anti_aliasing else template['word_spacing'],
        word_spacing_sigma=template['word_spacing_sigma'] * _AMP if anti_aliasing else template['word_spacing_sigma'],
        is_end_char=template['is_end_char'],
        is_half_char=template['is_half_char']
    )
    render = _RenderMaker(anti_aliasing, **template)
    with multiprocessing.Pool(worker) as pool:
        images = pool.map(render, images)
    return images


def _draw_text(
        text,
        size: tuple,
        box: tuple,
        font,
        font_size: int,
        font_size_sigma: float,
        line_spacing: int,
        line_spacing_sigma: float,
        word_spacing: int,
        word_spacing_sigma: float,
        is_end_char,
        is_half_char
) -> list:
    """
    Draw the text randomly in black images with white color
    :return: a list of drawn images with L mode and given size
    NOTE: (box[3] - box[1]) must be greater than font_size.
    NOTE: (box[2] - box[0]) must be greater than font_size.
    """
    if not box[3] - box[1] > font_size:
        raise ValueError("(box[3] - box[1]) must be greater than font_size.")
    if not box[2] - box[0] > font_size:
        raise ValueError("(box[2] - box[0]) must be greater than font_size.")

    left, upper, right, lower = box
    chars = iter(text)
    images = []
    try:
        char = next(chars)
        while True:
            image = PIL.Image.new(mode=_INTERNAL_MODE, size=size, color=_BLACK)
            draw = PIL.ImageDraw.Draw(image)
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
                images.append(image)
            except StopIteration:
                images.append(image)
                raise StopIteration()
    except StopIteration:
        return images


def _draw_char(draw, char: str, xy: tuple, font) -> int:
    """ Draw a single char with the parameters and white color, and return the offset """
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _RenderMaker:
    """
    The maker of the function-like object rendering the foreground that was drawn text and returning finished image
    """

    def __init__(
            self,
            anti_aliasing: bool,
            background,
            color: str,
            font_size: int,
            alpha: tuple,
            **kwargs
    ):
        self.__anti_aliasing = anti_aliasing
        self.__background = background
        self.__color = color
        self.__font_size = font_size
        self.__alpha = alpha
        self.__random = random.Random()

    def __call__(self, image):
        self.__random.seed()
        self.__perturb(image)
        if self.__anti_aliasing:
            image = self.__downsample(image)
        return self.__merge(image)

    def __perturb(self, image) -> None:
        """
        'perturb' the image and generally make the glyphs from same chars, if any, seem different
        NOTE: self.__alpha[0] must be between 0 (inclusive) and 1 (inclusive).
        NOTE: self.__alpha[1] must be between 0 (inclusive) and 1 (inclusive).
        """
        if not 0 <= self.__alpha[0] <= 1:
            raise ValueError("alpha[0] must be between 0 (inclusive) and 1 (inclusive).")
        if not 0 <= self.__alpha[1] <= 1:
            raise ValueError("alpha[1] must be between 0 (inclusive) and 1 (inclusive).")

        wavelength = 2 * self.__font_size
        alpha_x, alpha_y = self.__alpha
        matrix = image.load()
        for i in range((image.width + wavelength) // wavelength + 1):
            x0 = self.__random.randrange(-wavelength, image.width)
            for j in range(max(0, -x0), min(wavelength, image.width - x0)):
                offset = int(alpha_x * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self.__slide_x(matrix, x0 + j, offset, image.height)
        for i in range((image.height + wavelength) // wavelength + 1):
            y0 = self.__random.randrange(-wavelength, image.height)
            for j in range(max(0, -y0), min(wavelength, image.height - y0)):
                offset = int(alpha_y * wavelength / (2 * math.pi) * (1 - math.cos(2 * math.pi * j / wavelength)))
                self.__slide_y(matrix, y0 + j, offset, image.width)

    @staticmethod
    def __slide_x(matrix, x: int, offset: int, height: int) -> None:
        """ Slide one given column """
        for i in range(height - offset):
            matrix[x, i] = matrix[x, i + offset]
        for i in range(height - offset, height):
            matrix[x, i] = _BLACK

    @staticmethod
    def __slide_y(matrix, y: int, offset: int, width: int) -> None:
        """ Slide one given row """
        for i in range(width - offset):
            matrix[i, y] = matrix[i + offset, y]
        for i in range(width - offset, width):
            matrix[i, y] = _BLACK

    @staticmethod
    def __downsample(image):
        """ Downsample the image for 4X SSAA """
        width, height = image.size[0] // _AMP, image.size[1] // _AMP
        sampled_image = PIL.Image.new(mode=_INTERNAL_MODE, size=(width, height))
        spx, px = sampled_image.load(), image.load()
        for x in range(width):
            for y in range(height):
                spx[x, y] = (px[2 * x, 2 * y] + px[2 * x + 1, 2 * y]
                             + px[2 * x, 2 * y + 1] + px[2 * x + 1, 2 * y + 1]) // (_AMP * _AMP)
        return sampled_image

    def __merge(self, image):
        """ Merge the foreground and the background image """
        res = self.__background.copy()
        draw = PIL.ImageDraw.Draw(res)
        draw.bitmap(xy=(0, 0), bitmap=image, fill=self.__color)
        return res
