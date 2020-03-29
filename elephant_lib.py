"""Elephant lib is API to elephant component."""

import sys
import rpyc
import time
import socket
import random
import asyncio
from contextlib import contextmanager

import core_lib


class ElephantLib(core_lib.CoreLib):
    """An extended library for Elephant component."""

    def __init__(self, con):
        super(ElephantLib, self).__init__(con)

    async def send_and_recive(self, ip: str, port: int, count: int=5):
        """Sends packets and receive them back.

        Args:
            ip: The IP to send to and receive from.
            port: The port to send to and receive from.
            count: The number of packets to send.
        """

        src_port = random.randint(10000, 20000)
        r_IP = self._con.modules['scapy.all'].IP
        r_UDP = self._con.modules['scapy.all'].udp
        packet = r_IP(dst=ip)/r_UDP(sport=src_port, dport=port)/'Lego3 is great'
        r_send = self._con.modules['scapy.all'].send
        r_sniffer = self._con.modules['scapy.all'].AsyncSniffer(
            filter=f'udp and src port {port} and dst port {src_port}', count=count)

        r_sniffer.start()
        r_send(packet, count=count)
        await asyncio.sleep(3)
        packets = r_sniffer.stop()
        assert len(packets) == count
