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
            {
                "dashboard": Route("/dashboard", BasePage),
                "user_list": Route("/users", BasePage),
            }
        )

        self.router.register_routes(
            {
                "project_list": Route("/projects", BasePage),
            }
        )

        assert self.router.get_route("dashboard") is not None
        assert self.router.get_route("user_list") is not None
        assert self.router.get_route("project_list") is not None

    def test_register_route(self):
        self.router.register_route("home", Route("/", BasePage))
        page = self.router.get_page("home")

        assert isinstance(page, BasePage)

    def test_get_page_will_be_empty_when_route_is_not_found(self):
        page = self.router.get_page("fake_page")

        assert page is None

    def test_get_page_will_get_page_when_route_is_found(self):
        self.router.register_route("fake_page", Route("/", BasePage))

        page = self.router.get_page("fake_page")

        assert isinstance(page, BasePage)
