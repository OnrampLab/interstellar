import os

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from .base_test import BaseTest
from .utils import (
    wait_for_element_by_selector,
    wait_for_element_by_xpath,
    wait_for_element_to_click_by_xpath,
    wait_for_element_to_disappear_by_xpath,
)


@pytest.mark.UI
class BaseUITest(BaseTest):
    driver: WebDriver

    @pytest.fixture(autouse=True)
    def setup_method_framework_base_ui(self, driver):
        self.driver = driver
        self.app.init_e2e()

    def get_page(self, page_class):
        return page_class(self.injector, self.driver)

    def screenshot(self, file_name):
        screenshot_path = os.path.join(os.getcwd(), f"screenshots/{file_name}")

        self.driver.save_screenshot(screenshot_path)

    def wait_for_dom_element_by_xpath(self, xpath):
        return wait_for_element_by_xpath(self.driver, xpath)

    def wait_for_dom_element_to_disappear_by_xpath(self, xpath):
        return wait_for_element_to_disappear_by_xpath(self.driver, xpath)

    def wait_for_dom_element_to_click_by_xpath(self, xpath):
        return wait_for_element_to_click_by_xpath(self.driver, xpath)

    def wait_for_dom_element_by_selector(self, css_selector):
        return wait_for_element_by_selector(self.driver, css_selector)
