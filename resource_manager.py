"""
Runs on dv-samech
"""
import rpyc
import time
import collections

from helpers import Client, Test, Setup


class ResourceManager(rpyc.Service):
    """
    Setup and tests manager.
    Should manage the permissions for tests to run on setup.
    Stores its database using Rest API.
    """
    __slots__ = ("_allocations", "_bg_threads")
    ALIASES = ["ResourceManager"]

    def __init__(self, *args, **kwargs):
        super(ResourceManager, self).__init__(*args, **kwargs)
        self._allocations = collections.defaultdict(bool)
        self._bg_threads = dict()

    def on_connect(self, conn):
        print(f'Connected: {conn}')
        self._bg_threads[conn] = rpyc.BgServingThread(conn)

    def on_disconnect(self, conn):
        print(f'Disconnected: {conn}')
        del self._bg_threads[conn]

    def exposed_request_setup(self, client: Client, test: Test, setup: Setup) -> bool:
        # Note: remember to delete the connection from the queue if there is no response.
        print("register the request and its details in registered_to_run queue")
        print("Calculate if the requested setup available")
        # self._allocations
        # Return whether the requested setup available
        return False

    def exposed_get_wait_info(self):
        # By the connection_id return the info about the test ahead of
        # this test.

        return ['TestSingleUDP', 'TestSingleTCP', 'TestMultipleTCP']

    def exposed_notify_me(self):
        # Register this test (by connection) to the waiting_to_run queue and
        # notify the test when its requested setup is ready for it.

        time.sleep(2)
        return
        

if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same ResourceManager
    t = ThreadedServer(ResourceManager(), port=18861)
    t.start()

