import pytest

from transstellar.framework.base_ui_test import BaseUITest
from transstellar.framework.module import Module


class SimpleModule(Module):
    name: str

    def bootstrap(self):
        self.name = "SimpleModule"


class TestModule(BaseUITest):
    module: SimpleModule

    @pytest.fixture(autouse=True)
    def setup_method_test(self):
        self.module = SimpleModule(self.app)

    def test_app(self):
        assert self.module.app == self.app

    def test_bootstrap(self):
        self.logger.info(self.module)
        assert self.module.name == "SimpleModule"
