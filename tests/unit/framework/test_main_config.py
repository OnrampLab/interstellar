from transstellar.framework import BaseUITest, MainConfig
from transstellar.framework.config_service import ConfigService


class TestMainConfig(BaseUITest):
    main_config: MainConfig

    def setup_method(self):
        config_service = ConfigService()
        self.main_config = MainConfig(config_service)

    def test_get_app_url(self):
        app_url = self.main_config.get_app_url()

        assert app_url == "https://github.com"

    def test_get_api_url(self):
        api_url = self.main_config.get_api_url()

        assert api_url == "https://api.github.com"
