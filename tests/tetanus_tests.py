"""Tetanus spec tests."""

import pytest
import asyncio

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
        zebra, *_ = slaves
        zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_send_and_recv(self, slaves):
        zebra, elephant, *_ = slaves
        for slave in (zebra, elephant):
                slave.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra')
    async def test_monitor_send_and_recv(self, slaves):
        zebra, *_ = slaves
        with self._giraffe.monitor_logs(None, '.'):
            zebra.send_and_receive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_monitor_send_and_receive(self, slaves):
        zebra, elephant, *_ = slaves
        with self._giraffe.monitor_logs(None, '.'):
            for slave in (zebra, elephant):
                slave.send_and_receive(self._giraffe.get_ip(), self._echo_port)
