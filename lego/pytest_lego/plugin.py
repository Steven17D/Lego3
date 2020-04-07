"""
Implementation of the pytest-lego plugin.
"""
import asyncio
import functools
import pytest
import rpyc

from . import component_factory

MARK = 'lego'


@pytest.fixture(scope='session')
def components(request):
    """Provides the connection to the lego manager.

    The 'components' fixture doesn't provide components but provides a way
    for our test wrapper to create components.
    Using the lego manager API the test wrapper acquires the components and
    provide them to the original test function.

    Returns:
        RPyC connection to LegoManager service.
    """
    assert MARK in request.config.inicfg.config.sections, f'Missing {MARK} section in inifile'
    assert 'lego_manager' in request.config.inicfg.config.sections[MARK], (
        'Missing lego_manager hostname in inifile')
    manager = request.config.inicfg.config.sections[MARK]['lego_manager']
    lego_manager = rpyc.connect(host=manager, port=18861)
    request.addfinalizer(lego_manager.close)
    return lego_manager


def pytest_configure(config):
    """Adds the lego mark."""

    config.addinivalue_line(
        'markers',
        'Lego: Lego mark used in order to supply components by query'
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
        lego_manager, *_ = request._fixture_defs['components'].cached_result
        with component_factory.acquire_components(
                lego_manager, *mark.args, **mark.kwargs) as wrapped_components:
            test_class.setup_class(wrapped_components, *args, **kwargs)
            try:
                yield
            finally:
                teardown_class = getattr(test_class, 'teardown_class', None)
                if teardown_class is not None:
                    teardown_class()

    fixturedef.func = setup_class_wrapper


@pytest.mark.tryfirst
def pytest_pyfunc_call(pyfuncitem: pytest.Item):
    """Wraps the test function which is stored in `item.obj`.

    The wrapper uses the fixture in order to create the components and pass to the test.

    Args:
        pyfuncitem: The pytest test object.
    """

    lego_mark = pyfuncitem.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    test = pyfuncitem.obj
    if asyncio.iscoroutinefunction(test):
        @functools.wraps(test)
        async def test_wrapper(**kwargs):
            return await async_run_test(test, lego_mark, lego_manager=kwargs['components'])

    else:
        @functools.wraps(test)
        def test_wrapper(**kwargs):
            return run_test(test, lego_mark, lego_manager=kwargs['components'])

    test_wrapper.pytestmark = test.pytestmark
    pyfuncitem.obj = test_wrapper


def run_test(test_function, mark, lego_manager):
    """Runs the test function with wrapped components."""

    with component_factory.acquire_components(
            lego_manager, *mark.args, **mark.kwargs) as wrapped_components:
        return test_function(wrapped_components)


async def async_run_test(test_function, mark, lego_manager):
    """Runs the test function with wrapped components and await it."""

    with component_factory.acquire_components(
            lego_manager, *mark.args, **mark.kwargs) as wrapped_components:
        return await test_function(wrapped_components)
