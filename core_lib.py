"""A core library moudle."""
import rpyc


class CoreLib:
    """Core Library to wrap slave connection."""

    def __init__(self, con: rpyc.core.protocol.Connection):
        self._con = con

    @property
    def con(self) -> rpyc.core.protocol.Connection:
        """Gets the lib RPyC connection."""
        return self._con

    def get_ip(self) -> str:
        """Gets the IP of the component the slave running on."""

        hostname = self._con.modules['socket'].gethostname()
        return self._con.modules['socket'].gethostbyname(hostname)
