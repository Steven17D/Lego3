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
