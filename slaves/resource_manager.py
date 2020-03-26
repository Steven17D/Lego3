"""
Runs on central server
"""
import rpyc
import contextlib
from typing import List, Tuple, AnyStr, ClassVar


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
        self._allocations = dict()
        self._bg_threads = dict()

    def on_connect(self, conn):
        print(f'Connected: {conn}')
        self._bg_threads[conn] = rpyc.BgServingThread(conn)

    def on_disconnect(self, conn):
        print(f'Disconnected: {conn}')
        del self._bg_threads[conn]

    @contextlib.contextmanager
    def allocation(self, slaves):
        self.allocate(slaves)
        try:
            yield
        finally:
            self.deallocate(slaves)

    def allocate(self, slaves):
        self._allocations[slaves] = True

    def deallocate(self, slaves):
        del self._allocations[slaves]

    def run_query(self, query: str) -> List[Tuple[AnyStr, AnyStr]]:
        # TODO: Run query and return results in allocation
        return [(query, "lib.NetworkElement")]

    def exposed_acquire(self, query):
        return self.allocation(self.run_query(query))
        

if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same ResourceManager
    t = ThreadedServer(ResourceManager(), port=18861)
    t.start()

