"""Tetanus spec tests."""
from typing import List

import asyncio
import pytest

from Lego3.example.components.giraffe import Giraffe
from Lego3.example.libs.tetanus import Tetanus

TEST_VERSION = 3


class TestsSpecGiraffe:
    """A Giraffe spec tests base.

    Args:
        giraffe: Giraffe instance.
    """

    _giraffe: Giraffe = None # type: ignore

    @classmethod
    def setup_class(cls, components: List[Giraffe]) -> None:
        """Initializes the variables once in the start of the spec.

        Args:
            components: Required components.
        """

        cls._giraffe, *_ = components


class TestsSpecTetanus(TestsSpecGiraffe):
    """A Tetanus spec tests.

    Args:
        _tetanus_lib: An instance of the tested library.
        _echo_port: A port to echo on.
    """

    _tetanus_lib: Tetanus
    _echo_port: int

    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components: List[Giraffe]) -> None:
        """Initializes the variables once in the start of the spec.

        Args:
            components: Required components.
        """

        super().setup_class(components)

        cls._tetanus_lib = Tetanus()
        cls._echo_port = 1337

    @pytest.fixture(scope='function', autouse=True, params=[TEST_VERSION])
    def tetanus(self, request):
        """Install Tetanus before every test function, and uninstall after test end."""
        tetanus_version = request.param
        # Install Tetanus at the start of each test.
        self._tetanus_lib.install(TestsSpecTetanus._giraffe, tetanus_version, self._echo_port)
        yield
        # Uninstall Tetanus at the end of each test.
        self._tetanus_lib.uninstall(TestsSpecTetanus._giraffe)

    @pytest.mark.lego('zebra.alice')
    async def test_send_and_recv(self, components): # type: ignore
        """Send packets and expect them back."""

        zebra, *_ = components
        await zebra.send_and_receive(TestsSpecTetanus._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra.alice and zebra.logan')
    async def test_multi_send_and_recv(self, components): # type: ignore
        """Send packets from multiple components and expect them back."""

        tasks = []

        for component in components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(TestsSpecTetanus._giraffe.get_ip(), self._echo_port)))

        await asyncio.gather(*tasks)

    @pytest.mark.lego('zebra.alice')
    async def test_monitor_send_and_recv(self, components): # type: ignore
        """Send packets and expect them back while validating no bad logs written."""

        zebra, *_ = components
        with TestsSpecTetanus._giraffe.monitor_logs(event_handler=None, directory='.'):
            await zebra.send_and_receive(TestsSpecTetanus._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra.alice and zebra.logan')
    async def test_multi_monitor_send_and_receive(self, components): # type: ignore
        """Send and receive data from multiple components, while validating no bad logs written."""

        tasks = []

        for component in components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(TestsSpecTetanus._giraffe.get_ip(), self._echo_port)))

        with TestsSpecTetanus._giraffe.monitor_logs(event_handler=None, directory='.'):
            await asyncio.gather(*tasks)
