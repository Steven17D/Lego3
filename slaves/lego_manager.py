"""
Runs on central server
"""
import rpyc
import contextlib
from typing import List, Tuple, AnyStr, ClassVar


class LegoManager(rpyc.Service):
    """
    Setup and tests manager.
    Should manage the permissions for tests to run on setup.
    Stores its database using Rest API.
    """
    __slots__ = ("_allocations", "_bg_threads")
    ALIASES = ["LegoManager"]

    def __init__(self, *args, **kwargs):
        super(LegoManager, self).__init__(*args, **kwargs)
        self._allocations = dict()
        self._bg_threads = dict()

    def on_connect(self, conn):
        self._bg_threads[conn] = rpyc.BgServingThread(conn)

    def on_disconnect(self, conn):
        self._bg_threads.pop(conn).stop()
        
    @contextlib.contextmanager
    def allocation(self, slaves):
        self.allocate(slaves)
        try:
            yield slaves
        finally:
            self.deallocate(slaves)

    def allocate(self, slaves):
        for slave in slaves:
            self._allocations[slave] = True

    def deallocate(self, slaves):
        for slave in slaves:
            del self._allocations[slave]

    def run_query(self, query: str) -> List[Tuple[AnyStr, AnyStr]]:
        # TODO: Run query and return results in allocation
        return [(query, "lib.CoreLib")]

    def exposed_acquire(self, query, exclusive):
        return self.allocation(self.run_query(query))
        

if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same LegoManager
    t = ThreadedServer(LegoManager(), port=18861)
    t.start()

