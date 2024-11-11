import pytest

from modules.app import ApplicationBootstrapper


# pylint: disable=W0613
def pytest_runtest_protocol(item, nextitem):
    pass


def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    pass


@pytest.fixture(scope="module")
def app(request, testrun_uid):
    params = {
        "request": request,
        "testrun_uid": testrun_uid,
    }

    application = ApplicationBootstrapper().create_app(params)

    yield application

    application.close()
