import os
import unittest
from time import time
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.remote.webelement import WebElement

from transstellar.framework import BaseUITest, Element, handle_ui_error
from transstellar.html import Body, Button, Div, Header, Image, Li


class Page(Body):
    pass


class NotExistDiv(Element):
    XPATH_CURRENT = '//div[@id="not-exist"]'


class HeaderIconLink(Element):
    XPATH_CURRENT = '//a[@href="/"]'


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

    def test_find_next_element(self):
        div = self.page.find_next_element(
            Div,
            Button,
        )

        assert isinstance(div, Div)

    def test_find_next_element_by_xpath(self):
        div = self.page.find_next_element_by_xpath(Div, "//button")

        assert isinstance(div, Div)

    def test_find_preceding_element(self):
        div = self.page.find_preceding_element(
            Div,
            Button,
        )

        assert isinstance(div, Div)

    def test_find_preceding_element_by_xpath(self):
        div = self.page.find_preceding_element_by_xpath(Div, "//button")

        assert isinstance(div, Div)

    def test_get_next_element(self):
        li = self.page.find_element_by_label(Li, "Solutions")

        assert isinstance(li, Li)

        next_li = li.get_next_element(Li)

        assert next_li.get_text() == "Resources"

    def test_get_preceding_element(self):
        li = self.page.find_element_by_label(Li, "Solutions")

        assert isinstance(li, Li)

        preceding_li = li.get_preceding_element(Li)

        assert preceding_li.get_text() == "Product"

    def test_find_element_by_id(self):
        content = self.page.find_element_by_id(Div, "start-of-content")

        assert isinstance(content, Div)

    def test_is_element_present(self):
        assert not self.page.is_element_present(NotExistDiv)

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
