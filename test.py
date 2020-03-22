import pytest
from lego import get_slaves


@get_slaves("127.0.0.1")
def test_command(slaves):
    heart = slaves["127.0.0.1"]
    output = heart.run_command("uname -a")
    assert "Linux" in output

# @get_slaves("127.0.0.1")
# def test_extreme(slaves):
#     """
#     1. Monito log
#     2. Send and receive packets
#     3. reboot
#     """
#     heart = slaves["127.0.0.1"]
#     try:
#         heart.steven_lib.install()
#     finally:
#         heart.steven_lib.uinstall()


#@get_slaves("A_1", "B_1", "B_2", "C_1", "C_2")
# def test_multiple_slaves(slaves):
#    locals().update(slaves)

