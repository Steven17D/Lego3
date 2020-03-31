"""Elephant lib is API to elephant component."""

import asyncio
import random
import rpyc

import components.core


class Elephant(components.core.Core):
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
        packet = (
            self.connection.modules['scapy.all'].IP(dst=dst_ip) /
            self.connection.modules['scapy.all'].UDP(sport=src_port, dport=dst_port)/
            self.connection.modules['scapy.all'].Raw(load=payload)
        )
        r_srloop = rpyc.async_(self.connection.modules['scapy.all'].srloop)

        packets = r_srloop(packet, filter=f'udp and dst port {src_port}', timeout=2, count=count)

        await asyncio.sleep(0)

        answered, unanswered = packets.value

        assert len(answered) == count
        assert len(unanswered) == 0
        for i in range(count):
            assert answered[i][1].load.decode() == payload
