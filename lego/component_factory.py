"""
Supply components to the plugin by acquiring them in the lego manager and wrapping in the appropriate library.
"""
import asyncio
import contextlib
import functools
import importlib
from lego.pytest_lego.plugin import slaves


def require_components(query: str, exclusive: bool=True):
    """
    Wraps the test function.
    The wrapper uses the fixture in order to create the slaves and pass to the test.
    :param query:
    :param exclusive:
    :return:
    """
    def test_wrapper(test):
        if asyncio.iscoroutinefunction(test):
            @functools.wraps(test)
            async def run_test(*args, **kwargs):
                lego_manager = kwargs.pop("slaves")
                with acquire_slaves(lego_manager, query, exclusive) as wrapped_slaves:
                    return await test(*args, **kwargs, slaves=wrapped_slaves)

        else:
            @functools.wraps(test)
            def run_test(*args, **kwargs):
                lego_manager = slaves if 'setup_class' == test.__name__ else kwargs.pop("slaves")
                with acquire_slaves(lego_manager, query, exclusive) as wrapped_slaves:
                    return test(*args, **kwargs, slaves=wrapped_slaves)
        
        return run_test

    return test_wrapper


@contextlib.contextmanager
def acquire_slaves(lego_manager, query, exclusive):
    """
    Creates salves based on the requested setup.

    Args:
        setup - The requested setup.

    Returns:
        slaves.
    """
    with lego_manager.root.acquire(query, exclusive) as slaves:
        with contextlib.ExitStack() as stack:
            yield [
                stack.enter_context(get_library(library_name)(hostname))
                for hostname, library_name in slaves
            ]


def get_library(lib_name):
    """
    Receives string which represents a library name.
    Returns the library object by importing it.
    """
    *module, lib_class = lib_name.split('.')
    return getattr(importlib.import_module('.'.join(module)), lib_class)
