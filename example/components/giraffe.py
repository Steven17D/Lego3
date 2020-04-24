"""Giraffe component is the API to Giraffe component."""

from typing import Any, Optional

import contextlib
import watchdog.events

from Lego3.lego.components import RPyCComponent
from Lego3.lego.connections import SSHConnection


class Giraffe(RPyCComponent):
    """An extended interface for Giraffe component."""

    def __init__(self, hostname, username: str, password: str) -> None:
        """Initialize RPyC connection over SSH.

        Args:
            hostname: Hostname of the component.
            username: Username for SSH login.
            password: Password for SSH login.
        """
        self.ssh = SSHConnection(hostname, username, password)
        super().__init__(hostname, self.ssh)

    @contextlib.contextmanager
    def monitor_logs(
            self,
            event_handler: Optional[watchdog.events.FileSystemEventHandler],
            directory: str
    ) -> Any:
        """Monitor specific directory to not change.

        Args:
            event_handler: Event handler that is called with every
                incoming file system event.
            directory: Directory to watch.
        """

        r_observer = self.rpyc.modules['watchdog.observers'].Observer()
        r_observer.schedule(event_handler, directory)
        r_observer.start()
        try:
            yield r_observer
        finally:
            r_observer.stop()
            r_observer.join()
            if not r_observer.event_queue.empty():
                for event in r_observer.event_queue.get():
                    assert 'log.txt' not in event.src_path
