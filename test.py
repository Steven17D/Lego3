import pytest
import socket
import asyncio
import lego

@pytest.fixture
def slaves():
    pass

# Demo for running get_slaves test
@lego.get_slaves(['Linux', 'Windows'], True)
async def test_lego(slaves):
    print(slaves)

