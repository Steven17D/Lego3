"""
The lib contains all the logic
"""

class Heart:
    def __init__(self, slave_connection):
        self._conn = slave_connection

    # Define the wanted api
    def reboot(self):
        print self._conn
        self._conn.modules.os.system("ifconfig")

