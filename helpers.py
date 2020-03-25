import socket
import getpass


class Client:
    def __init__(self):
        self._user_name = getpass.getuser()
        self._host_name = socket.gethostname()


class Test:
    def __init__(self, test):
        self._test_name = test.__name__
        # Consider to get the should_schedule parameter here so the user will
        # not have to enter it before every test will run.
        # self._should_schedule = should_schedule


class Setup:
    def __init__(self, elements, allocation_type):
        self._elements = elements
        self._allocation_type = allocation_type
