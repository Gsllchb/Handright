# coding: utf-8
import os

import setuptools

import pylf

VERSION = pylf.__version__

CLASSIFIERS = (
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
)

INSTALL_REQUIRES = ("pillow >= 5.2.0, < 6", "pyyaml >= 3.13, < 5")

SETUP_REQUIRES = ("setuptools>=38.6.0",)


def get_long_description() -> str:
    with open(abs_path("README.md"), encoding="utf-8") as f:
        return f.read()


def main():
    setuptools.setup(
        classifiers=CLASSIFIERS,
        name="pylf",
        version=VERSION,
        author="Gsllchb",
        author_email="Gsllchb@gmail.com",
        packages=setuptools.find_packages(exclude=("*.tests", "tests")),
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
        python_requires=">= 3.5",
        description="A lightweight Python library for simulating Chinese handwriting",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        license="bsd-3-clause",
        keywords="simulating Chinese handwriting",
        url="https://github.com/Gsllchb/PyLf",
        zip_safe=True,
        entry_points={"console_scripts": ("pylf = pylf.__main__:main", ), }
    )


def abs_path(path: str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


if __name__ == "__main__":
    main()
