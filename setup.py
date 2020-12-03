#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="advent-of-code-2020",
    version="0.1",
    description="Advent of Code 2020 solutions",
    url="https://github.com/Soft/advent-of-code-2020",
    packages=find_packages(),
    entry_points={"console_scripts": ["aoc=aoc.runner:main"]},
    include_package_data=True,
    keywords=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
