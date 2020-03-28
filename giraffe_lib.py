import sys
import lib
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


class GiraffeLib(lib.Lib):
    def __init__(self, con):
        super(GiraffeLib, self).__init__(con)

    @contextmanager
    def monitor_logs(
            self,
            event_handler: watchdog.events.FileSystemEventHandler,
            files: list
        ):
        r_observer = self._con.modules['watchdog.observers'].Observer()
        for file in files:
            r_observer.schedule(event_handler, file)
        r_observer.start()
        try:
            yield r_observer
        finally:
            r_observer.stop()

    def get_ip(self):
        r_hostname = self._con.modules['socket'].gethostname()
        return self._con.modules['socket'].gethostbyname(r_hostname)
