from transstellar.framework import BasePage, BaseUITest


class TestBasePage(BaseUITest):
    def test_constructor(self):
        page = BasePage(self.app)

        assert page is not None

    def test_get_page(self):
        page = BasePage(self.app)

        fake_page = page.get_page(FakePage)

        assert isinstance(fake_page, FakePage)

    def test_get_page_from_module(self):
        page = BasePage(self.app)

        fake_page = page.get_page_from_module(
            "tests.unit.framework.test_base_page", "FakePage"
        )

        assert isinstance(fake_page, FakePage)

    def test_get_current_url(self):
        url = "https://github.com/"

        self.app.driver.get(url)

        page = BasePage(self.app)

        assert page.get_current_url().geturl() == url


class FakePage(BasePage):
    pass
