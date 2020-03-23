"""
Runs on dv-samech
"""
import rpyc
import contextlib
import collections
from lib import Heart


class ResourceManager(rpyc.Service):
    """
    Setup and tests manager.
    Should manage the permissions for tests to run on setup.
    Stores its database using Rest API.
    """
    ALIASES = ["ResourceManager"]

    def __init__(self, *args, **kwargs):
        super(ResourceManager, self).__init__(*args, **kwargs)
        self._allocations = collections.defaultdict(bool)

    def on_connect(self, conn):
        print "Connected", conn

    def on_disconnect(self, conn):
        print "Disconnected", conn

    def exposed_request_setup(client: Client, test: Test, setup: Setup) ->
    bool:
        # Note: remember to delete the connection from the queue if there
        # is no response.
        print("register the request and its details in registered_to_run
                queue")

        print("Calculate if the requested setup available")
        
        # Return whether the requested setup available
        return True

    def exposed_get_waiting_tests_info() 
        # By the connection_id return the info about the test ahead of
        # this test.

        pass

    def exposed_notity_to_run()
        # Register this test (by connection) to the waiting_to_run queue and
        # notiry the test when its requested setup is ready for it.
        
        pass


if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same ResourceManager
    t = ThreadedServer(ResourceManager(), port=18861)
    t.start()

