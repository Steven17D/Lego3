import pytest


def pytest_generate_tests(metafunc):
    if "slave" in metafunc.fixturenames:
        metafunc.parametrize("slave", next(metafunc.definition.iter_markers()).args)


def pytest_runtest_setup(item: pytest.Item):
    # a = item.ihook.pytest_runtest_call
    #
    # def f(*args, **kwargs):
    #     print("Before")
    #     print(f"a = {a}, args = {args}, kwargs={kwargs}")
    #     a(*args, **kwargs)
    #     print("After")
    #
    # item.ihook.pytest_runtest_call = f
    # print("setting up", item)
    # for mark in item.iter_markers():
    #     print(f"Mark is {mark}")
    pass


def pytest_pyfunc_call(pyfuncitem):
    test_function = pyfuncitem.obj

    def wrapped_test(*args, **kwargs):
        slave = OSError(kwargs["slave"])
        test_function(slave)

    pyfuncitem.obj = wrapped_test
    pass
