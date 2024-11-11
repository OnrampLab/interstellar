import os
from datetime import datetime

from transstellar.api_client import APIClient
from transstellar.framework.base_api_test import BaseApiTest


# pylint: disable=R0801
class TestAPIClient(BaseApiTest):
    def setup_method(self):
        self.token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.api_client = APIClient("https://api.github.com")
        self.api_client.as_token(self.token)
        self.comment_id = self.create_comment()
        self.should_delete_comment = True

    def teardown_method(self):
        if self.should_delete_comment:
            self.delete_comment()

    def create_comment(self):
        payload = {"body": f"test comment - {datetime.now()}"}
        json = self.api_client.post(
            "repos/OnrampLab/transstellar/issues/1/comments", payload
        )

        assert json["body"].startswith("test comment - ")

        return json["id"]

    def delete_comment(self):
        self.api_client.delete(
            f"repos/OnrampLab/transstellar/issues/comments/{self.comment_id}"
        )

    def test_as_token(self):
        assert self.api_client.token is not None

    def test_post(self):
        assert self.comment_id is not None

    def test_get(self):
        json = self.api_client.get(
            f"repos/OnrampLab/transstellar/issues/comments/{self.comment_id}"
        )

        assert json["id"] == self.comment_id

    def test_patch(self):
        payload = {"body": f"test updating comment - {datetime.now()}"}
        json = self.api_client.patch(
            f"repos/OnrampLab/transstellar/issues/comments/{self.comment_id}",
            payload,
        )
        assert json["body"].startswith("test updating comment - ")

    def test_put(self):
        payload = {"labels": ["enhancement"]}
        labels_json = self.api_client.put(
            "repos/OnrampLab/transstellar/issues/1/labels",
            payload,
        )

        assert labels_json[0]["name"] == "enhancement"

        payload = {"labels": []}
        self.api_client.put(
            "repos/OnrampLab/transstellar/issues/1/labels",
            payload,
        )

    def test_delete(self):
        self.delete_comment()

        self.should_delete_comment = False
