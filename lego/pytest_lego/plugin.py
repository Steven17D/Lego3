import asyncio
import functools
import socket
import plumbum
import pytest
import rpyc
import rpyc.utils.classic
from rpyc.utils.zerodeploy import DeployedServer

import pytest_lego.slave_factory as slave_factory
from slaves import rpyc_classic

MARK = "lego"


@pytest.fixture(scope="session")
def slaves(request):
    """
    Provides the connection to the resource manager.
    :return: RPyC connection to ResourceManager service.
    """
    manager = request.config.inicfg.config.sections[MARK]["resouce_manager"]
    try:
        resource_manager = rpyc.connect(host=manager, port=18861)
    except ConnectionRefusedError:
        with plumbum.SshMachine(manager, user="root", password="password") as machine:
            with DeployedServer(machine) as server:
                with server.classic_connect() as connection:
                    spawn_resource_manager(connection)

        resource_manager = rpyc.connect(host=manager, port=18861)

    request.addfinalizer(resource_manager.close)
    return resource_manager


def spawn_resource_manager(connection):
    # Upload necessary dependencies
    rpyc.utils.classic.upload_package(connection, rpyc, '/root/rpyc')
    rpyc.utils.classic.upload_package(connection, plumbum, '/root/plumbum')
    rpyc.utils.classic.upload_package(connection, rpyc_classic, '/root/slaves')
    # Start the resource_manager python process
    ros = connection.modules.os
    args = ['python', '/root/slaves/resource_manager.py', '--host', '0.0.0.0']
    env = {"PYTHONPATH": "/root/"}
    # TODO: Make it work
    ros.spawnvpe(ros.P_NOWAIT, 'python', args, env)


def pytest_configure(config):
    # Verify inifile
    assert MARK in config.inicfg.config.sections, f"Missing {MARK} section in inifile"
    assert "resouce_manager" in config.inicfg.config.sections[MARK], ""

    # Add the lego mark
    config.addinivalue_line(
        "markers",
        "lego: Lego mark used in order to supply slaves by query"
    )


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
