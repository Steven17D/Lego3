import rpyc
import socket
import scapy.all

class ZebraLib:

    def __init__(self, con):
        self._con = con

    def send_packets(self, packet, count):
        self._con.modules['scapy.all'].send(packet, count=count)


if __name__ == '__main__':
    con = rpyc.classic.connect('127.0.0.1')

    z = ZebraLib(con)
    z.send_packets('elyash', 5)



        

