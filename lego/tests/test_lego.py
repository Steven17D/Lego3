# type: ignore
# pylint: skip-file
import pytest


@pytest.mark.lego("giraffe.bob", exclusive=False)
def test_sync(components):
    print(f"components a: {components}")


@pytest.mark.lego("zebra.alice")
async def test_async(components):
    print(f"components b: {components}")


class TestsSpecA:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components):
        cls.components = components
        print(f"setup class with {cls.components}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown class with {cls.components}")

    def setup_method(self):
        print(f"setup method {self.components}")

    def teardown_method(self):
        print(f"teardown method {self.components}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components):
        print(f"Using: {components} and {self.components}")

    @pytest.mark.lego('zebra.alice')
    def test_b(self, components):
        print(f"Using: {components} and {self.components}")


class TestsSpecB:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components):
        cls.components = components
        print(f"setup class with {cls.components}")

    @classmethod
    def teardown_class(cls):
        print(f"teardown with {cls.components}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components):
        print(f"Using: {components} and {self.components}")


class TestsSpecWithoutSetupClass:
    @pytest.mark.lego('zebra.alice')
    def test_a(self, components):
        print(f"Using: {components}")


class TestsSpecSetupClassWithoutTeardown:
    @classmethod
    @pytest.mark.lego('giraffe.bob')
    def setup_class(cls, components):
        cls.components = components
        print(f"setup class with {cls.components}")

    @pytest.mark.lego('zebra.alice')
    def test_a(self, components):
        print(f"Using: {components}")
