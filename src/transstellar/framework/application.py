import logging
import os

from injector import Injector
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver


class Application:
    container: Injector
    testrun_uid: str
    driver: WebDriver

    def __init__(self, request, testrun_uid, options=None):
        self.testrun_uid = testrun_uid
        self.container = Injector()

        if options is None:
            self.options = {"enable_e2e": False}
        else:
            self.options = options

        if self.is_e2e_enabled():
            self.driver = self.init_driver()

        self.configure_log(request.config)

    def is_e2e_enabled(self):
        return self.options["enable_e2e"]

    def close(self):
        if self.is_e2e_enabled():
            logging.info("Driver closed")
            self.driver.quit()

        logging.info("Application closed")

    def configure_log(self, config):
        worker_id = os.environ.get("PYTEST_XDIST_WORKER")
        if worker_id is not None:
            with open(file=f"logs/pytest_{worker_id}.log", mode="w", encoding="utf-8"):
                pass

            logging.basicConfig(
                format=config.getini("log_file_format"),
                filename=f"logs/pytest_{worker_id}.log",
                level=config.getini("log_file_level"),
            )

    def init_driver(self) -> WebDriver:
        selenium_cmd_executor = os.environ.get(
            "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
        )
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = Remote(command_executor=selenium_cmd_executor, options=options)
        driver.implicitly_wait(5)
        logging.info("Driver initialized")

        return driver

    def get(self, key: any):
        return self.container.get(key)
