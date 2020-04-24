"""Zebra component is the API to Zebra component."""

import asyncio
import functools
import random

from Lego3.lego.components import RPyCComponent
from Lego3.lego.connections import SSHConnection


class Zebra(RPyCComponent):
    """An extended interface for Zebra component."""

    def __init__(self, hostname: str, username: str, password: str) -> None:
        """Initialize RPyC connection over SSH.

        Args:
            hostname: Hostname of the component.
            username: Username for SSH login.
            password: Password for SSH login.
        """
        self.ssh = SSHConnection(hostname, username, password)
        super().__init__(hostname, self.ssh)

    async def send_and_receive(
            self,
            dst_ip: str,
            dst_port: int,
            count: int = 5
    ) -> None:
        """Sends packets and receive them back.

        Args:
            dst_ip: The IP to send to and receive from.
            dst_port: The port to send to and receive from.
            count (optional): The number of packets to send. Defaults to 5.
        """

        executor = None
        received_index = 1
        payload = 'Lego3 is great'
        src_port = random.randint(10000, 20000)

        packet = (
            self.rpyc.modules['scapy.all'].IP(dst=dst_ip) /
            self.rpyc.modules['scapy.all'].UDP(sport=src_port, dport=dst_port)/
            self.rpyc.modules['scapy.all'].Raw(load=payload)
        )

        r_srloop = self.rpyc.modules['scapy.all'].srloop
        partial_r_srloop = functools.partial(
            r_srloop, packet, filter=f'udp and dst port {src_port}', timeout=1, count=count)

        loop = asyncio.get_running_loop()
        answered, unanswered = await loop.run_in_executor(executor, partial_r_srloop)

        assert len(answered) == count
        assert len(unanswered) == 0
        for i in range(count):
            assert answered[i][received_index].load.decode() == payload
