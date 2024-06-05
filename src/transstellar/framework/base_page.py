import sys
from urllib.parse import ParseResult, urlparse, urlunparse

from transstellar.framework.page_decorator_meta import PageDecoratorMeta

from .element import Element


class BasePage(Element, metaclass=PageDecoratorMeta):
    XPATH_CURRENT = "//body"

    # deprecated
    def go_to(self, url: str):
        self.go_to_url(url)

    def go_to_url(self, url: str):
        if url != urlunparse(self.get_current_url()):
            self.driver.get(url)

        self.set_current_dom_element(None)

    def go_to_route(self, route_key: str):
        self.app.go_to(route_key)

    # deprecated
    def get_page(self, page_class):
        return self.build_page(page_class)

    def build_page(self, page_class):
        return self.app.build_page(page_class)

    def get_route_page(self, route_key: str):
        self.app.get_page(route_key)

    def get_page_from_module(self, module, page_class):
        return getattr(sys.modules[module], page_class)(self.app)

    def get_current_url(self) -> ParseResult:
        return urlparse(self.app.driver.current_url)
