import pytest
import time


@pytest.mark.lego("giraffe")
def test_a(slave):
    print(f"Slave a: {slave}")
    time.sleep(1)


@pytest.mark.lego("elephant")
def test_b(slave):
    print(f"Slave b: {slave}")
    time.sleep(1)
