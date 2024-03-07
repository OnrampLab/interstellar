import requests
import pytest
from interstellar.framework import BaseApiTest

@pytest.fixture
def api_base_url():
    return 'https://api.github.com'

class TestGithubAPI(BaseApiTest):

    def test_search_users(self, api_base_url):
        search_endpoint = f'{api_base_url}/search/users'
        response = requests.get(search_endpoint, params={'q': 'john'})

        assert response.status_code == 200
        assert 'items' in response.json()
        assert len(response.json()['items']) > 0

    def test_get_user(self, api_base_url):
        username = 'octocat'  # Replace with a valid GitHub username
        user_endpoint = f'{api_base_url}/users/{username}'
        response = requests.get(user_endpoint)

        assert response.status_code == 200
        assert response.json()['login'] == username
