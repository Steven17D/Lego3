"""
Runs on central server
"""
from typing import List, Dict, Tuple, Iterator

import contextlib
import rpyc

import components.core


class LegoManager(rpyc.Service):
    """
    Setup and tests manager.
    Should manage the permissions for tests to run on setup.
    Stores its database using Rest API.
    """
    __slots__ = ("_allocations", "_bg_threads")
    ALIASES = ["LegoManager"]

    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        self._allocations: Dict = dict()
        self._bg_threads: Dict = dict()

    def on_connect(self, conn: rpyc.Connection) -> None:
        """Initializes thread for the incoming connection.

        Args:
            conn: An incoming connection.
        """

        self._bg_threads[conn] = rpyc.BgServingThread(conn)

    def on_disconnect(self, conn: rpyc.Connection) -> None:
        """Stops the connection's thread.

        Args:
            conn: A disconnected connection.
        """

        self._bg_threads.pop(conn).stop()

    @contextlib.contextmanager
    def _allocation(
            self,
            _components: List[components.core.Core],
            exclusive: bool
        ) -> Iterator[List[components.core.Core]]:
        """Manages the components allocations.

        Args:
            _components: Required components.
            exclusive: Whether to lock the required setup.

        Yields:
            Required components.
        """

        del exclusive # TODO: Add this functionality.

        self._allocate(_components)
        try:
            yield _components
        finally:
            self._deallocate(_components)

    def _allocate(self, _components: List[components.core.Core]) -> None:
        """Allocates the desired components if available.

        Args:
            _components: Desired components.
        """

        for component in _components:
            self._allocations[component] = True

    def _deallocate(self, _components: List[components.core.Core]) -> None:
        """Deallocates the desired components.

        Args:
            _components: Unneeded components.
        """

        for component in _components:
            del self._allocations[component]

    @staticmethod
    def _run_query(query: str) -> List[Tuple[str, str]]:
        """Runs the requested setup query on the setup management files
        and returns the available components libs and hostnames.

        Args:
            query: A query describes the desired setup.

        Returns:
            Desired hostnames and libraries.
        """
        # TODO: Run query and return results in allocation

        hostname_to_lib = {
            'zebra': 'example.components.zebra.Zebra',
            'giraffe': 'example.components.giraffe.Giraffe',
            'elephant': 'example.components.elephant.Elephant'
        }
        hostnames = (hostname.strip() for hostname in query.split('and'))

        return [(hostname, hostname_to_lib[hostname]) for hostname in hostnames]

    def exposed_acquire(self, query: str, exclusive: bool): # type: ignore
        """Acquired the desired setup if available.

        This function also will store all of the data about the setup usage.

        Args:
            query: A query describes the desired setup.
            exclusive: Weather the required setup needed exclusivly.

        Returns:
            Allocated requested setup as list of hostnames and libraries.
        """

        return self._allocation(LegoManager._run_query(query), exclusive)


if __name__ == "__main__":
    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer
    # Note: all connection will use the same LegoManager
    lego_server = ThreadedServer(LegoManager(), port=18861)
    lego_server.start()
