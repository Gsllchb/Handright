# coding: utf-8
import shutil

import PIL.Image
import PIL.ImageFont
import yaml

import pylf
import pylf.__main__
from tests.util import *

SEED = "PyLf"

TEMP_DIR = ".pylf_tmp"
TEMP_IMAGE = ".pylf_tmp.png"

FONT_PATH = "fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"


def test_run():
    shutil.rmtree(abs_path(TEMP_DIR), ignore_errors=True)
    os.makedirs(abs_path(TEMP_DIR), exist_ok=True)

    background = PIL.Image.new(mode="L", size=(400, 500), color="white")
    background.save(abs_path(TEMP_DIR, "background.png"))

    font = PIL.ImageFont.truetype(abs_path(FONT_PATH))
    shutil.copy(abs_path(FONT_PATH), abs_path(TEMP_DIR, "font.ttf"))

    text = get_long_text()
    with open(abs_path(TEMP_DIR, "content.txt"), mode="x", encoding="utf-8") as f:
        f.write(text)

    template = {
        "margin": {"left": 25, "right": 25, "top": 50, "bottom": 50},
        "line_spacing": 22,
        "font_size": 20,
    }
    with open(abs_path(TEMP_DIR, "template.yml"), mode="x", encoding="utf-8") as f:
        f.write(yaml.safe_dump(template))
    template["background"] = background
    template["font"] = font

    images1 = pylf.handwrite(text, template, seed=SEED)
    pylf.__main__.run(abs_path(TEMP_DIR), "--quiet", "--seed", SEED)
    images_dir = abs_path(
        TEMP_DIR,
        "out",
        os.listdir(abs_path(TEMP_DIR, "out"))[0]
    )
    images2 = [PIL.Image.open(abs_path(images_dir, n)) for n in sorted(os.listdir(images_dir))]

    assert all(map(visually_equal, images1, images2))

    shutil.rmtree(abs_path(TEMP_DIR))
