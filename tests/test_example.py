""" Example lego tests """
import asyncio
import time

from lego import require_components


@require_components("giraffe", exclusive=False)
def test_a(slaves):
    print(f"Slaves a: {slaves}")
    time.sleep(0.2)


@require_components("elephant")
async def test_b(slaves):
    print(f"Slaves b: {slaves}")
    await asyncio.sleep(0.2)

class TestsSpecA:
    @require_components('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def teardown_class(cls):
        print(f"teardown class with {cls._slaves}")

    def setup_method(self):
        print(f"setup method {self._slaves}")

    def teardown_method(self):
        print(f"teardown method {self._slaves}")

    @require_components('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")

    @require_components('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")


class TestsSpecB:
    @require_components('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def teardown_class(cls):
        print(f"teardown with {cls._slaves}")

    def setup_method(self):
        print(f"setup method {self._slaves}")

    def teardown_method(self):
        print(f"teardown method {self._slaves}")

    @require_components('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")

    @require_components('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves} and {self._slaves}")


class TestsSpecWithoutSetupClass:
    @require_components('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def setup_method(self):
        print(f"setup method")

    def teardown_method(self):
        print(f"teardown method")

    @require_components('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves}")

    @require_components('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves}")


class TestsSpecSetupClassWithoutTeardown:
    @require_components('giraffe')
    def setup_class(cls, slaves):
        cls._slaves = slaves
        print(f"setup class with {cls._slaves}")

    def setup_method(self):
        print(f"setup method")

    def teardown_method(self):
        print(f"teardown method")

    @require_components('zebra')
    def test_a(self, slaves):
        print(f"Using: {slaves}")

    @require_components('elephant')
    def test_b(self, slaves):
        print(f"Using: {slaves}")
