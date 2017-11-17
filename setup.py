from setuptools import setup, find_packages
import pylf
classifiers = [
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    "Topic :: Multimedia :: Graphics",
    'License :: OSI Approved :: BSD License',
    "Topic :: Multimedia :: Graphics",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    "Programming Language :: Python :: 3.6",
]
setup(
    name='pylf',
    version='0.1.3',
    author='Gsllchb',
    author_email="Gsllchb@gmail.com",
    packages=find_packages(),
    install_requires=['pillow>=4.3.0', 'multiprocess>=0.70.5', 'dill>=0.2.7'],
    python_requires='>=3.5',
    description="A lightweight and fast Python library for simulating Chinese handwriting.",
    long_description=pylf.__doc__,
    license="bsd-3-clause",
    keywords="simulating Chinese handwriting",
    url="https://github.com/Gsllchb/PyLf"
)
