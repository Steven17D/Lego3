"""
Connections provides the RPyC connection to the component.
Each connection should be based on different protocol, e.g. SSH or telnet.
"""
import plumbum
import rpyc
from rpyc.utils.zerodeploy import DeployedServer


class BaseConnection:
    """
    Wrapper for RPyC connection.
    According to different protocols, RPyC SlaveService will be deployed or connected
    differently on the remote machines.
    """
    @property
    def rpyc_connection(self) -> rpyc.core.protocol.Connection:
        """The RPyc Connection component."""
        raise NotImplementedError()

    def close(self) -> None:
        """Closes all connections."""
        raise NotImplementedError()


class SSHConnection(BaseConnection):
    """SSH wrapper for RPyC connection.

    SSH connection to remote machine, provide the connection to remote RPyC SlaveService.
    In case the machine doesn't already run SlaveService, it will be uploaded and run in a temporarily directory.

    Typical usage will be to start the connection in your component's __init__ and
    pass the created object to BaseComponent.
    """

    DEFAULT_USERNAME = "root"
    DEFAULT_PASSWORD = "password"

    def __init__(self, hostname: str, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD) -> None:
        """Initiates SSH connection, and connects (and start if needed) to RPyC remote SlaveService.

        Args:
            hostname: The hostname of the component we want to connect to.
            username: Username for SSH connection.
            password: Password for SSH connection.
        """

        # TODO: check why initializing machine doesn't work.
        # self._machine = plumbum.SshMachine(hostname, username, password)
        self._server = None
        self._machine = None

        try:
            # Checks if machine already runs RPyC SlaveService.
            self._conn = rpyc.classic.connect(hostname, keepalive=True)
        except ConnectionRefusedError:
            self._machine = plumbum.SshMachine(hostname, username, password)
            # Upload RPyC and start SlaveService in a temporarily directory.
            self._server = DeployedServer(self._machine)
            self._conn = self._server.classic_connect()

    @property
    def rpyc_connection(self) -> rpyc.core.protocol.Connection:
        """The RPyc Connection component."""

        return self._conn

    def close(self) -> None:
        """Closes SSH and RPyC connections."""

        self._conn.close()

        if self._server is not None:
            self._server.close()

        # TODO: remove if statement after solving above TODO (check why plumbum.SshMachine doesn't work).
        if self._machine is not None:
            self._machine.close()


class TelnetConnection(BaseConnection):
    # TODO: Add telnet connection that will support RPyC.
    pass
