"""Tetanus spec tests."""
from typing import List

import asyncio
import pytest

import components.core
import example.components.giraffe
import example.libs.tetanus


TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/cat"'
BUGY_LOGS_TOOL = TOOL + ' --output log.txt'
BUGY_SEND_TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/echo lego"'


class TestsSpecGiraffe:
    """A Giraffe spec tests base.

    Args:
        giraffe: Giraffe instance.
    """

    _giraffe: example.components.giraffe.Giraffe


    @classmethod
    def setup_class(cls, _components: List[components.core.Core]) -> None:
        """Initializes the variables once in the start of the spec.

        Args:
            _components: Required components.
        """

        cls._giraffe, *_ = _components


class TestsSpecTetanus(TestsSpecGiraffe):
    """A Tetanus spec tests.

    Args:
        _tetanus_lib: An instance of the tested library.
        _echo_port: A port to echo on.
    """

    _tetanus_lib: example.libs.tetanus.Tetanus
    _echo_port: int

    @classmethod
    @pytest.mark.lego('giraffe')
    def setup_class(cls, _components: List[components.core.Core]) -> None:
        """Initializes the variables once in the start of the spec.

        Args:
            _components: Required components.
        """

        super().setup_class(_components)

        cls._tetanus_lib = example.libs.tetanus.Tetanus()
        cls._echo_port = 1337

    def setup_method(self) -> None:
        """Installes Tetanus at the start of each test."""

        self._tetanus_lib.install(TestsSpecGiraffe._giraffe, TOOL, self._echo_port)

    def teardown_method(self) -> None:
        """Uninstalles Tetanus at the end of each test."""

        self._tetanus_lib.uninstall(TestsSpecGiraffe._giraffe)

    @pytest.mark.lego('zebra')
    async def test_send_and_recv(self, _components): # type: ignore
        "The test send packets and expect them back."""

        zebra, *_ = _components
        await zebra.send_and_receive(TestsSpecGiraffe._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_send_and_recv(self, _components): # type: ignore
        """The test send packets from multiple components and
            expect them back.
        """

        tasks = []

        for component in _components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(TestsSpecGiraffe._giraffe.get_ip(), self._echo_port)))

        await asyncio.gather(*tasks)

    @pytest.mark.lego('zebra')
    async def test_monitor_send_and_recv(self, _components): # type: ignore
        """The test send packets and expect them back while validating no bad
            logs written.
        """

        zebra, *_ = _components
        with TestsSpecGiraffe._giraffe.monitor_logs(event_handler=None, directory='.'):
            await zebra.send_and_receive(TestsSpecGiraffe._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_monitor_send_and_receive(self, _components): # type: ignore
        """The test send packets from multiple components and
            expect them back, while validating no bad logs written.
        """

        tasks = []

        for component in _components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(TestsSpecGiraffe._giraffe.get_ip(), self._echo_port)))

        with TestsSpecGiraffe._giraffe.monitor_logs(event_handler=None, directory='.'):
            await asyncio.gather(*tasks)
