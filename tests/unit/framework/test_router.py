import pytest

from transstellar.framework import BasePage, BaseUITest, Router


class TestRouter(BaseUITest):
    router: Router

    @pytest.fixture(autouse=True)
    def setup_method_test(self):
        self.router = Router()

    def test_constructor(self):
        assert self.router is not None
        assert self.router.routes is not None

    def test_register_routes(self):
        self.router.register_routes(
            {
                "dashboard": BasePage,
            }
        )

        assert self.router.routes.get("dashboard") is not None

    def test_register_route(self):
        self.router.register_route("home", BasePage)

        assert self.router.routes.get("home") is not None

    def test_get_page_will_be_empty_when_route_is_not_found(self):
        page = self.router.get_page(self.app, "fake_page")

        assert page is None

    def test_get_page_will_get_page_when_route_is_found(self):
        self.router.register_route("fake_page", BasePage)

        page = self.router.get_page(self.app, "fake_page")

        assert isinstance(page, BasePage)
