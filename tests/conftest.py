import pytest

from modules.app import ApplicationBootstrapper


def pytest_runtest_protocol(item, nextitem):
    pass


def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    pass


@pytest.fixture(scope="module")
def app(request, testrun_uid):
    application = ApplicationBootstrapper().create_app(request, testrun_uid)

    yield application

    application.close()
