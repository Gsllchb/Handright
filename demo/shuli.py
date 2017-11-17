from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support


def main():
    template = {
        'background': Image.open("./pictures/树信笺纸.jpg"),
        'box': (50, 100, 800-50, 800-100),
        'color': (0, 0, 0),
        'font': ImageFont.truetype("./fonts/HYYiNingLiJ.ttf"),
        'font_size': 45,
        'font_size_sigma': 1,
        'line_spacing': 50,
        'line_spacing_sigma': 1,
        'word_spacing': 0,
        'word_spacing_sigma': 1,
        'is_half_char': lambda c: c.isdigit() or c in (',', '.', ' '),
        'is_end_char': lambda c: c in ('!', '.', '?')
    }
    text = """彼黍离离 彼稷之苗 行迈靡靡 中心摇摇 知我者 谓我心忧 不知我者 谓我何求 悠悠苍天 此何人哉
彼黍离离 彼稷之穗 行迈靡靡 中心如醉 知我者 谓我心忧 不知我者 谓我何求 悠悠苍天 此何人哉
彼黍离离 彼稷之实 行迈靡靡 中心如噎 知我者 谓我心忧 不知我者 谓我何求 悠悠苍天 此何人哉
"""
    images = handwrite(text, template)
    images[0].save("./out/shuli.jpg")


if __name__ == '__main__':
    freeze_support()
    main()
