"""Tetanus spec tests."""

import asyncio
import pytest

import libs.giraffe_lib
import libs.tetanus_lib

pytest_plugins = 'lego.pytest_lego.plugin'

TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/cat"'
BUGY_LOGS_TOOL = TOOL + ' --output log.txt'
BUGY_SEND_TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/echo lego"'


class TestsSpecTetanus:
    """A Tetanus spec tests."""

    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._giraffe, *_ = slaves
        cls._tetanus_lib = libs.tetanus_lib.TetanusLib()
        cls._echo_port = 1337

    def setup_method(self):
        self._tetanus_lib.install(self._giraffe, TOOL, self._echo_port)

    def teardown_method(self):
        self._tetanus_lib.uninstall(self._giraffe)

    @pytest.mark.lego('zebra')
    async def test_send_and_recv(self, slaves):
        "The test send packets and expect them back."""

        zebra, *_ = slaves
        await zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_send_and_recv(self, slaves):
        """The test send packets from multiple components and
            expect them back.
        """

        tasks = []

        for slave in slaves:
            tasks.append(asyncio.ensure_future(
                slave.send_and_receive(self._giraffe.get_ip(), self._echo_port)))

        await asyncio.wait(tasks)

    @pytest.mark.lego('zebra')
    async def test_monitor_send_and_recv(self, slaves):
        """The test send packets and expect them back while validating no bad
            logs written.
        """

        zebra, *_ = slaves
        with self._giraffe.monitor_logs(None, '.'):
            await zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_monitor_send_and_receive(self, slaves):
        """The test send packets from multiple components and
            expect them back, while validating no bad logs written.
        """

        tasks = []

        for slave in slaves:
            tasks.append(asyncio.ensure_future(
                slave.send_and_receive(self._giraffe.get_ip(), self._echo_port)))

        with self._giraffe.monitor_logs(None, '.'):
            await asyncio.wait(tasks)
