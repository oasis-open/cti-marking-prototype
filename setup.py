#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'six==1.10.0',
]

setup(
    name="stixmarker",
    version="0.1.0",
    description="An API for handling Data Markings in STIX 2.0 content.",
    url="http://github.com/oasis-open/cti-marking-prototype",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
