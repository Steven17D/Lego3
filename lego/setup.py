"""This file describes the lego plugin setup info."""
from setuptools import setup

setup(
    name="pytest-lego",
    version="0.1",
    description="Lego plugin for pytest",
    packages=["pytest_lego"],
    install_requires=[
        "pytest>=5.4.1"
    ],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["lego = pytest_lego.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
