"""
Implementation of the pytest-lego plugin.
"""
import asyncio
import functools
import pytest
import rpyc

from pytest_lego import slave_factory


@pytest.fixture(scope="session")
def slaves(request):
    """
    Provides the connection to the lego manager.
    The 'slave' fixture doesn't provide slaves but provides a way
    for our test wrapper to create slaves.
    Using the lego manager API the test wrapper acquires the slaves and
    provide them to the original test function.
    :return: RPyC connection to LegoManager service.
    """
    manager = request.config.inicfg.config.sections["lego"]["lego_manager"]
    lego_manager = rpyc.connect(host=manager, port=18861)
    request.addfinalizer(lego_manager.close)
    return lego_manager


def pytest_configure(config):
    """
    Validates inifile and adds the lego mark.
    """
    # assert MARK in config.inicfg.config.sections, f"Missing {MARK} section in inifile"
    # assert "lego_manager" in config.inicfg.config.sections[MARK], "Missing lego_manager hostname in inifile"

