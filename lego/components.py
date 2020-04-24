"""
Component object provides the API which tests and libs will use to run code on the component.
"""
from __future__ import annotations
from typing import Optional, Type
from types import TracebackType
import abc
import socket

import rpyc
from rpyc.utils.zerodeploy import DeployedServer

from .connections import BaseConnection, SSHConnection


class BaseComponent(metaclass=abc.ABCMeta):
    """
    BaseComponent class is the base class of all other components,
    In order to extend the API implement a wrapping component, and to provide more
    complex functionality add appropriate Lib.
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

    @property
    def connection(self) -> BaseConnection:
        """Connection to the component."""

        return self._connection


class RPyCComponent(BaseComponent):
    """
    Wrapper for RPyC component, a component which we can run python on.
    Provides simple API which is generic for all RPyC connections.
    It has basic functionality which can run cross platform, only assuming we can run
    python on the component.
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

    def get_remote_socket(self, *args: int, **kwargs: int) -> socket.socket:
        """Allocates a socket on remote machine.

        Args:
            args: Positional arguments passed to socket.socket() constructor.
            kwargs: Keyword arguments passed to socket.socket() constructor.
        """

        r_socket = self.rpyc.modules['socket']
        return r_socket.socket(*args, **kwargs)

    def run_command(self, command: str) -> str:
        """Runs a bash command on the remote machine.

        Args:
            command: The bash command to run.

        Returns:
            The output of the command.
        """

        return self.rpyc.modules["subprocess"].check_output(command.split())

    def get_ip(self) -> str:
        """Gets IP for default route interface of the remote machine."""

        r_socket = self.get_remote_socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't have to be reachable.
            r_socket.connect(('10.255.255.255', 1))
            component_ip = r_socket.getsockname()[0]
        except socket.error:
            # Can't find default route, use localhost interface.
            component_ip = '127.0.0.1'
        finally:
            r_socket.close()

        return component_ip
