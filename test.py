import pytest
import time
import asyncio


@pytest.mark.lego("giraffe", exclusive=false)
def test_a(slave):
    print(f"Slave a: {slave}")
    time.sleep(1)


# @pytest.mark.lego(["elephant"], wait=False)
@pytest.mark.lego("giraffe")
async def test_b(slave):
    print(f"Slave b: {slave}")
    await asyncio.sleep(1)
