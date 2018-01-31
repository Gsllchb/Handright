# API Reference
*PyLf* is a lightweight *Python* library for simulating Chinese handwriting. It introduces a great deal of randomness in
the process of Chinese handwriting to simulate the uncertainty of glyphs written by human beings. Currently, *PyLf* is
built on the top of *Pillow* module.

## Functions

### pylf.handwrite(text, template: dict, anti_aliasing: bool = True, worker: int = 0) -> list
Handwrite the `text` with the parameters in the `template`
* **Parameter**:
    * **text**: A `char` `iterable`
    * **template**: A `dict` containing following parameters:
        * **background**: A Pillow's Image object
        * **box**: A bounding box as a 4-tuple defining the left, upper, right, and lower pixel coordinate  <br>
            The module uses a Cartesian pixel coordinate system, with `(0, 0)` in the upper left corner. The function do
            not guarantee the drawn `text` will completely in the `box`.
        * **font**: A Pillow's font object  <br>
            **NOTE**: This function do not use the `size` attribute of the font object.
        * **font_size**: A `int` as the average font size in pixel  <br>
            **NOTE**: `box[3] - box[1]` must be greater than `font_size`.  <br>
            **NOTE**: `box[2] - box[0]` must be greater than `font_size`.
        * **color**: A `str` with specific format  <br>
            The format is given as `'rgb(red, green, blue)'` where the color values are integers in the range `0` 
            (inclusive) to `255` (inclusive)  <br>
            Default: `'rgb(0, 0, 0)'`
        * **word_spacing**: A `int` as the average gap between two adjacent chars in pixel  <br>
            Default: `0`
        * **line_spacing**: A `int` as the average gap between two adjacent lines in pixel  <br>
            Default: `font_size // 5`
        * **font_size_sigma**: A `float` as the sigma of the gauss distribution of the font size  <br>
            Default: `font_size / 256`
        * **line_spacing_sigma**: A `float` as the sigma of the gauss distribution of the line spacing  <br>
            Default: `font_size / 256`
        * **word_spacing_sigma**: A `float` as the sigma of the gauss distribution of the word spacing  <br>
            Default: `font_size / 256`
        * **is_half_char**: A `function` judging whether or not a `char` only take up half of its original `width`  <br>
            The function must take a `char` parameter and return a `bool` value.  <br>
            The feature is designed for some of Chinese punctuations that only take up the left half of their space 
            (e.g. '，', '。', '！', '、').  <br>
            Default: `lambda c: False`
        * **is_end_char**: A `function` judging whether or not a `char` can NOT be in the beginning of the lines (e.g.
            '，', '。', '》', ')', ']')  <br>
            The function must take a `char` parameter and return a `bool` value.  <br>
            Default: `lambda c: c in _DEFAULT_END_CHARS`
        * **alpha**: A `tuple` of two floats as the degree of the distortion in the horizontal and vertical direction in 
            order Both values must be between `0.0` (inclusive) and `1.0` (inclusive).  <br>
            Default: `(0.1, 0.1)`
    * **anti_aliasing**: whether or not turn on the anti-aliasing  <br>
        It will do the anti-aliasing with using 4X SSAA. Generally, to turn off this anti-aliasing option would
        significantly reduce the overall computation.  <br>
        Default: `True`
    * **worker**: A `int` as the number of worker  <br>
        if `worker` is less than or equal to `0`, the actual amount of worker would be the number of CPU in the computer
        adding `worker`.
        Default: `0` (use all the available CPUs in the computer)
* **Return**: A `list` of drawn images with the same `size` and `mode` as background image