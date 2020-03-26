import rpyc
import pytest
import importlib
import plumbum
import socket
import functools
import asyncio
from pytest_lego import slave_factory

MARK = "lego"


@pytest.fixture(scope="session")
def slave():
    """
    Provides the connection to the resource manager.
    :return: RPyC connection to ResourceManager service.
    """
    try:
        return rpyc.connect(host='central', port=18861)
    except:  # TODO: Handle specify
        machine = plumbum.SshMachine("central", user="root", password="password")
        with rpyc.utils.zerodeploy.DeployedServer(machine) as server:
            conn = server.classic_connect()
            return  # TODO: Upload resource_manager


def pytest_generate_tests(metafunc):
    """
    Generate (multiple) parametrized calls to a test function.
    :param metafunc: _pytest.python.Metafunc
    :return:
    """
    lego_mark = metafunc.definition.get_closest_marker(MARK)
    if lego_mark is not None:
        assert ["slave"] == metafunc.fixturenames, "Lego test must use fixture 'slave'"


def pytest_runtest_setup(item: pytest.Item):
    lego_mark = item.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    test_function = item.obj
    if asyncio.iscoroutinefunction(test_function):
        @functools.wraps(test_function)
        async def test_wrapper(*args, **kwargs):
            return await async_run_test(test_function, lego_mark, *args, resource_manager=kwargs["slave"])

    else:
        @functools.wraps(test_function)
        def test_wrapper(*args, **kwargs):
            return run_test(test_function, lego_mark, *args, resource_manager=kwargs["slave"])

    test_wrapper.pytestmark = test_function.pytestmark
    item.obj = test_wrapper


def run_test(test_function, mark, resource_manager):
    with slave_factory.acquire_slaves(resource_manager, *mark.args, **mark.kwargs) as slave:
        return test_function(slave)


async def async_run_test(test_function, mark, resource_manager):
    with slave_factory.acquire_slaves(resource_manager, *mark.args, **mark.kwargs) as slave:
        return await test_function(slave)
