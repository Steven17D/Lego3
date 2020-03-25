import pytest
import time


@pytest.mark.lego("1.1.1.1")
def test_a(slave):
    print(f"Slave a: {slave}")
    time.sleep(1)


@pytest.mark.lego("2.2.2.2")
def test_b(slave):
    print(f"Slave b: {slave}")
    time.sleep(1)


@pytest.mark.xfail
def test_missing_fixture(slave):
    print(f"Slave a: {slave}")
    time.sleep(1)


# @pytest.mark.xfail
# @pytest.mark.lego("2.2.2.2")
# def test_missing_argument(test_input):
#     print(f"No slave")
#     time.sleep(1)

