"""Elephant lib is API to elephant component."""
import contextlib
import watchdog.events

import components.core


class Giraffe(components.core.Core):
    """An extended library for Giraffe component."""

    @contextlib.contextmanager
    def monitor_logs(
            self,
            event_handler: watchdog.events.FileSystemEventHandler,
            directory: str
        ):
        """Monitor specific directory to not change.

        Args:
            event_handler: Event handler that called with every
                incoming file system event.
            directory: Diractory to watch on.
        """

        r_observer = self.connection.modules['watchdog.observers'].Observer()
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
