from setuptools import setup, find_packages
from setuptools.command.install import install
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sbtmh',
    version='0.1',
    description='Sequence Bloom Trees meet MinHash sketches',
    long_description=long_description,
    url='https://github.com/luizirber/2016-sbt-minhash/',
    author='Luiz Irber, Camille Scott, C Titus Brown',
    author_email='sbtmh@luizirber.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
    ],
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["sbt", "sbtmh"],
    install_requires=['khmer', 'sourmash', 'numpy'],
)
