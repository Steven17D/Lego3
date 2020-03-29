import pytest
import time
import asyncio


@pytest.mark.lego("giraffe", exclusive=False)
def test_a(slaves):
    print(f"Slaves a: {slaves}")
    time.sleep(0.25)


@pytest.mark.lego("elephant")
async def test_b(slaves):
    print(f"Slaves b: {slaves}")
    await asyncio.sleep(0.25)


class TestsSpecA:
    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def teardown_class(cls):
        print(f"teardown class with {cls._slaves}")
        
    def setup_method(self):
        print(f"setup method {self._slaves}")

    def teardown_method(self):
        print(f"teardown method {self._slaves}")

    @pytest.mark.lego('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")

    @pytest.mark.lego('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")


class TestsSpecB:
    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def teardown_class(cls):
        print(f"teardown with {cls._slaves}")

    def setup_method(self):
        print(f"setup method {self._slaves}")

    def teardown_method(self):
        print(f"teardown method {self._slaves}")

    @pytest.mark.lego('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")

    @pytest.mark.lego('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")


class TestsSpecWithoutSetupClass:
    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def setup_method(self):
        print(f"setup method")

    def teardown_method(self):
        print(f"teardown method")

    @pytest.mark.lego('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves}")

    @pytest.mark.lego('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves}")


class TestsSpecSetupClassWithoutTeardown:
    @pytest.mark.lego('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def setup_method(self):
        print(f"setup method")

    def teardown_method(self):
        print(f"teardown method")

    @pytest.mark.lego('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves}")

    @pytest.mark.lego('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves}")
