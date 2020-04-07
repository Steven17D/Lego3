"""
The lib contains all the logic
"""
from typing import Tuple
import rpyc
import plumbum
from rpyc.utils.zerodeploy import DeployedServer


class Core:
    """
    Wrapper for RPyC connection.
    Provides simple API which is generic for all RPyC connections.
    In order to extend the API implement a wrapping Lib.
    """

    __slots__ = ['_conn']

    def __init__(self, hostname):
        try:
            self._conn = rpyc.classic.connect(hostname, keepalive=True)
        except ConnectionRefusedError:
            with plumbum.SshMachine(hostname, user="root", password="password") as machine:
                with DeployedServer(machine) as server:
                    self._conn = server.classic_connect()

    def __enter__(self):
        return self

    def __exit__(self, exec_type, value, traceback):
        self._conn.close()

    @property
    def connection(self) -> rpyc.core.protocol.Connection:
        """Gets the RPyC connection to the component."""

        return self._conn

    def getpid(self) -> int:
        """Gets the PID of the service process."""

        return self._conn.modules.os.getpid()

    def send_packet(self, addr: Tuple[str, int], data: bytes):
        """Sends an UDP packet.

        Args:
            addr - The address (IP and port) to send the packet to.
            data - The data to send.
        """

        r_socket = self._conn.modules['socket']
        R_AF_INET = self._conn.modules['socket'].AF_INET
        R_SOCK_DGRAM = self._conn.modules['socket'].SOCK_DGRAM
        remote_socket = r_socket.socket(R_AF_INET, R_SOCK_DGRAM)
        remote_socket.sendto(data, addr)
        remote_socket.close()

    def run_command(self, command: str) -> str:
        """Runs a bash command on the remote machind.

        Args:
            command - The command to run.

        Returns:
            The output of the command.
        """

        return self._conn.modules["subprocess"].check_output(command.split())

    def reboot(self):
        """Reboots the remote machine."""

        return self._conn.modules.os.system("reboot -f")

    def get_ip(self) -> str:
        """Gets the IP of the remote machine."""

        hostname = self._conn.modules['socket'].gethostname()
        return self._conn.modules['socket'].gethostbyname(hostname)
