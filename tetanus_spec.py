import pytest
import asyncio
import tetanus_lib
import giraffe_lib

class TetanusTestsSpec:

    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        self._tetanus_lib = tetanus_lib.TetanusLib()
        self._giraffe = slaves['giraffe']
        self._echo_port = 1337

    def setup_method(self):
        self._tetanus_lib.install(self._giraffe, self._echo_port)

    def teardown_method(self):
        self._tetanus_lib.uninstall()

    @pytest.mark.lego('zebra')
    def test_send_and_recv(self, slaves):
        slaves['zebra'].send_and_recive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    def test_multi_send_and_recv(self, slaves):
        asyncio.gather(slave.send_and_recive(self._giraffe.get_ip(), self._echo_port)
            for slave in (slaves['zebra'], slaves['elephant']))

    @pytest.mark.lego('zebra')
    def test_monitor_send_and_recv(self, slaves):
        with self._giraffe.monitor_logs(giraffe_lib.EventHandler(), '.'):
            slaves['zebra'].send_and_recive(self._giraffe.get_ip(), self._echo_port)

    @pytest.mark.lego('zebra and elephant')
    def test_multi_monitor_send_and_receive(self, slaves):
        with self._giraffe.monitor_logs(giraffe_lib.EventHandler(), '.'):
            asyncio.gather(slave.send_and_recive(self._giraffe.get_ip(), self._echo_port)
            for slave in (slaves['zebra'], slaves['elephant']))



