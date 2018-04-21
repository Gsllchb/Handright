# API Reference
PyLf is a lightweight Python library for simulating Chinese handwriting. It introduces a great deal of randomness in the
process of Chinese handwriting to simulate the uncertainty of glyphs written by human beings. Currently, PyLf is built 
on the top of [Pillow][Pillow-homepage] library.


## pylf Module
The pylf module is the core of PyLf library.


------------------------------------------------------------------------------------------------------------------------
#### handwrite(text, template: dict, anti_aliasing: bool = True, worker: int = 0) -> list
Handwrite the `text` with the parameters in the `template`
* **text**: A `char` `iterable`
* **template**: A `dict` containing following parameters
    * **background**: A Pillow's Image object
    * **box**: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate  <br>
        The module uses a Cartesian pixel coordinate system, with `(0, 0)` in the upper left corner. The function do not
        guarantee the drawn `text` will completely in the `box`.
    * **font**: A Pillow's font object  <br>
        **NOTE**: This function do not use the `size` attribute of the font object.
    * **font_size**: A `int` as the average font size in pixel  <br>
        **NOTE**: `box[3] - box[1]` must be greater than `font_size`.  <br>
        **NOTE**: `box[2] - box[0]` must be greater than `font_size`.
    * **color**: A `str` with specific format  <br>
        The format is given as `'rgb(red, green, blue)'` where the color values are integers in the range `0`
        (inclusive) to `255` (inclusive)  <br>
        *default:* `'rgb(0, 0, 0)'`
    * **word_spacing**: A `int` as the average gap between two adjacent chars in pixel  <br>
        *default:* `0`
    * **line_spacing**: A `int` as the average gap between two adjacent lines in pixel  <br>
        *default:* `font_size // 5`
    * **font_size_sigma**: A `float` as the sigma of the gauss distribution of the font size  <br>
        *default:* `font_size / 256`
    * **word_spacing_sigma**: A `float` as the sigma of the gauss distribution of the word spacing  <br>
        *default:* `font_size / 256`
    * **line_spacing_sigma**: A `float` as the sigma of the gauss distribution of the line spacing  <br>
        *default:* `font_size / 256`
    * **is_half_char**: A `function` judging whether or not a `char` only take up half of its original `width`  <br>
        The function must take a `char` parameter and return a `bool` value. The feature is designed for some of Chinese
        punctuations that only take up the left half of their space (e.g. '，', '。', '！', '、').  <br>
        *default:* `lambda c: False`
    * **is_end_char**: A `function` judging whether or not a `char` can NOT be in the beginning of the lines (e.g. '，',
        '。', '》', ')', ']')  <br>
        The function must take a `char` parameter and return a `bool` value.  <br>
        *default:* `lambda c: c in _DEFAULT_END_CHARS`
    * **alpha**: A `tuple` of two floats as the degree of the distortion in the horizontal and vertical direction in
        order  <br>
        Both values must be between `0.0` (inclusive) and `1.0` (inclusive).  <br>
        *default:* `(0.1, 0.1)`
* **anti_aliasing**: whether or not turn on the anti-aliasing  <br>
    It will do the anti-aliasing with using 4X SSAA. Generally, to turn off this anti-aliasing option would
    significantly reduce the overall computation.  <br>
    *default:* `True`
* **worker**: A `int` as the number of worker  <br>
    if `worker` is less than or equal to `0`, the actual amount of worker would be the number of CPU in the computer
    adding `worker`.  <br>
    *default:* `0` (use all the available CPUs in the computer)
* **Return**: A `list` of drawn images with the same `size` and `mode` as background image

_since 1.0.0_


------------------------------------------------------------------------------------------------------------------------
#### handwrite2(text, template2: dict, anti_aliasing: bool = True, worker: int = 0) -> list:
The 'periodic' version of `handwrite`. See also `handwrite`.
* **text**: A `char` `iterable`
* **template2**: A `dict` containing following parameters:
    * **page_settings**: A `list` of `dict` containing the following parameters <br>
        Each of these `dict` will be applied cyclically to each page.
        * **background**: A Pillow's Image object
        * **box**: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate  <br>
            The module uses a Cartesian pixel coordinate system, with `(0, 0)` in the upper left corner. The function do
            not guarantee the drawn `text` will completely in the `box`.
        * **font_size**: A `int` as the average font size in pixel  <br>
            **NOTE**: `box[3] - box[1]` must be greater than `font_size`.  <br>
            **NOTE**: `box[2] - box[0]` must be greater than `font_size`.
        * **word_spacing**: A `int` as the average gap between two adjacent chars in pixel  <br>
            *default:* `0`
        * **line_spacing**: A `int` as the average gap between two adjacent lines in pixel  <br>
            *default:* `font_size // 5`
        * **font_size_sigma**: A `float` as the sigma of the gauss distribution of the font size  <br>
            *default:* `font_size / 256`
        * **word_spacing_sigma**: A `float` as the sigma of the gauss distribution of the word spacing  <br>
            *default:* `font_size / 256`
        * **line_spacing_sigma**: A `float` as the sigma of the gauss distribution of the line spacing  <br>
            *default:* `font_size / 256`
    * **font**: A Pillow's font object  <br>
        **NOTE**: This function do not use the `size` attribute of the font object.
    * **color**: A `str` with specific format  <br>
        The format is given as `'rgb(red, green, blue)'` where the color values are integers in the range `0`
        (inclusive) to `255` (inclusive)  <br>
        *default:* `'rgb(0, 0, 0)'`
    * **is_half_char**: A `function` judging whether or not a `char` only take up half of its original `width`  <br>
        The function must take a `char` parameter and return a `bool` value. The feature is designed for some of Chinese
        punctuations that only take up the left half of their space (e.g. '，', '。', '！', '、').  <br>
        *default:* `lambda c: False`
    * **is_end_char**: A `function` judging whether or not a `char` can NOT be in the beginning of the lines (e.g.
        '，', '。', '》', ')', ']')  <br>
        The function must take a `char` parameter and return a `bool` value.  <br>
        *default:* `lambda c: c in _DEFAULT_END_CHARS`
    * **alpha**: A `tuple` of two floats as the degree of the distortion in the horizontal and vertical direction in
        order  <br>
        Both values must be between `0.0` (inclusive) and `1.0` (inclusive).  <br>
        *default:* `(0.1, 0.1)`
* **anti_aliasing**: whether or not turn on the anti-aliasing  <br>
    It will do the anti-aliasing with using 4X SSAA. Generally, to turn off this anti-aliasing option would
    significantly reduce the overall computation.  <br>
    *default:* `True`
* **worker**: A `int` as the number of worker  <br>
    if `worker` is less than or equal to `0`, the actual amount of worker would be the number of CPU in the computer
    adding `worker`.  <br>
    *default:* `0` (use all the available CPUs in the computer)
* **Return**: A `list` of drawn images with the same `size` and `mode` as corresponding background images

_since 1.1.0_

------------------------------------------------------------------------------------------------------------------------


[Pillow-homepage]: https://python-pillow.org/
