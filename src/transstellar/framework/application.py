import logging
import os
from typing import Type

from injector import Injector
from pytest import FixtureRequest
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver

from transstellar.framework.main_config import MainConfig

from .module import Module
from .router import Router


class Application:
    container: Injector
    testrun_uid: str
    request: FixtureRequest
    driver: WebDriver
    options: any
    e2e_enabled: bool = False
    closed: bool = False
    logged_in: bool = False

    def __init__(self, params: dict):
        logging.info("Creating application")

        options = params.get("options")
        self.request = params.get("request")
        self.driver = params.get("driver")
        self.testrun_uid = params.get("testrun_uid")
        self.container = Injector()
        self.router = Router(self)
        self.main_config = self.get(MainConfig)

        routes = params.get("routes")

        if options:
            self.options = options
        else:
            self.options = {}

        self.__configure_log__()
        self.register_routes(routes)

    def init_e2e(self):
        if self.e2e_enabled:
            return

        self.e2e_enabled = True

        self.driver = self.__init_driver__()

        self.closed = False

    def is_e2e_enabled(self):
        return self.e2e_enabled

    def get(self, key: any):
        return self.container.get(key)

    def register_module(self, module_class: Type[Module]):
        module = module_class(self)
        self.container.binder.bind(module_class, module)

    def register_routes(self, routes: dict):
        self.router.register_routes(routes)

    def get_page(self, route_key: str):
        if not self.e2e_enabled:
            return None

        route = self.router.get_route(route_key)

        page = route.get_page(self)
        page.wait_for_ready()

        return page

    def build_page(self, page_class):
        return page_class(self)

    def go_to_url(self, url: str):
        if url != self.driver.current_url:
            self.driver.get(url)

    def go_to(self, route_key: str):
        if not self.e2e_enabled:
            return None

        route = self.router.get_route(route_key)

        base_url = self.main_config.get_app_url()
        path = route.path
        url = f"{base_url}{path}"

        self.go_to_url(url)

        page = route.get_page(self)
        page.wait_for_ready()

        return page

    def close(self):
        if self.closed:
            return

        logging.info("Closing application")

        if self.is_e2e_enabled():
            self.driver.quit()
            logging.info("Driver closed")

        self.e2e_enabled = False
        self.closed = True

        logging.info("Application closed")

    def set_logged_in(self):
        if not self.is_e2e_enabled():
            raise RuntimeError("Only E2E test supports setting logged_in")

        self.logged_in = True

    def is_logged_in(self):
        return self.logged_in

    def __configure_log__(self):
        worker_id = os.environ.get("PYTEST_XDIST_WORKER")
        if worker_id is not None:
            with open(file=f"logs/pytest_{worker_id}.log", mode="w", encoding="utf-8"):
                pass

            logging.basicConfig(
                format=self.request.config.getini("log_file_format"),
                filename=f"logs/pytest_{worker_id}.log",
                level=self.request.config.getini("log_file_level"),
            )

    def __init_driver__(self) -> WebDriver:
        logging.info("Initializing driver")
        selenium_cmd_executor = os.environ.get(
            "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
        )
        implicitly_wait_time = self.options.get("implicitly_wait_time", 10)
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = Remote(command_executor=selenium_cmd_executor, options=options)
        driver.implicitly_wait(implicitly_wait_time)
        logging.info("Driver initialized")

        return driver
