import lib
import rpyc
import time
import zebra_lib
import giraffe_lib
from scapy.all import *
from contextlib import contextmanager


class TetanusLib:

    def install(giraffe, port):
        """Installs an echo server."""
        
        def echo_packet(packet):
            r_IP = giraffe.con.modules['scapy.all'].IP
            r_UDP = giraffe.con.modules['scapy.all'].UDP
            packet[r_IP].dst, packet[r_IP].src = packet[r_IP].src, packet[r_IP].dst
            packet[r_UDP].dport, packet[r_UDP].sport = packet[r_UDP].sport, packet[r_UDP].dport
            send(packet)

        self._r_sniffer = giraffe.con.modules['scapy.all'].AsyncSnfifer(
            filter=f'udp and port {port}', prn=echo_packet)
        self.r_sniffer.start()

    def uninstall(giraffe):
        self.r_sniffer.stop()

