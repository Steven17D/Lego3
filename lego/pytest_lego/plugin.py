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
def slaves(request):
    """
    Provides the connection to the resource manager.
    :return: RPyC connection to ResourceManager service.
    """
    try:
        resource_manager = rpyc.connect(host='central', port=18861)
    except:  # TODO: Handle specify
        with plumbum.SshMachine("central", user="root", password="password") as machine:
            with rpyc.utils.zerodeploy.DeployedServer(machine) as server:
                with server.classic_connect() as connection:
                    # TODO: connection.upload(ResourceManager)
                    resource_manager = connection

    request.addfinalizer(resource_manager.close)
    return resource_manager


def pytest_generate_tests(metafunc):
    """
    Official: Generate (multiple) parametrized calls to a test function.
    Used in order to verify lego test function signature to have the 'slaves' fixture.
    :param metafunc: _pytest.python.Metafunc
    :return:
    """
    lego_mark = metafunc.definition.get_closest_marker(MARK)
    if lego_mark is not None:
        assert "slaves" in metafunc.fixturenames, "Lego test must use fixture 'slaves'"


def pytest_runtest_setup(item: pytest.Item):
    """
    Wraps the test function which is stored in `item.obj`.
    The wrapper uses the fixture in order to create the slaves and pass to the test.
    :param item: pytest.Item
    :return:
    """
    lego_mark = item.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    test_function = item.obj
    if asyncio.iscoroutinefunction(test_function):
        @functools.wraps(test_function)
        async def test_wrapper(*args, **kwargs):
            return await async_run_test(test_function, lego_mark, *args, resource_manager=kwargs["slaves"])

    else:
        @functools.wraps(test_function)
        def test_wrapper(*args, **kwargs):
            return run_test(test_function, lego_mark, *args, resource_manager=kwargs["slaves"])

    test_wrapper.pytestmark = test_function.pytestmark
    item.obj = test_wrapper


def run_test(test_function, mark, resource_manager):
    with slave_factory.acquire_slaves(resource_manager, *mark.args, **mark.kwargs) as slave:
        return test_function(slave)


async def async_run_test(test_function, mark, resource_manager):
    with slave_factory.acquire_slaves(resource_manager, *mark.args, **mark.kwargs) as slave:
        return await test_function(slave)
