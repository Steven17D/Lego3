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
