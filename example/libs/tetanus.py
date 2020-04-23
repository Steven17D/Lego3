"""Library for Tetanus functionality."""
import subprocess

from Lego3.example.components.giraffe import Giraffe


class Tetanus:
    """Library for Tetanus functionality."""

    def __init__(self) -> None:
        self._tool_process: subprocess.Popen

    def install(
            self,
            giraffe: Giraffe,
            tool: str,
            port: int
        ) -> None:
        """Installs an echo server.

        Args:
            giraffe: Component API to install on.
            port: Port to echo on.
        """

        r_popen = giraffe.rpyc.modules['subprocess'].Popen
        self._tool_process = r_popen(
            tool.format(port),
            shell=True,
            preexec_fn=giraffe.rpyc.modules.os.setsid)

    def uninstall(self, giraffe: Giraffe) -> None:
        """Uninstall the echo server.

        Args:
            giraffe: Component API to uninstall tool.
        """
        pgrp = giraffe.rpyc.modules.os.getpgid(self._tool_process.pid)
        giraffe.rpyc.modules.os.killpg(
            pgrp, giraffe.rpyc.modules.signal.SIGINT)
