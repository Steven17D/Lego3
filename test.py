import pytest
import socket
import asyncio
import lego
import time


@pytest.mark.lego("1.1.1.1")
def test_a(slave):
    print(f"Slave a: {slave}")
    time.sleep(2)


@pytest.mark.lego("2.2.2.2")
def test_b(slave):
    print(f"Slave b: {slave}")
    time.sleep(2)
