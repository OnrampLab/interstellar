import os
import unittest
from time import time
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.remote.webelement import WebElement

from transstellar.framework import BaseUITest, Element, handle_ui_error


class Page(Element):
    XPATH_CURRENT = "//body"


class Header(Element):
    XPATH_CURRENT = "//header"


class Image(Element):
    XPATH_CURRENT = "//img"


class Button(Element):
    XPATH_CURRENT = "//button"


class HeaderIconLink(Element):
    XPATH_CURRENT = '//a[@href="https://github.com/"]'


@handle_ui_error()
class TestElement(BaseUITest, unittest.TestCase):
    page: Page

    @pytest.fixture(autouse=True)
    def setup_method_test(self):
        self.app.driver.get("https://github.com")
        self.page = Page(self.app)

    def test_constructor(self):
        element = Header(self.app)

        assert element is not None

    def teardown_method(self, method):  # pylint: disable=W0613
        screenshot_path = os.path.join(os.getcwd(), "screenshots", "screenshot.png")
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    def test_get_current_element_xpath(self):
        xpath = Header.get_current_element_xpath()

        assert xpath == Header.XPATH_CURRENT

    def test_get_current_element_xpath_with_empty_xpath_current(self):
        with pytest.raises(Exception) as exc_info:
            Element.get_current_element_xpath()

        assert (
            str(exc_info.value)
            == "Element should set XPATH_CURRENT in order to get element"
        )

    def test_get_current_dom_element(self):

        element = Header(self.app)
        dom_element = element.get_current_dom_element()

        assert isinstance(dom_element, WebElement)

    def test_set_current_dom_element(self):
        # should think a way to test
        pass

    def test_get_current_html(self):
        element = Header(self.app)
        html = element.get_current_html()

        assert "<button" in html

    def test_refresh(self):
        element = HeaderIconLink(self.app)
        dom_element = element.get_current_dom_element()
        html = dom_element.get_attribute("innerHTML")

        new_dom_element = element.refresh()
        new_html = new_dom_element.get_attribute("innerHTML")

        # NOTE: there is a chance to error
        assert html == new_html

    def test_find_global_element(self):
        element = self.page.find_global_element(Header)

        assert isinstance(element, Header)

    def test_find_element(self):
        header = self.page.find_element(Header)
        icon = header.find_element(HeaderIconLink)

        assert isinstance(icon, HeaderIconLink)

    def test_find_element_with_timeout(self):
        header = self.page.find_element(Header, 5)
        icon = header.find_element(HeaderIconLink)

        assert isinstance(icon, HeaderIconLink)

    def test_find_elements(self):
        images = self.page.find_elements(Image)

        assert len(images) > 1

    def test_find_elements_with_timeout(self):
        images = self.page.find_elements(Image, 5)

        assert len(images) > 1

    def test_find_element_by_label(self):
        sign_up_button = self.page.find_element_by_label(Button, "Sign up for GitHub")

        assert isinstance(sign_up_button, Button)

    def test_wait_for_global_element_to_disappear(self):
        # should think a way to test
        pass

    def test_find_global_dom_element_by_xpath(self):
        dom_element = self.page.find_global_dom_element_by_xpath(Header.XPATH_CURRENT)

        assert isinstance(dom_element, WebElement)

    def test_find_dom_elements_by_tag_name(self):
        dom_elements = self.page.find_dom_elements_by_tag_name("header")

        assert isinstance(dom_elements[0], WebElement)

    def test_find_dom_element_by_xpath(self):
        dom_element = self.page.find_dom_element_by_xpath(Header.XPATH_CURRENT)

        assert isinstance(dom_element, WebElement)

    def test_wait_for_dom_element_to_disappear_by_xpath(self):
        # should think a way to test
        pass

    def test_wait_for_dom_element_to_click_by_xpath(self):
        dom_element = self.page.wait_for_dom_element_to_click_by_xpath(
            Header.XPATH_CURRENT
        )

        assert isinstance(dom_element, WebElement)

    def test_wait_for_dom_element_by_selector(self):
        dom_element = self.page.wait_for_dom_element_by_selector(".header-logged-out")

        assert isinstance(dom_element, WebElement)

    def test_sleep(self):
        start_time = time()

        self.page.sleep(2)

        end_time = time()
        elapsed_time = end_time - start_time

        assert 1.9 <= elapsed_time <= 2.1

    def test_scroll_to_view(self):
        self.app.close()
        self.app.driver = MagicMock()

        self.page.scroll_to_view()

        self.app.driver.execute_script.assert_called_once_with(
            "arguments[0].scrollIntoView(false);", self.page.dom_element
        )

        self.app.init_e2e()

    def test_get_classes(self):
        classes = self.page.get_classes()

        assert "home-campaign" in classes
