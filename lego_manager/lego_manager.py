"""
Runs on central server
"""
from typing import List, Dict, Tuple, Iterator

import contextlib
import rpyc


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
            connections: List[Tuple[str, str]],
            exclusive: bool
        ) -> Iterator[List[Tuple[str, str]]]:
        """Manages the components allocations.

        Args:
            connections: Required components.
            exclusive: Whether to lock the required setup.

        Yields:
            Required components.
        """

        del exclusive # TODO: Add this functionality.

        self._allocate(connections)
        try:
            yield connections
        finally:
            self._deallocate(connections)

    def _allocate(self, connections: List[Tuple[str, str]]) -> None:
        """Allocates the desired components if available.

        Args:
            connections: Desired components.
        """

        for connection in connections:
            self._allocations[connection] = True


    def _deallocate(self, connections: List[Tuple[str, str]]) -> None:
        """Deallocates the desired components.

        Args:
            connections: Unneeded components.
        """

        for connection in connections:
            del self._allocations[connection]

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
            'zebra': 'Lego3.example.components.zebra.Zebra',
            'giraffe': 'Lego3.example.components.giraffe.Giraffe',
            'elephant': 'Lego3.example.components.elephant.Elephant'
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


def main() -> None:
    """Starts Lego server."""

    rpyc.lib.setup_logger()
    from rpyc.utils.server import ThreadedServer # pylint: disable=import-outside-toplevel
    # Note: all connection will use the same LegoManager
    lego_server = ThreadedServer(LegoManager(), port=18861)
    lego_server.start()

if __name__ == "__main__":
    main()
