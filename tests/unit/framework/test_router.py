import pytest

from transstellar.framework import BasePage, BaseUITest, Router
from transstellar.framework.route import Route


class TestRouter(BaseUITest):
    router: Router

    @pytest.fixture(autouse=True)
    def setup_method_test(self):
        self.router = Router(self.app)

    def test_constructor(self):
        assert self.router is not None
        assert self.router.routes is not None

    def test_register_routes(self):
        self.router.register_routes(
            [
                Route("/dashboard", "dashboard", BasePage),
                Route("/users", "user_list", BasePage),
            ]
        )

        self.router.register_routes(
            {
                Route("/projects", "project_list", BasePage),
            }
        )

        assert self.router.get_route("dashboard") is not None
        assert self.router.get_route("user_list") is not None
        assert self.router.get_route("project_list") is not None

    def test_register_route(self):
        self.router.register_route(Route("/projects", "project_list", BasePage))
        page = self.router.get_page("project_list")

        assert isinstance(page, BasePage)

    def test_get_dynamic_route(self):
        self.router.register_route(
            Route("/projects/{project_id}", "project_list", BasePage)
        )
        page = self.router.go_to("project_list", {"project_id": 1})

        assert isinstance(page, BasePage)

    def test_get_page_will_fail_when_route_is_not_found(self):
        try:
            self.router.get_page("fake_page")
        except LookupError:
            assert True
