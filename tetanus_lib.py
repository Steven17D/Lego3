import lib
import rpyc
import time
import zebra_lib
from scapy.all import *
from contextlib import contextmanager


class TetanusLib:
    def __init__(self, zebra_lib, giraffe_libs):
        self._zebra_lib = zebra_lib
        self._giraffe_libs = giraffe_libs

    @contextmanager
    def run_echo_server(self):
        def echo_packet(packet):
            print(packet)
            udp = self._zebra_lib._con.modules['scapy.all'].UDP
            packet[udp].sport, packet[udp].dport = packet[udp].dport, packet[udp].sport
            #self._zebra_lib.send_packets(packet)
        with self._zebra_lib.sniff_packets(filter='udp and port 1337', prn=echo_packet):
                yield


if __name__ == '__main__':
    c = rpyc.classic.connect('127.0.0.1')
    t = TetanusLib(zebra_lib.ZebraLib(c), None)

    with t.run_echo_server():
        time.sleep(100)

