import pytest
import functools
import rpyc


def get_slaves(*slaves):

    def decorator_wrapper(func):
        @functools.wraps(func)
        def wrapper():
            slave_manager = rpyc.connect(host="127.0.0.1", port=18861)
            with slave_manager.root.get_setup(slaves) as connections:
                func(connections)

        return wrapper

    return decorator_wrapper

@get_slaves("127.0.0.1")
def test_abc(slaves):
    print slaves
    slaves["127.0.0.1"].reboot()

"""
@get_slaves("PC-2", "PC-1")
def test_cba(slaves):
    print "AA"
    print slaves
"""
