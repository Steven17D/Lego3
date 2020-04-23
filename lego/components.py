"""
Component object provides the API which tests and libs will use to run code on the component.
"""
from __future__ import annotations
from typing import Tuple, Optional, Type
from types import TracebackType
import abc

import rpyc
from rpyc.utils.zerodeploy import DeployedServer

from .connections import BaseConnection, SSHConnection

_SocketAddress = Tuple[str, int]


class BaseComponent(metaclass=abc.ABCMeta):
    """
    BaseComponent class is the base class of all other components,
    In order to extend the API implement a wrapping component, and to provide more complex functionality
    add appropriate Lib.
    """

    def __init__(self, connection: BaseConnection) -> None:
        """Initiates the connection to remote machine.

        Args:
            connection: Connection to the component.
        """
        self._connection = connection

    def __enter__(self) -> BaseComponent:
        """Allowing the use of 'with' statement with components objects.

        Returns:
            Created class instance.
        """

        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]) -> None:
        """Closes the connection at the exit from the context manager.

        Args:
            exc_type: Exception type.
            exc_value: Exception value.
            traceback: Exception traceback.
        """
        self.close()
        self._connection.close()

    def close(self):
        """Allow subclasses to free resources after finishing tests."""
        pass

    @property
    def connection(self) -> BaseConnection:
        """Connection to the component."""

        return self._connection


class RPyCComponent(BaseComponent):
    """
    Wrapper for RPyC component, a component which we can run python on.
    Provides simple API which is generic for all RPyC connections.
    It has basic functionality which can run cross platform, only assuming we can run python on the component.
    """

    def __init__(self, hostname: str, connection: BaseConnection) -> None:
        """Initiates RPyC connection to SlaveService on remote machine.

        Args:
            hostname: Hostname of remote machine.
            connection: Connection to the component.
        """
        super().__init__(connection)

        try:
            # Checks if the machine already runs RPyC SlaveService.
            self.rpyc = rpyc.classic.connect(hostname, keepalive=True)
        except ConnectionRefusedError:
            if isinstance(connection, SSHConnection):
                # Upload RPyC and start SlaveService in a temporarily directory.
                with DeployedServer(connection.shell) as server:
                    self.rpyc = server.classic_connect()
            else:
                raise

    def close(self) -> None:
        """Closes RPyC connection."""

        self.rpyc.close()
        super().close()

    def getpid(self) -> int:
        """Gets the PID of the service process."""

        return self.rpyc.modules.os.getpid()

    def send_packet(self, addr: _SocketAddress, data: bytes) -> None:
        """Sends an UDP packet.

        Args:
            addr: The address (IP and port) to send the packet to.
            data: The data to send.
        """

        r_socket = self.rpyc.modules['socket']
        remote_socket = r_socket.socket(r_socket.AF_INET, r_socket.R_SOCK_DGRAM)
        remote_socket.sendto(data, addr)
        remote_socket.close()

    def run_command(self, command: str) -> str:
        """Runs a bash command on the remote machine.

        Args:
            command: The bash command to run.

        Returns:
            The output of the command.
        """

        return self.rpyc.modules["subprocess"].check_output(command.split())

    def get_ip(self) -> str:
        """Gets the IP of the remote machine."""

        hostname = self.rpyc.modules['socket'].gethostname()
        return self.rpyc.modules['socket'].gethostbyname(hostname)
