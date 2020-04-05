"""Tetanus spec tests."""

import asyncio
import pytest

import libs.tetanus


TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/cat"'
BUGY_LOGS_TOOL = TOOL + ' --output log.txt'
BUGY_SEND_TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/echo lego"'


class TestsSpecGiraffe:
    """A Giraffe spec tests base."""
    @classmethod
    def setup_class(cls, components):
        cls._giraffe, *_ = components


class TestsSpecTetanus(TestsSpecGiraffe):
    """A Tetanus spec tests."""

    @classmethod
    @pytest.mark.lego('giraffe')
    def setup_class(cls, components):
        super().setup_class(components)

        cls._tetanus_lib = libs.tetanus.Tetanus()
        cls._echo_port = 1337

    def setup_method(self):
        self._tetanus_lib.install(self._giraffe, TOOL, self._echo_port)

    def teardown_method(self):
        self._tetanus_lib.uninstall(self._giraffe)

    @pytest.mark.lego('zebra')
    async def test_send_and_recv(self, components):
        "The test send packets and expect them back."""

        zebra, *_ = components
        await zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_send_and_recv(self, components):
        """The test send packets from multiple components and
            expect them back.
        """

        tasks = []

        for component in components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(self._giraffe.get_ip(), self._echo_port)))

        await asyncio.gather(*tasks)

    @pytest.mark.lego('zebra')
    async def test_monitor_send_and_recv(self, components):
        """The test send packets and expect them back while validating no bad
            logs written.
        """

        zebra, *_ = components
        with self._giraffe.monitor_logs(event_handler=None, directory='.'):
            await zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_monitor_send_and_receive(self, components):
        """The test send packets from multiple components and
            expect them back, while validating no bad logs written.
        """

        tasks = []

        for component in components:
            tasks.append(asyncio.ensure_future(
                component.send_and_receive(self._giraffe.get_ip(), self._echo_port)))

        with self._giraffe.monitor_logs(event_handler=None, directory='.'):
            await asyncio.gather(*tasks)
