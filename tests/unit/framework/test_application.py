import pytest

from transstellar.framework.application import Application
from transstellar.framework.base_page import BasePage
from transstellar.framework.module import Module
from transstellar.framework.route import Route


class User:
    pass


class TestApplication:
    app: Application

    @pytest.fixture(autouse=True)
    def setup_method_test(self, request, testrun_uid):
        params = {
            "request": request,
            "testrun_uid": testrun_uid,
            "routes": [
                Route("/enterprise", "enterprise", BasePage),
                Route("/projects/{project_id}", "project_detail", BasePage),
            ],
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
            [
                Route("/", "home", BasePage),
            ]
        )

        assert self.app.router.get_page("home") is not None

    def test_go_to(self):
        self.app.init_e2e()

        self.app.go_to("enterprise")

        path = self.app.get_current_url().path

        assert path == "/enterprise"

    def test_go_to_with_path_params(self):
        self.app.init_e2e()

        self.app.go_to("project_detail", {"project_id": 1})

        path = self.app.get_current_url().path

        assert path == "/projects/1"

    def test_get_page(self):
        self.app.init_e2e()

        enterprise_page = self.app.get_page("enterprise")

        assert enterprise_page is not None

    def test_is_logged_in(self):
        self.app.init_e2e()
        user = User()

        self.app.set_current_user(user)

        assert self.app.is_logged_in()
        assert user == self.app.get_current_user()


class SimpleModule(Module):
    name: str

    def bootstrap(self):
        self.name = "SimpleModule"
