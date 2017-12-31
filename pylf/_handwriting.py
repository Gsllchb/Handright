""" The core module """
import multiprocessing
import random
import PIL.Image
import PIL.ImageDraw


# Chinese, English and other end chars
_DEFAULT_END_CHARS = "，。》、？；：’”】｝、！％）" + ",.>?;:]}!%)" + "′″℃℉"


def handwrite(text, template: dict, worker: int=0) -> list:
    """
    Simulating Chinese handwriting through introducing numerous randomness in the process.
    The module uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner as same as Pillow Module.
    Note that, the module is built for simulating Chinese handwriting instead of English(or other languages')
    handwriting. Though injecting pieces of exotic language generally may not effect the overall performance, you should
    NOT count on it has a great performance in the domain of non-Chinese handwriting.

    :param text: a char iterable

    :param template: a dict containing the settings of the template
        The dict should contain below settings:
        'background': <Image>
            An Image object used as the background
        'box': (<int>, <int>, <int>, <int>)
            A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate
            NOTE: The bounding area should be in the 'background'. In other words, it should be in (0, 0,
            background.width, background.height).
            NOTE: The function do NOT guarantee the drawn texts will completely in the 'box' due to the used randomness.
        'color': (<int>, <int>, <int>)
            The color of font in RGB. These values should be within [0, 255].
            default: (0, 0, 0)
        'font': <FreeTypeFont>
            NOTE: the size of the FreeTypeFont Object means nothing in the function.
        'font_size': <int>
            The average font size in pixel
        'line_spacing': <int>
            The average gap between two adjacent lines in pixel
        'word_spacing': <int>
            The average gap between two adjacent chars in pixel
            default: 0

        Advanced:
        'font_size_sigma': <float>
            The sigma of the gauss distribution of the font size
        'line_spacing_sigma': <float>
            The sigma of the gauss distribution of the line spacing
        'word_spacing_sigma': <float>
            The sigma of the gauss distribution of the word spacing
        'is_half_char': <callable>
            A function judges whether or not a char only take up half of its original width
            The function must take a char parameter and return a boolean value.
            The feature is designed for some of Chinese punctuations that only take up the left half of their
            space (e.g. '，', '。').
            default: (lambda c: False)
        'is_end_char': <callable>
            A function judges whether or not a char can NOT be in the beginning of the lines (e.g. '，' , '。', '》')
            The function must take a char parameter and return a boolean value.
            default: (lambda c: c in _DEFAULT_END_CHARS)
        'alpha_x': <float>
            A float that controls the degree of the distortion in the horizontal direction
            its value must be between 0(inclusive) and 1(inclusive).
            default: 0.1
        'alpha_y': <float>
            A float that controls the degree of the distortion in the vertical direction
            its value must be between 0(inclusive) and 1(inclusive).
            default: 0.1

    :param worker: the number of worker
        if worker is less than or equal to 0, the actual amount of worker would be multiprocessing.cpu_count() + worker.
        default: 0 (use all the available CPU in the computer)

    :return: a list of drawn images
    """
    template = dict(template)
    if 'color' not in template:
        template['color'] = (0, 0, 0)
    if 'word_spacing' not in template:
        template['word_spacing'] = 0
    if 'is_half_char' not in template:
        template['is_half_char'] = lambda c: False
    if 'is_end_char' not in template:
        template['is_end_char'] = lambda c: c in _DEFAULT_END_CHARS
    if 'alpha_x' not in template:
        template['alpha_x'] = 0.1
    if 'alpha_y' not in template:
        template['alpha_y'] = 0.1
    worker = worker if worker > 0 else multiprocessing.cpu_count() + worker
    return _handwrite(text, template, worker)


def _handwrite(text, template, worker):
    images = _draw_text(text, size=template['background'].size, **template)
    if not images:
        return images
    render = _RenderMaker(**template)
    with multiprocessing.Pool(min(worker, len(images))) as pool:
        images = pool.map(render, images)
    return images


