"""Elephant lib is API to elephant component."""

import random
import asyncio

import libs.core_lib


class ElephantLib(libs.core_lib.CoreLib):
    """An extended library for Elephant component."""

    async def send_and_receive(self, dst_ip: str, dst_port: int, count: int = 5):
        """Sends packets and receive them back.

        Args:
            dst_ip: The IP to send to and receive from.
            dst_port: The port to send to and receive from.
            count: The number of packets to send.
        """

        payload = 'Lego3 is great'
        src_port = random.randint(10000, 20000)
        R_Raw = self.connection.modules['scapy.all'].Raw
        packet = (
            self.connection.modules['scapy.all'].IP(dst=dst_ip) /
            self.connection.modules['scapy.all'].UDP(sport=src_port, dport=dst_port)/
            payload
        )
        r_sr = self.connection.modules['scapy.all'].sr

        packets, _ = r_sr([packet] * count)

        assert len(packets) == count
        for _, response in packets:
            assert response[R_Raw].load.decode() == payload

