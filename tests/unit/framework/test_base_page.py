from transstellar.framework import BasePage, BaseUITest


class TestBasePage(BaseUITest):
    def test_constructor(self):
        page = BasePage(self.app)

        assert page is not None
