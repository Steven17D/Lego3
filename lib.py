"""
The lib contains all the logic
"""
import rpyc


class Lib(object):
    __slots__ = ['_conn']

    def __init__(self, slave_connection):
        self._conn = slave_connection

    @property
    def connection(self):
        return self._conn


class NetworkElement(Lib):
    def __init__(self, connection):
        super(NetworkElement, self).__init__(connection)

    def send_packet(self, addr, data):
        rsocket = self._conn.modules["socket"]
        remote_socket = rsocket.socket()
        remote_socket.sendto(addr, data)
        remote_socket.close()


class Linux(NetworkElement):
    pass


class Windows(NetworkElement):
    pass


class Bash(Lib):
    def __init__(self, linux):
        super(Bash, self).__init__(linux.connection)
        self._linux = linux

    def run_command(self, command):
        return self._conn.modules["subprocess"].check_output(command.split())

    def reboot(self):
        return self._conn.modules.os.system("reboot")

    def getpid(self):
        return self._conn.modules.os.getpid()

