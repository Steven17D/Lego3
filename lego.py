import rpyc
import socket
import getpass
import functools


#########################

# Should inhrate from db for easy API to store in DB

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

##########################

# Should be in one main file, to enable access by the resource manager and this
# file.
# Which file format?

SETUP = {
    'Linux': ['1', '2', '3'],
    'Windows': ['1', '2']
}

#########################



def get_slaves(setup: dict, should_lock: bool) -> function:
    """
    Returns the slaves for the requested setup when its available.

    Note: Should run several tests asynchronicly.

    Args:
        setup - Which setup required, specific devices or just types.
        should_lock - Whether to lock the setup from another requests.
        ## should_schedule - Whether to schedule the test if the setup
            is unavailable or return false.

    Returns:
        The requested slaves.
    """

    def decorator_wrapper(test: coroutine) -> function:
        @functools.wraps(test)
        def wrapper():
            # Run the ResourceManager (from dv-samech) if it not running
            resource_manager = rpyc.connect(host='127.0.0.1', port=18861)
            request_setup = rpyc.async_(resource_manager.root.request_setup)

            # When setup request comes to the ResourceManager, it procceed the
            # request, regiter it in the registred_to_run queue, and return whether
            # the setup is available and no registered test ahead of the test.
            may_run = await request_setup(Client(), Test(test), Setup(setup, should_lock))

            if not may_run:
                get_waiting_tests_info = rpyc.async_(resource_manager.root.get_waiting_test_info)
                print(await get_waiting_tests_info())

                should_schedule = input('By the above info, would you like to schedule
                    your test?')
                if not should_schedule:
                    print('The test cannot run since there are no available setup')
                    resource_manager.close()
                    return

                notify_to_run = rpyc.async_(resource_manager.root.notify_to_run)
                await notify_to_run()

            print('Your test may run')

            # Wrap every network element in its basic lib
            slaves = create_slaves(setup)
            test(slaves)

            resource_manager.close()

        return wrapper

    return decorator_wrapper
