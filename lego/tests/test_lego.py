# type: ignore
# pylint: skip-file
import pytest


@pytest.mark.lego("giraffe.bob", exclusive=False)
def test_sync(components_func):
    print(f"components a: {components_func}")


@pytest.mark.lego("zebra.alice")
async def test_async(components_func):
    print(f"components b: {components_func}")


class TestsSpecA:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components_cls):
        cls.components = components_cls
        print(f"setup class with {cls.components}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown class with {cls.components}")

    def setup_method(self):
        print(f"setup method {self.components}")

    def teardown_method(self):
        print(f"teardown method {self.components}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components_func):
        print(f"Using: {components_func} and {self.components}")

    @pytest.mark.lego('zebra.alice')
    def test_b(self, components_func):
        print(f"Using: {components_func} and {self.components}")


class TestsSpecB:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components_cls):
        cls.components = components_cls
        print(f"setup class with {cls.components}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown with {cls.components}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components_func):
        print(f"Using: {components_func} and {self.components}")


class TestsSpecWithoutSetupClass:
    @pytest.mark.lego('zebra.alice')
    def test_a(self, components_func):
        print(f"Using: {components_func}")


class TestsSpecSetupClassWithoutTeardown:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components_cls):
        cls.connections = components_cls
        print(f"setup class with {cls.connections}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components_func):
        print(f"Using: {components_func}")