def _draw_text(
        text,
        size,
        box,
        color,
        font,
        font_size,
        font_size_sigma,
        line_spacing,
        line_spacing_sigma,
        word_spacing,
        word_spacing_sigma,
        is_end_char,
        is_half_char,
        **kwargs
):
    """
    Draw the text randomly in blank images
    :return: a list of drawn images
    :raise: ValueError
    """
    if not box[3] - box[1] > font_size:
        raise ValueError('(box[3] - box[1]) must be greater than font_size.')
    if not box[2] - box[0] > font_size:
        raise ValueError('(box[2] - box[0]) must be greater than font_size.')

    left, upper, right, lower = box
    chars = iter(text)
    images = []
    try:
        char = next(chars)
        while True:
            # FIXME: the used image mode-'RGBA' actually is unnecessary. Change it to grey level image.
            image = PIL.Image.new('RGBA', size, color=(0, 0, 0, 0))
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
                        actual_font_size = int(random.gauss(font_size, font_size_sigma))
                        xy = x, int(random.gauss(y, line_spacing_sigma))
                        font = font.font_variant(size=actual_font_size)
                        draw.text(xy, char, fill=(*color, 255), font=font)
                        font_width = font.getsize(char)[0]
                        x_step = word_spacing + font_width * (1 / 2 if is_half_char(char) else 1)
                        x += int(random.gauss(x_step, word_spacing_sigma))
                        char = next(chars)
                    y += line_spacing + font_size
                images.append(image)
            except StopIteration:
                images.append(image)
                raise StopIteration()
    except StopIteration:
        return images


class _RenderMaker:
    """
    The maker of the function-like object rendering the foreground that was drawn text and returning finished image
    """

    def __init__(
            self,
            background,
            font_size,
            alpha_x,
            alpha_y,
            **kwargs
    ):
        self.__background = background
        self.__font_size = font_size
        self.__alpha_x = alpha_x
        self.__alpha_y = alpha_y
        self.__random = random.Random()

    def __call__(self, image):
        self.__random.seed()
        self.__perturb(image)
        return self.__merge(image)

    def __perturb(self, image) -> None:
        """
        'perturb' the image and generally make the glyphs from same chars, if any, seem different
        :raise: ValueError
        """
        from math import cos, pi
        if not 0 <= self.__alpha_x <= 1:
            raise ValueError("alpha_x must be between 0 (inclusive) and 1 (inclusive).")
        if not 0 <= self.__alpha_y <= 1:
            raise ValueError("alpha_y must be between 0 (inclusive) and 1 (inclusive).")

        wavelength = 2 * self.__font_size
        matrix = image.load()
        for i in range(image.width // wavelength + 1):
            x0 = self.__random.randrange(0, image.width)
            for j in range(min(wavelength, image.width - x0)):
                offset = self.__alpha_x * wavelength / (2 * pi) * (1 - cos(2 * pi * j / wavelength))
                self.__slide_x(matrix, x0 + j, offset, image.height)
        for i in range(image.height // wavelength + 1):
            y0 = self.__random.randrange(0, image.height)
            for j in range(min(wavelength, image.height - y0)):
                offset = self.__alpha_y * wavelength / (2 * pi) * (1 - cos(2 * pi * j / wavelength))
                self.__slide_y(matrix, y0 + j, offset, image.width)

    @staticmethod
    def __slide_x(matrix, x: int, offset: float, height: int) -> None:
        """
        The helper function of __perturb()
        Slide one given column without producing jaggies
        :param offset: a float value between 0(inclusive) and 1(inclusive)
        """
        for i in range(height - 1):
            matrix[x, i] = (1 - offset) * matrix[x, i] + offset * matrix[x, i + 1]
        matrix[x, height - 1] = (1 - offset) * matrix[x, height - 1]

    @staticmethod
    def __slide_y(matrix, y: int, offset: float, width: int) -> None:
        """
        The helper function of __perturb()
        Slide one given row without producing jaggies
        :param offset: a float value between 0(inclusive) and 1(inclusive)
        """
        for i in range(width - 1):
            matrix[i, y] = (1 - offset) * matrix[i, y] + offset * matrix[i + 1, y]
        matrix[width - 1, y] = (1 - offset) * matrix[width - 1, y]

    def __merge(self, image):
        """ Merge the foreground and the background image """
        # FIXME: rewrite the code for the change of _draw_text()
        background = self.__background.copy()
        background.paste(image, mask=image)
        return background
