from setuptools import setup

setup(
    name="pytest-lego",
    description="Lego plugin for pytest",
    packages=["pytest_lego"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["lego = pytest_lego.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
