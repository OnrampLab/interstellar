from modules.github.github_config_parser import GithubConfigParser
from transstellar.framework.module import Module


class GithubModule(Module):
    github_config_parser: GithubConfigParser

    def bootstrap(self):
        self.logger.info("Github Module!")

        self.github_config_parser = self.app.get(GithubConfigParser)

    def get_api_url(self):
        return self.github_config_parser.get_api_url()

    def get_test_account(self):
        return self.github_config_parser.get_test_account()
