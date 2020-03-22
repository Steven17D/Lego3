"""
The lib contains all the logic
"""

class Lib(object):
    def __init__(self, slave_connection):
        self._conn = slave_connection


class EmperorLib(object):
    def install(self):
        print "Installing Emperor"

    def uninstall(self):
        print "Uninstalling Emperor"


class Heart(Lib):
    def __init__(self, *args, **kwargs):
        super(Heart, self).__init__(*args, **kwargs)
        self._emperor_lib = None

    # Define the wanted api
    def reboot(self):
        self._conn.modules.os.system("reboot")

    def getpid(self):
        return self._conn.modules.os.getpid()

    @propery
    def emperory_lib(self):
        if self._emperor_lib is None:
            self._emperor_lib = EmperorLib(self)
        return self._emperor_lib

