import unittest

import pytest

from transstellar.framework import BaseUITest, Element, handle_ui_error
from transstellar.html import Body, Button


class Page(Body):
    pass


class CodeBlock(Element):
    XPATH_CURRENT = '//article[@id="post-76"]'


@handle_ui_error()
class TestButton(BaseUITest, unittest.TestCase):
    page: Page

    @pytest.fixture(autouse=True)
    def setup_method_test(self):
        self.app.driver.get("https://html.com/attributes/button-disabled/")
        self.app.driver.set_window_size(1024, 768)
        self.page = Page(self.app)
        self.code_block = self.page.find_element(CodeBlock)

    def test_constructor(self):
        element = Button(self.app)

        assert element is not None

    def test_disabled(self):
        input_element = self.page.find_element(Button)

        assert not input_element.is_enabled()
