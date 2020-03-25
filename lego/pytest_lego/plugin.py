import rpyc

MARK = "lego"



def prepare_slave(slave_hostname):
    resource_manager = rpyc.connect(host='central', port=18861)
    resource_manager.root.
    connection = rpyc.classic.connect(slave_hostname, keepalive=True)
    return


def pytest_cmdline_parse(pluginmanager, args):
    pass


def pytest_generate_tests(metafunc):
    """
    Generate (multiple) parametrized calls to a test function.

    :param metafunc: _pytest.python.Metafunc
    :return:
    """

    # next((mark for mark in metafunc.definition.iter_markers() if MARK == mark.name), None)
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
