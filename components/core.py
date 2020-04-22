"""
Component object provides the API which tests and libs will use to run code on the component.
Core class is the base class of all the components, and in this class the RPyC connection will be initiated.
"""
from __future__ import annotations
from typing import Tuple, Optional, Type
from types import TracebackType

import rpyc

from .connections import BaseConnection


class Core:
    """
    Wrapper for RPyC connection.
    Provides simple API which is generic for all RPyC connections.
    In order to extend the API implement a wrapping Lib.
    """

    def __init__(self, connection: BaseConnection) -> None:
        """Initiates the connection to remote machine.

        Args:
            connection: The connection to the component.
        """
        self._remote_connection = connection
        self._rpyc = self._remote_connection.rpyc_connection

    def __enter__(self) -> Core:
        """Enabling context manager in this class.

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

        self._remote_connection.close()

    @property
    def connection(self) -> rpyc.core.protocol.Connection:
        """RPyc connection to the component."""

        return self._rpyc

    def getpid(self) -> int:
        """Gets the PID of the service process."""

        return self._rpyc.modules.os.getpid()

    def send_packet(self, addr: Tuple[str, int], data: bytes) -> None:
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
