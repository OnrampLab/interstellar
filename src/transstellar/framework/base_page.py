import sys
from urllib.parse import ParseResult, urlparse

from .element import Element
from .utils import wait_for_element_by_xpath


class BasePage(Element):
    XPATH_CURRENT = "//body"

    def get_page(self, page_class):
        return page_class(self.injector, self.driver)

    def get_page_from_module(self, module, page_class):
        return getattr(sys.modules[module], page_class)(self.injector, self.driver)

    def get_current_url(self) -> ParseResult:
        return urlparse(self.driver.current_url)
