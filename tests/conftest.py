import logging
import os
import typing as t

import pytest
from injector import Injector, inject
from selenium.webdriver import ChromeOptions, Remote

SELENIUM_CMD_EXECUTOR = os.environ.get(
    "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
)

def init_injector():
    injector = Injector()

    return injector

def pytest_runtest_protocol(item, nextitem):
    pass


def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    pass


def pytest_configure(config):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        with open(f"logs/pytest_{worker_id}.log", "w"):
            pass

        logging.basicConfig(
            format=config.getini("log_file_format"),
            filename=f"logs/pytest_{worker_id}.log",
            level=config.getini("log_file_level"),
        )


@pytest.fixture(scope="session")
def injector(request):
    injector = init_injector()


    return injector


@pytest.fixture(scope="session")
def driver() -> t.Iterator[Remote]:
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = Remote(command_executor=SELENIUM_CMD_EXECUTOR, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
