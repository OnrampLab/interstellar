from transstellar.framework import BasePage, BaseUITest, Route


class TestBasePage(BaseUITest):
    def test_constructor(self):
        page = BasePage(self.app)

        assert page is not None

    def test_land(self):
        self.app.register_routes({"home": Route("/", FakePage)})
        page = FakePage(self.app)

        page.land()

        assert self.app.get_current_url().path == "/"


class FakePage(BasePage):
    route_key = "home"
