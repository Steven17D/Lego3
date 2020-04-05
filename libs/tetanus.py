"""Library for Tetanus functionality."""

import components.giraffe


class Tetanus:
    """Library for Tetanus functionality."""

    def __init__(self):
        self._tool_process = None

    def install(self, giraffe: components.giraffe.Giraffe, tool: str, port: int):
        """Installs an echo server.

        Args:
            giraffe: Component API to install on.
            port: Port to echo on.
        """

        r_popen = giraffe.connection.modules['subprocess'].Popen
        self._tool_process = r_popen(
            tool.format(port),
            shell=True,
            preexec_fn=giraffe.connection.modules.os.setsid)

    def uninstall(self, giraffe):
        """Uninstall the echo server.

        Args:
            giraffe: Component API to uninstall tool.
        """

        pgrp = giraffe.connection.modules.os.getpgid(self._tool_process.pid)
        giraffe.connection.modules.os.killpg(
            pgrp, giraffe.connection.modules.signal.SIGINT)
