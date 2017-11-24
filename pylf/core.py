"""
The core module.
"""
import multiprocess
import random
import PIL.Image
import PIL.ImageDraw


def handwrite(text, template: dict, anti_aliasing: bool=True, worker: int=0) -> list:
    """
    Simulating Chinese handwriting through introducing numerous randomness in the process.
    The module uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner as same as Pillow Module.
    Note that, the module is built for simulating Chinese handwriting instead of English(or other languages)
    handwriting. Though injecting pieces of exotic language generally may not effect the overall performance, you should
    NOT count on it has a great performance in the domain of non-Chinese handwriting.

    :param text: a char sequence.

    :param template: a dict containing the settings of the template.
        The dict should contain below settings:
        'background': <Image>
            An Image object used as the background.
        'box': (<int>, <int>, <int>, <int>)
            A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate.
            NOTE: The bounding area should be in the 'background'. In other words, it should be in (0, 0,
            background.width, background.height).
            NOTE: The function DO NOT guarantee the drawn texts would absolutely in the 'box' due to the randomness used.
        'color': (<int>, <int>, <int>)
            The color of font in RGB. These values should be within [0, 255].
        'font': <FreeTypeFont>
            A FreeTypeFont object. Note that the size of the FreeTypeFont Object means nothing to the function.
        'font_size': <int>
        'font_size_sigma': <float>
            The sigma of the gauss distribution of font size.
        'line_spacing': <int>
        'line_spacing_sigma': <float>
            The sigma of the gauss distribution of line spacing.
        'word_spacing': <int>
        'word_spacing_sigma': <float>
            The sigma of the gauss distribution of word spacing.
        'is_half_char': <callable>
            A function judges whether or not a char only take up half of the horizontal space of other char (e.g. 'a',
            '?', '2').
            The function should take a char parameter and return a boolean value.
        'is_end_char': <callable>,
            A function judges whether or not a char can NOT be in the beginning of the lines (e.g. ',' , '!').

        Advanced:
        If you do NOT fully understand the algorithm, please leave these value default.
        'x_amplitude': <float>
            default: 0.06 * font_size.
        'y_amplitude': <float>
            default: 0.06 * font_size.
        'x_wavelength': <float>
            default: 2 * font_size.
        'y_wavelength': <float>
            default: 2 * font_size.
        'x_lambd': <float>
            default: 1 / font_size.
        'y_lambd': <float>
            default: 1 / font_size.

    :param anti_aliasing: whether or not turn on the anti-aliasing.
        It will do the anti-aliasing with using 4X SSAA. Generally, to turn off this anti-aliasing option would
        significantly reduce the computational cost.
        default True.

    :param worker: the number of worker.
        if worker <= 0, the actual amount of worker would be multiprocessing.cpu_count() + worker.
        default 0 (use all available CPU in the computer).

    :return: a list of drawn images.
    """
    template = dict(template)
    font_size = template['font_size']
    if 'x_amplitude' not in template:
        template['x_amplitude'] = 0.06 * font_size
    if 'y_amplitude' not in template:
        template['y_amplitude'] = 0.06 * font_size
    if 'x_wavelength' not in template:
        template['x_wavelength'] = 2 * font_size
    if 'y_wavelength' not in template:
        template['y_wavelength'] = 2 * font_size
    if 'x_lambd' not in template:
        template['x_lambd'] = 1 / font_size
    if 'y_lambd' not in template:
        template['y_lambd'] = 1 / font_size
    worker = worker if worker > 0 else multiprocess.cpu_count() + worker
    return _handwrite(text, template, anti_aliasing, worker)


def _handwrite(text, template, anti_aliasing, worker):
    outlines = _sketch(anti_aliasing, text, **template)
    # Because the FreeTypeFont object is NOT pickle-able, we can not accelerate _draw_chars() with multiprocess.
    images = map(_draw_chars_factory(anti_aliasing, **template), outlines)
    with multiprocess.Pool(worker) as p:
        images = p.map(_perturb_factory(anti_aliasing, **template), images)
        images = p.map(_downsample_factory(anti_aliasing, **template), images)
        images = p.map(_merge_factory(anti_aliasing, **template), images)
    return images


