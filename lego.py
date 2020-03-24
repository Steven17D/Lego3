import rpyc
import socket
import getpass
import asyncio
import functools

from helpers import Client, Test, Setup


# Should be in one main file, to enable access by the resource manager and this
# file.
# Which file format?

SETUP = {
    'Linux': ['1', '2', '3'],
    'Windows': ['1', '2']
}

#########################

def create_slaves(setup):
    """
    Creates salves based on the requested setup.

    Args:
        setup - The requested setup.

    Returns:
        slaves.
    """

    slaves = []
    for component_name in setup:
        slaves = 'API_' + component_name
    return slaves

def get_slaves(setup: dict, should_lock: bool):
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

    def decorator_wrapper(test):
        @functools.wraps(test)
        async def wrapper():
            loop = asyncio.get_event_loop()
            resource_manager = rpyc.connect(host='127.0.0.1', port=18861)

            request_setup = resource_manager.root.request_setup
            may_run = await loop.run_in_executor(None, request_setup, Client(),Test(test), Setup(setup, should_lock))

            if not may_run:
                get_wait_info = resource_manager.root.get_wait_info
                print(await loop.run_in_executor(None, get_wait_info))

                should_schedule = input('By the above info, would you like to schedule your test? (y/n)')
                if should_schedule != 'y':
                    print('The test cannot run since there are no available setup')
                    resource_manager.close()
                    return

                notify_me = resource_manager.root.notify_me
                await loop.run_in_executor(None, notify_me)

            print('Your test may run')

            slaves = create_slaves(setup)
            await test(slaves)

            resource_manager.close()

        return wrapper

    return decorator_wrapper
