"""A library which used as basic API to zebra component"""


import sys
import rpyc
import time
import socket
import asyncio
import watchdog
from contextlib import contextmanager
from watchdog.observers import Observer


# Just for the test
class EventHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event):
        print(event)


class Lib:
    def __init__(self, con):
        self._con = con
        self._bgsrv = rpyc.BgServingThread(self._con)

    def __del__(self):
        self._bgsrv.stop()


class ZebraLib(Lib):
    def __init__(self, con):
        super(ZebraLib, self).__init__(con)

    def send_packets(self, *args, **kwargs):
        sender = rpyc.async_(self._con.modules['scapy.all'].send)
        return sender(*args, **kwargs)

    @contextmanager
    def sniff_packets(self, *args, **kwargs):
        sniffer = self._con.modules['scapy.all'].AsyncSniffer(*args, **kwargs)
        sniffer.start()
        try:
            yield sniffer
        finally:
            sniffer.stop()

    @contextmanager
    def monitor_logs(
            self,
            event_handler: watchdog.events.FileSystemEventHandler,
            files: list
        ):
        observer = self._con.modules['watchdog.observers'].Observer()
        for file in files:
            observer.schedule(event_handler, file)
        observer.start()
        try:
            yield observer
        finally:
            observer.stop()

def main():
    con = rpyc.classic.connect('127.0.0.1')
    z = ZebraLib(con)
    f = open('a.txt', 'w')

    with z.sniff_packets(filter='udp and port 1337'):
        ip = con.modules['scapy.all'].IP
        udp = con.modules['scapy.all'].UDP
        z.send_packets(ip(dst='127.0.0.1')/udp(dport=1338))

    with z.monitor_logs(EventHandler(), ['.']) as observer:
        f.write('Lego 3 will be great')
        f.flush()

    f.close()
    con.close()


if __name__ == '__main__':
    main()
