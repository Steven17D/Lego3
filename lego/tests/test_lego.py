# type: ignore
# pylint: skip-file
import pytest


@pytest.mark.lego("giraffe", exclusive=False)
def test_sync(connections):
    print(f"connections a: {connections}")


@pytest.mark.lego("elephant")
async def test_async(connections):
    print(f"connections b: {connections}")


class TestsSpecA:
    @classmethod
    @pytest.mark.lego('giraffe')
    def setup_class(cls, connections):
        cls.connections = connections
        print(f"setup class with {cls.connections}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown class with {cls.connections}")

    def setup_method(self):
        print(f"setup method {self.connections}")

    def teardown_method(self):
        print(f"teardown method {self.connections}")

    @pytest.mark.lego('zebra')
    def test_a(self, connections):
        print(f"Using: {connections} and {self.connections}")

    @pytest.mark.lego('elephant')
    def test_b(self, connections):
        print(f"Using: {connections} and {self.connections}")


class TestsSpecB:
    @classmethod
    @pytest.mark.lego('giraffe')
    def setup_class(cls, connections):
        cls.connections = connections
        print(f"setup class with {cls.connections}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown with {cls.connections}")

    @pytest.mark.lego('zebra')
    def test_a(self, connections):
        print(f"Using: {connections} and {self.connections}")


class TestsSpecWithoutSetupClass:
    @pytest.mark.lego('zebra')
    def test_a(self, connections):
        print(f"Using: {connections}")


class TestsSpecSetupClassWithoutTeardown:
    @classmethod
    @pytest.mark.lego('giraffe')
    def setup_class(cls, connections):
        cls.connections = connections
        print(f"setup class with {cls.connections}")

    @pytest.mark.lego('zebra')
    def test_a(self, connections):
        print(f"Using: {connections}")
