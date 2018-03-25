from setuptools import setup, find_packages

import pylf

classifiers = [
    'License :: OSI Approved :: BSD License',
    "Topic :: Multimedia :: Graphics",
    "Programming Language :: Python",
    'Programming Language :: Python :: 3.5',
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython"
]

setup(
    name='pylf',
    version=pylf.__version__,
    author='Gsllchb',
    author_email="Gsllchb@gmail.com",
    packages=find_packages(),
    install_requires=['pillow >= 5.0.0, < 6', ],
    python_requires='>=3.5, <3.7',
    description="A lightweight Python library for simulating Chinese handwriting",
    long_description=pylf.__doc__,
    license="bsd-3-clause",
    keywords="simulating Chinese handwriting",
    url="https://github.com/Gsllchb/PyLf",
    zip_safe=True
)
