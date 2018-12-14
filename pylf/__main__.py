# coding: utf-8
import argparse
import sys

DESCRIPTION = """The cmd tool for PyLf"""


def run(*args):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("path", help="path to handwriting project")
    parser.parse_args(args)
    # TODO


def main():
    run(*sys.argv[1:])


if __name__ == '__main__':
    main()
