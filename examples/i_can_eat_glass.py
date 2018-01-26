from PIL import Image, ImageFont
from pylf import handwrite
from multiprocessing import freeze_support


def main():
    template = dict(
        background=Image.open("./pictures/树信笺纸.jpg"),
        box=(50, 500, 800 - 80, 800 - 50),
        font=ImageFont.truetype("./fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"),
        font_size=60,
    )
    text = "我能吞下玻璃而不伤身体。"
    images = handwrite(text, template)
    images[0].crop((0, 450, 800, 800-200)).save("./out/i_can_eat_glass.jpg")


if __name__ == '__main__':
    freeze_support()
    main()
