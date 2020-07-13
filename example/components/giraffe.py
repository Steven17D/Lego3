"""Giraffe component is the API to Giraffe component."""
from typing import Any, Optional

import asyncio
import contextlib
import watchdog.events

from Lego3.lego.components import RPyCComponent


class LogMonitor:
    """A logs monitoring manager."""

    async def monitor(self, c, d):
        try:
            old_stat = c.modules.os.stat(d)
            while True:
                assert old_stat == c.modules.os.stat(d)
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            pass


class Giraffe(RPyCComponent):
    """An extended interface for Giraffe component."""

    @contextlib.contextmanager
    def monitor_logs(self, d) -> Any:
        l = LogMonitor()
        t = asyncio.create_task(l.monitor(self.connection, d))
        yield
        try:
            t.result() # Raises the task exceptions
        except asyncio.exceptions.InvalidStateError:
            pass
        finally:
            t.cancel()

