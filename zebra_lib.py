"""A library which used as basic API to zebra component"""


import sys
import rpyc
import time
import socket
import asyncio
import watchdog
from contextlib import contextmanager
from watchdog.observers import Observer
from core_lib import CoreLib


# Just for the test
class EventHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event):
        print(event)


class ZebraLib(CoreLib):
    def send_packets(self, *args, **kwargs):
        r_sender = rpyc.async_(self._conn.modules['scapy.all'].send)
        return r_sender(*args, **kwargs)

    @contextmanager
    def sniff_packets(self, *args, **kwargs):
        r_sniffer = self._conn.modules['scapy.all'].AsyncSniffer(*args, **kwargs)
        r_sniffer.start()
        try:
            yield r_sniffer
        finally:
            r_sniffer.stop()

    @contextmanager
    def monitor_logs(
            self,
            event_handler: watchdog.events.FileSystemEventHandler,
            files: list
        ):
        r_observer = self._conn.modules['watchdog.observers'].Observer()
        for file in files:
            r_observer.schedule(event_handler, file)
        r_observer.start()
        try:
            yield r_observer
        finally:
            r_observer.stop()

def main():
    con = rpyc.classic.connect('127.0.0.1')
    bgsrv = rpyc.BgServingThread(con)
    with ZebraLib(con) as z, open('a.txt', 'w') as f:
        with z.sniff_packets(filter='udp and port 1337'):
            r_ip = con.modules['scapy.all'].IP
            r_udp = con.modules['scapy.all'].UDP
            z.send_packets(r_ip(dst='127.0.0.1')/r_udp(dport=1338))

        with z.monitor_logs(EventHandler(), ['.']):
            f.write('Lego 3 will be great')
            f.flush()

        f.close()
        bgsrv.stop()
        con.close()


if __name__ == '__main__':
    main()
