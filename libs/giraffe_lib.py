"""Elephant lib is API to elephant component."""
import watchdog.events
import contextlib

import libs.core_lib


# Just for the test
class EventHandler(watchdog.events.FileSystemEventHandler):
    """Event handler called on every incoming file system event."""

    def on_modified(self, event: watchdog.events.FileModifiedEvent):
        """Called when file has modified.

        Args:
            event: File modified event.
        """

        assert event.src_file != 'a.txt'


class GiraffeLib(libs.core_lib.CoreLib):
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

        r_observer = self._con.modules['watchdog.observers'].Observer()
        r_observer.schedule(event_handler, directory)
        r_observer.start()
        try:
            yield r_observer
        finally:
            r_observer.stop()
