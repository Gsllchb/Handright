# coding: utf-8
import os

import setuptools

import handright


def main():
    setuptools.setup(
        name=handright.__name__,
        version=handright.__version__,
        description="A lightweight Python library for simulating Chinese handwriting",
        license="bsd-3-clause",
        author="Chenghui Li (Gsllchb)",
        author_email="Gsllchb@qq.com",
        python_requires=">= 3.7",
        keywords="simulating Chinese handwriting",
        url="https://github.com/Gsllchb/Handright",
        long_description_content_type="text/markdown",
        long_description=get_long_description(),
        zip_safe=True,
        packages=setuptools.find_packages(exclude=("*.tests", "tests")),
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
        install_requires=("pillow >= 8.3.2, < 10",),
        setup_requires=("setuptools>=38.6.0",),
    )


def get_long_description() -> str:
    with open(abs_path("README.md"), encoding="utf-8") as f:
        return f.read()


def abs_path(path: str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


if __name__ == "__main__":
    main()
