"""
Runs on dv-samech
"""
import rpyc
import contextlib
from lib import Heart


def setup_factory(hostname):
    return {
        "127.0.0.1": Heart,
    }[hostname](rpyc.classic.connect(hostname))


class SlaveManager(rpyc.Service):
    """
    Setup and agents manager.
    When a test starts to start, it asks this agent for setup.
    As respose (if the setup available), this agent returns the relevant agents.
    """
    ALIASES = ["SlaveManager"]

    @contextlib.contextmanager
    def allocation(self, setup):
        print "Allocated", setup
        # self._allocation.append(setup)
        try:
            yield setup
        finally:
            print "Deallocated", setup
            # self._allocation.remove(setup)

    def on_connect(self, conn):
        self._setup = {'A': (1,2,3), 'B': (1,2,)}
        print "Connected", conn

    def on_disconnect(self, conn):
        print "Disconnected", conn

    def get_setup(self, requested_setup):
	"""
	Gets ["127.0.0.1"]
	Return [ContextManager<Heart(rpyc.connetion<"127.0.0.1">)>]
	"""
        return self.allocation({setup: setup_factory(setup) for setup in requested_setup})


if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same SlaveManager
    t = ThreadedServer(SlaveManager(), port=18861, protocol_config={'allow_public_attrs': True})
    t.start()

