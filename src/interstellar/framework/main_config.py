from injector import inject

from .config_service import ConfigService


class MainConfig:
    @inject
    def __init__(self, config_service: ConfigService):
        self.config = config_service.config

    def get_api_url(self):
        return self.config["api"]["api_url"]
