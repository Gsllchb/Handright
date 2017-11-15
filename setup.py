from setuptools import setup, find_packages
import pylf
setup(
    name='pylf',
    version='0.1.0',
    author='Gsllchb',
    author_email="Gsllchb@gmail.com",
    packages=find_packages(),
    install_requires=['pillow>=4.3.0', 'multiprocess>=0.70.5'],
    python_requires='>=3.5',
    description="Lightweight and fast Python library for simulating Chinese handwriting.",
    long_description=pylf.__doc__,
    license="bsd-3-clause",
    keywords="simulating Chinese handwriting",
    url="https://github.com/Gsllchb/PyLf"
)