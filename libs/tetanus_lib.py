"""Library for Tetanus functionality."""

import scapy.layers.inet

import libs.giraffe_lib

TOOL = 'ncat -l {} --keep-open --udp --exec "/bin/cat"'


class TetanusLib:
    """Library for Tetanus functionality."""

    def __init__(self):
        self._tool_pid = -1

    def install(self, giraffe: libs.giraffe_lib.GiraffeLib, port: int):
        """Installs an echo server.

        Args:
            giraffe: Component API to install on.
            port: Port to echo on.
        """

        r_popen = giraffe.connection.modules['subprocess'].Popen
        self._tool_pid = r_popen(TOOL.format(port), shell=True).pid

    def uninstall(self, giraffe):
        """Uninstall the echo server.

        Args:
            giraffe: Component API to uninstall tool.
        """

        giraffe.connection.modules.os.kill(self._tool_pid, 9)
        giraffe.connection.modules.os.kill(self._tool_pid + 1, 9)
