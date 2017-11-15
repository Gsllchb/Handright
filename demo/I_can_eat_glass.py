from PIL import Image, ImageFont
from pylf import handwrite
template = {
    'background': Image.open("./pictures/树信笺纸.jpg"),
    'box': (50, 500, 800 - 80, 800 - 50),
    'color': (0, 0, 0),
    'font': ImageFont.truetype("./fonts/HYYiNingLiJ.ttf"),
    'font_size': 60,
    'font_size_sigma': 4,
    'line_spacing': 50,
    'line_spacing_sigma': 1,
    'word_spacing': 30,
    'word_spacing_sigma': 5,
    'is_half_char': lambda c: c.isalpha() or c.isdigit() or c in (',', '.'),
    'is_end_char': lambda c: c in ('!', '.', '?')
}
text = "我能吞下玻璃而不伤身体"
images = handwrite(text, template)
images[0].crop((0, 450, 800, 800-200)).save("./out/I_can_eat_glass.jpg")
