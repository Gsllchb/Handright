# -*- coding: utf-8 -*-
import setuptools

import pylf

VERSION = pylf.__version__

CLASSIFIERS = ["License :: OSI Approved :: BSD License",
               "Topic :: Multimedia :: Graphics",
               "Programming Language :: Python",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3.4",
               "Programming Language :: Python :: 3.5",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3.7",
               "Programming Language :: Python :: Implementation :: CPython"]

INSTALL_REQUIRES = ['pillow >= 5.2.0, < 6', ]

SETUP_REQUIRES = ['setuptools>=38.6.0', ]


def get_long_description() -> str:
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def main():
    setuptools.setup(classifiers=CLASSIFIERS,
                     name='pylf',
                     version=VERSION,
                     author='Gsllchb',
                     author_email="Gsllchb@gmail.com",
                     packages=setuptools.find_packages(),
                     install_requires=INSTALL_REQUIRES,
                     setup_requires=SETUP_REQUIRES,
                     python_requires='>=3.4',
                     description="A lightweight Python library for simulating Chinese handwriting",
                     long_description=get_long_description(),
                     long_description_content_type='text/markdown',
                     license="bsd-3-clause",
                     keywords="simulating Chinese handwriting",
                     url="https://github.com/Gsllchb/PyLf",
                     zip_safe=True)


if __name__ == '__main__':
    main()
