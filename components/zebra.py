"""Zebra lib is API to Zebra component."""

import asyncio
import functools
import random
import rpyc

import components.core


class Zebra(components.core.Core):
    """An extended library for Zebra component."""

    async def send_and_receive(self, dst_ip: str, dst_port: int, count: int = 5):
        """Sends packets and receive them back.

        Args:
            dst_ip: The IP to send to and receive from.
            dst_port: The port to send to and receive from.
            count: The number of packets to send.
        """

        executor = None
        received_index = 1
        payload = 'Lego3 is great'
        src_port = random.randint(10000, 20000)

        packet = (
            self.connection.modules['scapy.all'].IP(dst=dst_ip) /
            self.connection.modules['scapy.all'].UDP(sport=src_port, dport=dst_port)/
            self.connection.modules['scapy.all'].Raw(load=payload)
        )

        r_srloop = self.connection.modules['scapy.all'].srloop
        partial_r_srloop = functools.partial(r_srloop, packet,
                filter=f'udp and dst port {src_port}', timeout=1, count=count)

        loop = asyncio.get_running_loop()
        answered, unanswered = await loop.run_in_executor(executor, partial_r_srloop)

        assert len(answered) == count
        assert len(unanswered) == 0
        for i in range(count):
            assert answered[i][received_index].load.decode() == payload
