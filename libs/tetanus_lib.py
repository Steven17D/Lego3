"""Library for Tetanus functionality."""

import scapy

import libs.giraffe_lib

class TetanusLib:
    """Library for Tetanus functionality."""

    def __init__(self):
        self._r_sniffer = None

    def install(self, giraffe: libs.giraffe_lib.GiraffeLib, port: int):
        """Installs an echo server.

        Args:
            giraffe: Component API to install on.
            port: Port to echo on.
        """

        def echo_packet(packet: scapy.layers.inet.IP):
            """Echo the recive packet back.

            Args:
                packet: The received packet.
            """

            r_ip = giraffe.con.modules['scapy.all'].IP
            r_udp = giraffe.con.modules['scapy.all'].UDP
            packet[r_ip].dst, packet[r_ip].src = packet[r_ip].src, packet[r_ip].dst
            packet[r_udp].dport, packet[r_udp].sport = packet[r_udp].sport, packet[r_udp].dport
            giraffe.con.modules['scapy.all'].send(packet)

        self._r_sniffer = giraffe.con.modules['scapy.all'].AsyncSnfifer(
            filter=f'udp and port {port}', prn=echo_packet)
        self._r_sniffer.start()

    def uninstall(self):
        """Uninstall the echo server."""

        self._r_sniffer.stop()
