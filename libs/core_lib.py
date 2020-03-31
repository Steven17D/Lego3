"""
The lib contains all the logic
"""
import rpyc
import plumbum
from rpyc.utils.zerodeploy import DeployedServer


class CoreLib:
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
    def connection(self):
        return self._conn

    def getpid(self):
        return self._conn.modules.os.getpid()

    def send_packet(self, addr, data):
        rsocket = self._conn.modules["socket"]
        remote_socket = rsocket.socket()
        remote_socket.sendto(addr, data)
        remote_socket.close()

    def run_command(self, command):
        return self._conn.modules["subprocess"].check_output(command.split())

    def reboot(self):
        return self._conn.modules.os.system("reboot -f")

    def get_ip(self):
        hostname = self._conn.modules['socket'].gethostname()
        return self._conn.modules['socket'].gethostbyname(hostname)
