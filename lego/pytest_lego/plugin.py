import rpyc
import pytest
import importlib
import plumbum
import socket

MARK = "lego"


def get_library(slave):
    d = {
        "giraffe": "lib.NetworkElement",
        "zebra": "lib.NetworkElement",
        "elephant": "lib.NetworkElement"
    }
    *module, lib = "lib.NetworkElement".split('.')
    return getattr(importlib.import_module('.'.join(module)), lib)


def prepare_slave(slave):
    # try:
    # resource_manager = rpyc.connect(host='central', port=18861)
    # except:  # TODO: Handle specify
    #     machine = plumbum.SshMachine("central", user="root")
    #     with rpyc.utils.zerodeploy.DeployedServer(machine) as server:
    #         conn = server.classic_connect()
    #         pass
    # setup_result = resource_manager.root.request_setup()
    # assert setup_result  # TODO: Wait async for setup

    library = get_library(slave)
    return library(slave)


def pytest_cmdline_parse(pluginmanager, args):
    pass


def pytest_generate_tests(metafunc):
    """
    Generate (multiple) parametrized calls to a test function.

    :param metafunc: _pytest.python.Metafunc
    :return:
    """

    lego_mark = metafunc.definition.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    assert ["slave"] == metafunc.fixturenames, "Lego test must have argument 'slave'"
    metafunc.parametrize("slave", next(metafunc.definition.iter_markers()).args)


def pytest_runtest_setup(item: pytest.Item):
    lego_mark = item.get_closest_marker(MARK)
    if lego_mark is None:
        # The test doesn't have lego mark
        return

    test_function = item.obj

    def test_wrapper(*args, **kwargs):
        test_function(slave=prepare_slave(*args, **kwargs))

    item.obj = test_wrapper
    pass
