"""
Runs on dv-samech
"""
import rpyc
import contextlib
import collections
from lib import Heart


class ResourceManager(rpyc.Service):
    """
    Setup and agents manager.
    When a test starts to start, it asks this agent for setup.
    """
    ALIASES = ["ResourceManager"]

    def __init__(self, *args, **kwargs):
        super(ResourceManager, self).__init__(*args, **kwargs)
        self._allocations = collections.defaultdict(bool)

    def on_connect(self, conn):
        print "Connected", conn

    def on_disconnect(self, conn):
        print "Disconnected", conn

    def get_setup(self, requested_setup):
	"""
	Gets ["127.0.0.1"]
	Return [ContextManager<Heart(rpyc.connetion<"127.0.0.1">)>]
	"""
        return self.allocation(requested_setup)

    @contextlib.contextmanager
    def allocation(self, setup):
        for s in setup:
            assert self._allocations[s]
            self._allocations.remove(s)

        print "Allocated", setup
        # TODO: Require setup with soft/hard policy
        try:
            yield
        finally:
            print "Deallocated", setup
            for connection in setup.itervalues():
                connection._conn.close()
            # self._allocation.remove(setup)



if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same ResourceManager
    t = ThreadedServer(ResourceManager(), port=18861, protocol_config={'allow_public_attrs': True})
    t.start()

