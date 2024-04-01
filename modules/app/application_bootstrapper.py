from modules.github.github_module import GithubModule
from transstellar.framework import Application
from transstellar.framework.application_bootstrapper import (
    ApplicationBootstrapper as BaseApplicationBootstrapper,
)


class ApplicationBootstrapper(BaseApplicationBootstrapper):
    def bootstrap(self, app: Application):
        app.register_module(GithubModule)
