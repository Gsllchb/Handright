# coding: utf-8
import argparse
import os
import sys
import time

import PIL.Image
import PIL.ImageFont
import yaml

import pylf

DESCRIPTION = """The cmd tool for PyLf"""  # TODO

ENCODING = "utf-8"

TEXT_FILE = "content.txt"

TEMPLATE_FILE = "template.yml"
FONT_FILE = "font.ttf"
BACKGROUND_FILE_PREFIX = "background."

OUTPUT_DIRECTORY = "out"
OUTPUT_FORMAT = "png"


def run(*args):
    args = _parse_args(args)
    images = pylf.handwrite(
        _get_text(args.dir),
        _get_template(args.dir)
    )
    _output(args.dir, images, args.quiet)


def _parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("dir", help="directory of handwriting project")
    return parser.parse_args(args)


def _get_text(directory: str):
    path = os.path.join(directory, TEXT_FILE)
    with open(path, encoding=ENCODING) as file:
        return file.read()


def _get_template(directory: str):
    with open(
            os.path.join(directory, TEMPLATE_FILE),
            encoding=ENCODING
    ) as file:
        template = yaml.safe_load(file)

    background_file = next(
        (n for n in os.listdir(directory)
         if n.startswith(BACKGROUND_FILE_PREFIX))
    )
    template["background"] = PIL.Image.open(
        os.path.join(directory, background_file)
    )

    template["font"] = PIL.ImageFont.truetype(
        os.path.join(directory, FONT_FILE)
    )
    return template


def _output(directory: str, images, quiet: bool):
    path = _get_output_path(directory)
    for index, image in enumerate(images):
        image.save(
            os.path.join(path, "{}.{}".format(index, OUTPUT_FORMAT))
        )
    if quiet:
        return
    msg = "{} page(s) successfully generated! Please check {}."
    print(msg.format(len(images), path))


def _get_output_path(directory: str) -> str:
    path = os.path.join(
        directory,
        OUTPUT_DIRECTORY,
        "{:.6f}".format(time.time()).replace('.', '')
    )
    os.makedirs(path, exist_ok=True)
    return path


def main():
    run(*sys.argv[1:])


if __name__ == '__main__':
    main()
