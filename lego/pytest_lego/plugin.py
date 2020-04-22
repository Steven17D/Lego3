# type: ignore
# pylint: skip-file
"""
Implementation of the pytest-lego plugin.
"""
from typing import Any, List

import functools
import pytest
import rpyc

from . import component_factory
from Lego3.components.core import Core

MARK = 'lego'


@pytest.fixture(scope='session')
def lego_manager(request) -> rpyc.Connection:
    """Provides the connection to the lego manager.

    Args:
        request: A PyTest fixture helper, with information on the requesting test function.

    Returns:
        RPyC connection to LegoManager service.
    """

    assert MARK in request.config.inicfg.config.sections, f'Missing {MARK} section in inifile'

    try:
        manager_hostname = request.config.inicfg.config.sections[MARK]['lego_manager_hostname']
        manager_port = request.config.inicfg.config.sections[MARK]['lego_manager_port']
    except KeyError as e:
        missing_key = e.args[0]
        raise KeyError(f'Missing {missing_key} under {MARK} section in inifile')

    lego_manager = rpyc.connect(manager_hostname, manager_port)
    request.addfinalizer(lego_manager.close)

    return lego_manager


@pytest.fixture()
def components(request, lego_manager) -> List[Core]:
    """Provides the components requested in corresponding lego mark for the test.

    This fixture provides the components requested by the test function.
    To provide arguments to the components, one should define [component] section in pytest config file.
    The fixture splits the components given in mark.lego by the word 'and'.

    Typical usage example:

    @pytest.mark.lego('zebra.alice and elephant.bob')
    def test_default_sizes(self, components):
        zebra, elephant, *_ = components
        assert zebra.size == elephant.size

    Example for configuration in pytest.ini:
    [zebra.alice]
    hostname = zebra
    username = admin
    password = password
    [elephant.bob]
    hostname=192.168.100.11
    name = Bob
    size = 120

    Args:
        request: A PyTest fixture helper, with information on the requesting test function.
        lego_manager: An RPyC connection to LegoManager service.

    Returns:
        List of components requested in lego.mark.
    """
    print(request.fixturenames)

    lego_mark = request.node.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark.
        return None

    with component_factory.acquire_components(
            lego_manager,
            request.config,
            *lego_mark.args,
            **lego_mark.kwargs
    ) as components:
        yield components


def pytest_configure(config: Any) -> None:
    """Adds the lego mark.

    Args:
        config: A PyTest configuration object.
    """

    config.addinivalue_line(
        'markers',
        f'{MARK}: Lego mark used in order to supply components by query'
    )


@pytest.mark.tryfirst
def pytest_fixture_setup(fixturedef, request):
    """Adds the ability to add lego marks to `setup_class` functions in test classes."""

    if fixturedef.argname != '_Class__pytest_setup_class':
        return

    test_class = request.cls
    marks = getattr(test_class.setup_class, 'pytestmark', None)
    if marks is None:
        return

    mark = next(mark for mark in marks if MARK == mark.name)
    if mark is None:
        return

    @functools.wraps(fixturedef.func)
    def setup_class_wrapper(*args, **kwargs):
        lego_manager = request.getfixturevalue('connections')
        with component_factory.acquire_connections(lego_manager, *mark.args, **mark.kwargs) as wrapped_connections:
            test_class.setup_class(wrapped_connections, *args, **kwargs)
            try:
                yield
            finally:
                teardown_class = getattr(test_class, 'teardown_class', None)
                if teardown_class is not None:
                    teardown_class()

    fixturedef.func = setup_class_wrapper
