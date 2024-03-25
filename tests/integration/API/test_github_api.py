import pytest
import requests

from modules.github.github_module import GithubModule
from transstellar.framework import BaseApiTest


class TestGithubAPI(BaseApiTest):
    github_module: GithubModule
    api_base_url: str

    @pytest.fixture(autouse=True)
    def setup_test(self):
        self.github_module = self.app.get(GithubModule)
        self.api_base_url = self.github_module.get_api_url()

    def test_search_users(self):
        search_endpoint = f"{self.api_base_url}/search/users"
        response = requests.get(search_endpoint, params={"q": "john"})

        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) > 0

    def test_get_user(self):
        username = self.github_module.get_test_account().get_username()
        user_endpoint = f"{self.api_base_url}/users/{username}"
        response = requests.get(user_endpoint)

        assert response.status_code == 200
        assert response.json()["login"] == username
