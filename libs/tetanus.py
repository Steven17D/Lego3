"""Library for Tetanus functionality."""

import components.giraffe


class Tetanus:
    """Library for Tetanus functionality."""

    def __init__(self):
        self._tool_pid = -1

    def install(self, giraffe: components.giraffe.Giraffe, tool: str, port: int):
        """Installs an echo server.

        Args:
            giraffe: Component API to install on.
            port: Port to echo on.
        """

        r_popen = giraffe.connection.modules['subprocess'].Popen
        self._tool_pid = r_popen(tool.format(port), shell=True).pid

    def uninstall(self, giraffe):
        """Uninstall the echo server.

        Args:
            giraffe: Component API to uninstall tool.
        """

        try:
            giraffe.connection.modules.os.kill(self._tool_pid, 9)
            giraffe.connection.modules.os.kill(self._tool_pid + 1, 9)
        except ProcessLookupError:
            pass
