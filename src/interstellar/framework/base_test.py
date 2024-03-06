import pytest
from injector import Injector

from .logger import Logger


class BaseTest:
    injector: Injector
    logger: Logger

    @pytest.fixture(autouse=True)
    def setup_method_base_test(self, injector: Injector):
        self.injector = injector
        self.logger = Logger(self.__class__.__name__)
