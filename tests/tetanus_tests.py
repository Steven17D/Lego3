"""Tetanus spec tests."""

import pytest
import asyncio

import libs.tetanus_lib

pytest_plugins = 'lego.pytest_lego.plugin'


class TestsSpecTetanus:
    """A Tetanus spec tests."""

    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._tetanus_lib = libs.tetanus_lib.TetanusLib()
        cls._giraffe = slaves['giraffe']
        cls._echo_port = 1337

    def setup_method(self):
        self._tetanus_lib.install(self._giraffe, self._echo_port)

    def teardown_method(self):
        self._tetanus_lib.uninstall()

    @pytest.mark.lego('zebra')
    async def test_send_and_recv(self, slaves):
        await slaves['zebra'].send_and_recive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_send_and_recv(self, slaves):
        asyncio.gather(await slave.send_and_recive(self._giraffe.get_ip(), self._echo_port)
                       for slave in (slaves['zebra'], slaves['elephant']))

    @pytest.mark.lego('zebra')
    async def test_monitor_send_and_recv(self, slaves):
        with self._giraffe.monitor_logs(giraffe_lib.EventHandler(), '.'):
            await slaves['zebra'].send_and_recive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    async def test_multi_monitor_send_and_receive(self, slaves):
        with self._giraffe.monitor_logs(giraffe_lib.EventHandler(), '.'):
            asyncio.gather(await slave.send_and_recive(self._giraffe.get_ip(), self._echo_port)
                           for slave in (slaves['zebra'], slaves['elephant']))
