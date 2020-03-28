import lego
import pytest
import asyncio
import contextlib
import functools


class TetanusTestsSpec:

    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        self._giraffe = slaves['giraffe']

    def setup_method(self):
        self._giraffe.run_echo_server()

    def teardown_method(self):
        self._giraffe.stop_echo_server()

    @pytest.mark.lego('zebra')
    def test_send_and_recv(self, slaves):
        slaves['zebra'].send_and_recive()

    @pytest.mark.lego('4 zebra')
    def test_multi_send_and_recv(self, slaves):
        asyncio.gather(slave.send_and_recive() for hostname, slave in slaves if hostname.startswith('zebra'))

    @pytest.mark.lego('zebra')
    def test_monitor_send_and_recv(self, slaves):
        with self._giraffe.monitor_logs():
            slaves['zebra'].send_and_recive()

    @pytest.mark.lego('4 zebra')
    def test_multi_monitor_send_and_receive(self, slaves):
        with self._giraffe.monitor_logs():
            asyncio.gather(slave.send_and_recive() for hostname, slave in slaves if hostname.startswith('zebra')


