from injector import inject

from modules.github.account_config import AccountConfig
from transstellar.framework import ConfigService


class GithubConfigParser:
    @inject
    def __init__(self, config_service: ConfigService):
        self.config = config_service.config

    def get_test_account(self):
        return AccountConfig(self.config["accounts"]["test"])

    def get_api_url(self):
        return self.config["api"]["api_url"]
