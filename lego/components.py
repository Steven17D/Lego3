"""
Component object provides the API which tests and libs will use to run code on the component.
"""
from __future__ import annotations
from typing import Tuple, Optional, Type
from types import TracebackType
import abc

from .connections import BaseConnection, RPyCConnection

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

        self._connection.close()

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

    def __init__(self, connection: RPyCConnection) -> None:
        """Initiates the connection to remote machine.

        Args:
            connection: RPyC SlaveService connection to the component.
        """
        super().__init__(connection)

        self._rpyc = self.connection.rpyc_connection

    def getpid(self) -> int:
        """Gets the PID of the service process."""

        return self._rpyc.modules.os.getpid()

    def send_packet(self, addr: _SocketAddress, data: bytes) -> None:
        """Sends an UDP packet.

        Args:
            addr: The address (IP and port) to send the packet to.
            data: The data to send.
        """

        r_socket = self._rpyc.modules['socket']
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

        return self._rpyc.modules["subprocess"].check_output(command.split())

    def get_ip(self) -> str:
        """Gets the IP of the remote machine."""

        hostname = self._rpyc.modules['socket'].gethostname()
        return self._rpyc.modules['socket'].gethostbyname(hostname)
