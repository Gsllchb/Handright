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
        _get_text(args.project),
        _get_template(args.project)
    )
    _output(args.project, images, args.quiet)


def _parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        add_help=False
    )
    parser.add_argument(
        "project",
        help="手写项目的路径"
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="显示此帮助信息并退出"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="运行时关闭输出"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="PyLf {}".format(pylf.__version__),
        help="显示程序版本号并退出"
    )
    return parser.parse_args(args)


def _get_text(parent: str):
    path = os.path.join(parent, TEXT_FILE)
    with open(path, encoding=ENCODING) as file:
        return file.read()


def _get_template(parent: str):
    with open(
            os.path.join(parent, TEMPLATE_FILE),
            encoding=ENCODING
    ) as file:
        template = yaml.safe_load(file)

    background_file = next(
        (n for n in os.listdir(parent)
         if n.startswith(BACKGROUND_FILE_PREFIX))
    )
    template["background"] = PIL.Image.open(
        os.path.join(parent, background_file)
    )

    template["font"] = PIL.ImageFont.truetype(
        os.path.join(parent, FONT_FILE)
    )
    return template


def _output(parent: str, images, quiet: bool):
    path = _get_output_path(parent)
    for index, image in enumerate(images):
        image.save(
            os.path.join(path, "{}.{}".format(index, OUTPUT_FORMAT))
        )
    if quiet:
        return
    msg = "{} page(s) successfully generated! Please check {}."
    print(msg.format(len(images), path))


def _get_output_path(parent: str) -> str:
    path = os.path.join(
        parent,
        OUTPUT_DIRECTORY,
        "{:.6f}".format(time.time()).replace('.', '')
    )
    os.makedirs(path, exist_ok=True)
    return path


def main():
    run(*sys.argv[1:])


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
