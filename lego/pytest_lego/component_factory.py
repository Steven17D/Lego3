"""
Supply components to the plugin by acquiring them in the lego manager,
and wrapping in the appropriate library.
"""
import contextlib
import importlib


def get_library(lib_name: str):
    """Gets the requesnt library instance.

    Args:
        lib_name: the requeted module instance.

    Retruns:
        The library instance.
    """

    *module, lib_class = lib_name.split('.')
    return getattr(importlib.import_module('.'.join(module)), lib_class)


@contextlib.contextmanager
def acquire_components(lego_manager, query: str, exclusive:bool = True):
    """Creates components based on the requested setup.

    Args:
        setup - The requested setup.

    Returns:
        components.
    """

    with lego_manager.root.acquire(query, exclusive) as components:
        with contextlib.ExitStack() as stack:
            yield [
                stack.enter_context(get_library(library_name)(hostname))
                for hostname, library_name in components
            ]
