"""
The lib contains all the logic
"""
import rpyc


class Lib(object):
    def __init__(self, slave_connection):
        self._conn = slave_connection


class Heart(Lib):
    def __init__(self, *args, **kwargs):
        super(Heart, self).__init__(*args, **kwargs)
        self._steven_lib = None

    # Define the wanted api
    def run_command(self, command):
        return self._conn.modules["subprocess"].check_output(command.split())

    def reboot(self):
        return self._conn.modules.os.system("reboot")

    def getpid(self):
        return self._conn.modules.os.getpid()

    def send_packet(self, addr, data):
        rsocket = self._conn.modules["socket"]
        remote_socket = rsocket.socket()
        remote_socket.sendto(addr, data)
        remote_socket.close()

