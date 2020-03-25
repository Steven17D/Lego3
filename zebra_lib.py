import sys
import rpyc
import time
import socket
import asyncio
import watchdog
from watchdog.observers import Observer
from scapy.all import *
from contextlib import contextmanager


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
        send = rpyc.async_(self._con.modules['scapy.all'].send)
        return send(*args, **kwargs)

    @contextmanager
    def sniff_packets(self, *args, **kwargs):
        sniffer = self._con.modules['scapy.all'].AsyncSniffer(*args, **kwargs)
        sniffer.start()
        try:
            yield sniffer
        finally:
            print(sniffer.stop())

    @contextmanager
    def monitor_logs(self, files: list):
        observer = self._con.modules['watchdog.observers'].Observer()
        for file in files:
            observer.schedule(EventHandler(), file)
        observer.start()

        try:
            yield observer
        finally:
            observer.stop()


def main():
    con = rpyc.classic.connect('127.0.0.1')
    con.modules.sys.stdout = sys.stdout
    z = ZebraLib(con)
    f = open('a.txt', 'w')

    with z.sniff_packets(filter='udp and port 1337') as sniffer:
        z.send_packets(IP(dst='127.0.0.1')/UDP(dport=1337))

    with z.monitor_logs(['.']) as observer:
        f.write('Lego 3 will be great')
        f.flush()

    f.close()
    con.close()


if __name__ == '__main__':
    main()