def _sketch(anti_aliasing, text, box, font_size, font_size_sigma, line_spacing, line_spacing_sigma,
            word_spacing, word_spacing_sigma, is_end_char, is_half_char, **kwargs):
    """
    Draw the outlines for later parallel computation.
    :return: outlines
        outlines is a list of lists containing tuples that respectively contain (x, y), char, actual_font_size in order.
    """
    if anti_aliasing:
        box = tuple(2 * i for i in box)
        font_size *= 2
        font_size_sigma *= 2
        line_spacing *= 2
        line_spacing_sigma *= 2
        word_spacing *= 2
        word_spacing_sigma *= 2

    length = len(text)
    outlines = []
    i = 0
    while i != length:
        outline = []
        y = box[1]
        while y < box[3] - font_size and i != length:
            x = box[0]
            while i != length:
                char = text[i]
                # DO NOT change the order of these if statements.
                if char == '\n':
                    i += 1
                    break
                if x >= box[2] - font_size and not is_end_char(char):
                    break
                actual_font_size = int(random.gauss(font_size, font_size_sigma))
                outline.append(((x, int(random.gauss(y, line_spacing_sigma))), char, actual_font_size))
                x_step = word_spacing + actual_font_size * (1 / 2 if is_half_char(char) else 1)
                x += int(random.gauss(x_step, word_spacing_sigma))
                i += 1
            y += line_spacing
        outlines.append(outline)
    return outlines


def _draw_chars_factory(anti_aliasing, background, font, color, **kwargs):
    """
    The factory of the function that draw chars on the foreground depending on the 'outline' provided by _sketch().
    """
    size = tuple(2 * i for i in background.size) if anti_aliasing else background.size

    def _draw_chars(outline):
        image = PIL.Image.new('RGBA', size, color=(0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        for xy, char, font_size in outline:
            draw.text(xy, char, fill=(*color, 255), font=font.font_variant(size=font_size))
        return image
    return _draw_chars


def _perturb_factory(anti_aliasing, x_amplitude, y_amplitude, x_wavelength, y_wavelength, x_lambd, y_lambd, **kwargs):
    """
    The factory of the function that 'perturb' the foreground image.
    """
    if anti_aliasing:
        x_amplitude *= 2
        y_amplitude *= 2
        x_wavelength *= 2
        y_wavelength *= 2
        x_lambd /= 2
        y_lambd /= 2

    def _perturb(image):
        from math import sin, pi
        height = image.height
        width = image.width
        px = image.load()
        start = 0
        for x in range(width):
            if x >= start + x_wavelength:
                start = x + random.expovariate(x_lambd)
            if x <= start:
                continue
            offset = int(x_amplitude * (sin(2 * pi *(x - start) / x_wavelength - pi / 2) + 1))
            for y in range(height - offset):
                px[x, y] = px[x, y + offset]
            for y in range(height - offset, height):
                px[x, y] = (0, 0, 0, 0)
        start = 0
        for y in range(height):
            if y >= start + y_wavelength:
                start = y + random.expovariate(y_lambd)
            if y <= start:
                continue
            offset = int(y_amplitude * (sin(2 * pi *(y - start) / y_wavelength - pi / 2) + 1))
            for x in range(width - offset):
                px[x, y] = px[x + offset, y]
            for x in range(width - offset, width):
                px[x, y] = (0, 0, 0, 0)
        return image
    return _perturb


def _downsample_factory(anti_aliasing, **kwargs):
    """
    The factory of the function downsampling for 4X SSAA.
    """
    if anti_aliasing:
        def _downsample(image):
            width, height = image.size[0] // 2, image.size[1] // 2
            sampled_image = PIL.Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
            spx, px = sampled_image.load(), image.load()
            for x in range(width):
                for y in range(height):
                    temp = zip(px[2 * x, 2 * y], px[2 * x + 1, 2 * y], px[2 * x, 2 * y + 1], px[2 * x + 1, 2 * y + 1])
                    spx[x, y] = tuple(sum(i) // 4 for i in temp)
            return sampled_image
        return _downsample
    else:
        return lambda image: image


def _merge_factory(anti_aliasing, background, **kwargs):
    """
    The factory of the function that merge the image with the background.
    """
    def _merge(image):
        bg = background.copy()
        bg.paste(image, mask=image)
        return bg
    return _merge
