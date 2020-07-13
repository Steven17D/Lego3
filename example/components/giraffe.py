"""Giraffe component is the API to Giraffe component."""
from typing import Any, Optional

import asyncio
import contextlib

from Lego3.lego.components import RPyCComponent
from Lego3.lego.connections import RPyCConnection


class LogMonitor:
    """A logs monitoring manager."""

    async def monitor(
        self,
        connection: RPyCConnection,
        path: str
    ) -> Any:
        """Monitor file task.

        Args:
            connection: The RPyC connection to remove mechine.
            path: The file or directory to monitor.
        """

        try:
            first_stat = connection.modules.os.stat(path)
            while True:
                assert first_stat == connection.modules.os.stat(path)
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            pass


class Giraffe(RPyCComponent):
    """An extended interface for Giraffe component."""

    @contextlib.contextmanager
    def monitor_logs(self, path: str) -> Any:
        """Monitors on file or directory in this remove machine.

        Args:
            path: The file or directory to monitor.
        """

        logs_monitor = LogMonitor()
        monitoring = asyncio.create_task(logs_monitor.monitor(self.connection, path))
        yield
        try:
            monitoring.result() # Raises the task exceptions
        except asyncio.exceptions.InvalidStateError:
            pass
        finally:
            monitoring.cancel()

