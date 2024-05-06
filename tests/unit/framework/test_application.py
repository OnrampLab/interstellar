import pytest

from transstellar.framework.application import Application
from transstellar.framework.base_page import BasePage
from transstellar.framework.module import Module


class TestApplication:
    app: Application

    @pytest.fixture(autouse=True)
    def setup_method_test(self, request, testrun_uid):
        params = {
            "request": request,
            "testrun_uid": testrun_uid,
            "routes": {"dashboard": BasePage},
        }
        self.app = Application(params)

    def teardown_method(self):
        self.app.close()

    def test_default(self):
        assert not self.app.is_e2e_enabled()

    def test_enable_e2e(self):
        self.app.init_e2e()

        assert self.app.is_e2e_enabled()

    def test_get(self):
        self.app.container.binder.bind(Application, self.app)

        app = self.app.get(Application)

        assert app == self.app

    def test_register_module(self):

        self.app.register_module(SimpleModule)

        assert self.app.get(SimpleModule).name == "SimpleModule"

    def test_register_routes(self):
        self.app.init_e2e()
        self.app.register_routes(
            {
                "home": BasePage,
            }
        )

        assert self.app.router.get_page(self.app, "home") is not None

    def test_go_to(self):
        self.app.init_e2e()

        dashboard_page = self.app.go_to("dashboard")

        assert dashboard_page is not None


class SimpleModule(Module):
    name: str

    def bootstrap(self):
        self.name = "SimpleModule"
