from setuptools import setup, find_packages

import pylf


VERSION = pylf.__version__
PROJECT_URL_HEADER = "https://github.com/Gsllchb/PyLf/blob/v{}/".format(VERSION)


def get_long_description() -> str:
    file_paths = (
        "docs/API-Reference.md",
        "docs/CODE_OF_CONDUCT.md",
        "docs/CONTRIBUTING.md",
        "docs/ISSUE_TEMPLATE.md",
        "docs/Release-Notes.md",
        "LICENSE",
        "README.md"
    )
    with open('README.md') as f:
        long_description = f.read()
    for file_path in file_paths:
        long_description = long_description.replace(file_path, PROJECT_URL_HEADER + file_path)
    return long_description


setup(
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    name='pylf',
    version=VERSION,
    author='Gsllchb',
    author_email="Gsllchb@gmail.com",
    packages=find_packages(),
    setup_requires=['setuptools>=38.6.0', ],
    install_requires=['pillow >= 5.0.0, < 6', ],
    python_requires='>=3.5, <3.7',
    description="A lightweight Python library for simulating Chinese handwriting",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license="bsd-3-clause",
    keywords="simulating Chinese handwriting",
    url="https://github.com/Gsllchb/PyLf",
    zip_safe=True
)
