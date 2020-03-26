import contextlib
import importlib


def get_library(lib_name):
    *module, lib_class = lib_name.split('.')
    return getattr(importlib.import_module('.'.join(module)), lib_class)


@contextlib.contextmanager
def acquire_slaves(resource_manager, query, exclusive=True):
    """
    Creates salves based on the requested setup.

    Args:
        setup - The requested setup.

    Returns:
        slaves.
    """
    with resource_manager.root.acquire(query, exclusive) as slaves:
        yield [get_library(library_name)(hostname) for hostname, library_name in slaves]
