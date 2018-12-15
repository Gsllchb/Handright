# coding: utf-8
import argparse
import datetime
import os.path
import sys

import pylf

DESCRIPTION = """The cmd tool for PyLf"""

ENCODING = "utf-8"

TEXT_FILE = "content.txt"

OUTPUT_DIRECTORY = "output"
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
    template = {}
    # TODO
    return template


def _output(directory: str, images, quiet: bool):
    path = os.path.join(
        directory,
        OUTPUT_DIRECTORY,
        str(datetime.datetime.now())
    )
    image_path_fmt = os.path.join(path, "{}.{fmt}".format(fmt=OUTPUT_FORMAT))
    for index, image in enumerate(images):
        image.save(image_path_fmt.format(index))
    if quiet:
        return
    msg = "{} pages successfully generated! Please check {}."
    print(msg.format(len(images), path))


def main():
    run(*sys.argv[1:])


if __name__ == '__main__':
    main()
