"""
Supply components to the plugin by acquiring them in the lego manager,
then getting their arguments from pytest configuration (pytest.ini file).
"""
from typing import Iterator, List, Any, Type

import contextlib
import importlib
import rpyc

from Lego3.components.core import Core


def get_component_class(component_path: str) -> Type[Core]:
    """Gets the requested component's class object.

    Args:
        component_path: The path to the requested component class. For example, Lego3.example.components.zebra.Zebra

    Returns:
        The component's class object.
    """

    *module, component_class = component_path.split('.')
    return getattr(importlib.import_module('.'.join(module)), component_class)


def get_component(component_name: str, component_path: str, pytest_config: Any) -> Core:
    """Initialize the component object.

    Args:
        component_name: The component name in pytest config file (usually, pytest.ini file).
        component_path: The path to the requested component class.
        pytest_config: A PyTest configuration object associated with current test.

    Returns:
        Component object.
    """
    # A dictionary with all the arguments the component should receive in __init__.
    component_config = pytest_config.inicfg.config.sections[component_name]

    component_class = get_component_class(component_path)
    return component_class(**component_config)


@contextlib.contextmanager
def acquire_components(
        lego_manager: rpyc.Connection,
        pytest_config: Any,
        query: str,
        exclusive: bool = True
) -> Iterator[List[Core]]:
    """Creates components based on the requested setup.

    Args:
        lego_manager: A lego manager instance.
        pytest_config: A PyTest configuration object associated with current test.
        query: A query that describes the requested setup.
        exclusive (optional): Whether to lock the requested setup. Defaults to True.

    Yields:
        The requested components.
    """

    with lego_manager.root.acquire(query, exclusive) as available_components:
        with contextlib.ExitStack() as stack:
            # yield [
            #     stack.enter_context(get_component(component_name, component_path, pytest_config))  # type: ignore
            #     for component_name, component_path in components
            # ]
            components = []
            for component_name, component_path in available_components:
                component = get_component(component_name, component_path, pytest_config)
                components.append(stack.enter_context(component))
            yield components
