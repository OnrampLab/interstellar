from modules.github.github_module import GithubModule
from transstellar.framework import Application


class ApplicationBootstrapper:
    def create_app(self, request, testrun_uid):
        application = Application(request, testrun_uid)

        application.register_module(GithubModule)

        return application
