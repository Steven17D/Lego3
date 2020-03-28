import sys
import lib
import rpyc
import time
import socket
import random
import asyncio
from contextlib import contextmanager


class ElephantLib(lib.Lib):
    def __init__(self, con):
        super(ElephantLib, self).__init__(con)

    def send_packets(self, *args, **kwargs):
        r_sender = rpyc.async_(self._con.modules['scapy.all'].send)
        return r_sender(*args, **kwargs)

    @contextmanager
    def sniff_packets(self, *args, **kwargs):
        r_sniffer = self._con.modules['scapy.all'].AsyncSniffer(*args, **kwargs)
        r_sniffer.start()
        try:
            yield r_sniffer
        finally:
            r_sniffer.stop()

    async def send_and_recive(self, ip, port, count=5):
        src_port = random.randint(10000, 20000)
        r_IP = self._con.modules['scapy.all'].IP
        r_UDP = self._con.modules['scapy.all'].udp
        packet = r_IP(dst=ip)/r_UDP(sport=src_port, dport=port)/'Lego3 is great'

        with self.sniff_packets(filter=f'udp and src port {port} and dst port {src_port}', count=count) as sniffer:
            self.send_packets(packet, count=count)
            await asyncio.sleep(3)
            assert len(sniffer.join()) != count

