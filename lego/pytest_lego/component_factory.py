"""
Supply components to the plugin by acquiring them in the lego manager,
and wrapping in the appropriate library.
"""
from typing import Iterator, List

import contextlib
import importlib
import rpyc

import components.core


def get_library(lib_name: str) -> components.core.Core:
    """Gets the requesnt library instance.

    Args:
        lib_name: the requeted module instance.

    Retruns:
        The library instance.
    """

    *module, lib_class = lib_name.split('.')
    return getattr(importlib.import_module('.'.join(module)), lib_class)


@contextlib.contextmanager
def acquire_components(
        lego_manager: rpyc.Connection,
        query: str,
        exclusive: bool = True
    ) -> Iterator[List[components.core.Core]]:
    """Creates components based on the requested setup.

    Args:
        lego_manager: A lego manager instance.
        query: A query describes the requested setup.
        exclusive (optional): Wether to lock the requested setup. Defaults to True.

    Yields:
        The reqested components.
    """

    with lego_manager.root.acquire(query, exclusive) as _components:
        with contextlib.ExitStack() as stack:
            yield [
                stack.enter_context(get_library(library_name)(hostname))
                for hostname, library_name in _components
            ]
