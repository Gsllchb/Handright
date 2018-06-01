# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import pylf


VERSION = pylf.__version__


def get_long_description() -> str:
    with open('README.md') as f:
        return f.read()


classifiers=[
    "License :: OSI Approved :: BSD License",
    "Topic :: Multimedia :: Graphics",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython"
]


requires = [
    'setuptools>=38.6.0',
    'pillow >= 5.0.0, < 6',
]


setup(
    classifiers=classifiers,
    name='pylf',
    version=VERSION,
    author='Gsllchb',
    author_email="Gsllchb@gmail.com",
    packages=find_packages(),
    install_requires=requires,
    python_requires='>=3.4',
    description="A lightweight Python library for simulating Chinese handwriting",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license="bsd-3-clause",
    keywords="simulating Chinese handwriting",
    url="https://github.com/Gsllchb/PyLf",
    zip_safe=True
)
