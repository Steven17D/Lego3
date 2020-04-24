"""
Connections provides the connection to the components. A connection should provide simple functionality to
the component, such as running a shell command or upload a file.
Each connection should be based on different protocol, e.g. SSH or telnet.
"""
from __future__ import annotations
from typing import Optional, Type
from types import TracebackType
import abc

import plumbum


class BaseConnection(metaclass=abc.ABCMeta):
    """
    BaseConnection class is the base class of every connection to any type of components.
    A connection should provide simple API to communicate and control the component.
    """

    def __enter__(self) -> BaseConnection:
        """Allowing the use of 'with' statement with connections objects.

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

    @abc.abstractmethod
    def close(self) -> None:
        """Closes all connections."""
        pass


class SSHConnection(BaseConnection):
    """SSH connection for remote machine.

    This connection provides a shell, that can be used to run shell commands and upload or download files.

    Usage example:
    connection = SSHConnection('zebra', 'admin', 'root')
    remote_shell = connection.shell
    r_ls = shell["ls"]
    remote_files = r_ls()

    For more details on how to use plumbum.SshMachine see https://plumbum.readthedocs.io/en/latest/#user-guide
    """

    def __init__(self, hostname: str, username: str, password: str) -> None:
        """Initiates SSH connection.

        Args:
            hostname: The hostname of the component we want to connect to.
            username: Username for SSH connection.
            password: Password for SSH connection.
        """

        # TODO: Check if Paramkio machine can be used with rpyc.DeployedServer.
        #       SshMachine uses an ssh connection for every command, and paramkio use only one connection.
        self._machine = plumbum.SshMachine(hostname, user=username, password=password)

    @property
    def shell(self) -> plumbum.SshMachine:
        """The SSH connection to component."""

        return self._machine

    def close(self) -> None:
        """Closes all SSH connections."""

        self._machine.close()


class TelnetConnection(BaseConnection):
    # TODO: Add telnet connection that will support RPyC.
    pass
