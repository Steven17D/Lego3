import asyncio
import pytest
import socket

# Will replaced with get_slaves from lego.py
def ask_for_setup(test):
    async def wrapper():
        print(f'Want to run {test}')
        setup = await asyncio.sleep(1)
        await test(setup)
    return wrapper

@pytest.mark.asyncio_cooperative
@ask_for_setup
async def test_1(setup):
    print("test1 start")
    await asyncio.sleep(2)
    print("test1 done")

@pytest.mark.asyncio_cooperative
@ask_for_setup
async def test_2(setup):
    print("test2 start")
    await asyncio.sleep(1)
    print("test2 done")

