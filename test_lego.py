import pytest
import time
import asyncio


@pytest.mark.lego("giraffe", exclusive=False)
def test_a(slaves):
    print(f"Slaves a: {slaves}")
    time.sleep(1)


@pytest.mark.lego("elephant")
async def test_b(slaves):
    print(f"Slaves b: {slaves}")
    await asyncio.sleep(1)
