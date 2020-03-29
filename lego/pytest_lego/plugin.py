import asyncio
import functools
import socket
import plumbum
import pytest
import rpyc

from pytest_lego import slave_factory

MARK = "lego"


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
    manager = request.config.inicfg.config.sections[MARK]["resouce_manager"]
    lego_manager = rpyc.connect(host=manager, port=18861)
    request.addfinalizer(lego_manager.close)
    return lego_manager


def pytest_configure(config):
    # Verify inifile
    assert MARK in config.inicfg.config.sections, f"Missing {MARK} section in inifile"
    assert "resouce_manager" in config.inicfg.config.sections[MARK], ""

    # Add the lego mark
    config.addinivalue_line(
        "markers",
        "lego: Lego mark used in order to supply slaves by query"
    )


@pytest.mark.tryfirst
def pytest_fixture_setup(fixturedef, request):
    """
    Addes the ability to add lego marks to `setup_class` functions in test classes.
    """
    if '_Class__pytest_setup_class' != fixturedef.argname:
        return

    test_class = request.cls
    marks = getattr(test_class.setup_class, "pytestmark", None)
    if marks is None:
        return

    mark = next(mark for mark in marks if MARK == mark.name)
    if mark is None:
        return

    @functools.wraps(fixturedef.func)
    def setup_class_wrapper(*args, **kwargs):
        lego_manager, *_ = request._fixture_defs["slaves"].cached_result
        with slave_factory.acquire_slaves(lego_manager, *mark.args, **mark.kwargs) as slaves:
            test_class.setup_class(test_class, slaves)
            try:
                yield 
            finally:
                teardown_class = getattr(test_class, "teardown_class", None)
                if teardown_class is not None:
                    teardown_class(test_class)

    fixturedef.func = setup_class_wrapper


@pytest.mark.tryfirst
def pytest_pyfunc_call(pyfuncitem):
    """
    Wraps the test function which is stored in `item.obj`.
    The wrapper uses the fixture in order to create the slaves and pass to the test.
    :param item: pytest.Item
    :return:
    """
    lego_mark = pyfuncitem.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    test = pyfuncitem.obj
    if asyncio.iscoroutinefunction(test):
        @functools.wraps(test)
        async def test_wrapper(*args, **kwargs):
            return await async_run_test(test, lego_mark, *args, lego_manager=kwargs["slaves"])

    else:
        @functools.wraps(test)
        def test_wrapper(*args, **kwargs):
            return run_test(test, lego_mark, *args, lego_manager=kwargs["slaves"])

    test_wrapper.pytestmark = test.pytestmark
    pyfuncitem.obj = test_wrapper


def run_test(test_function, mark, lego_manager):
    with slave_factory.acquire_slaves(lego_manager, *mark.args, **mark.kwargs) as slaves:
        return test_function(slaves)


async def async_run_test(test_function, mark, lego_manager):
    with slave_factory.acquire_slaves(lego_manager, *mark.args, **mark.kwargs) as slaves:
        return await test_function(slaves)
