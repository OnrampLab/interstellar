import os
from datetime import datetime

from transstellar.api_client import APIResource
from transstellar.api_client.api_client import APIClient
from transstellar.framework.base_api_test import BaseApiTest


class TestAPIResource(BaseApiTest):
    def setup_method(self):
        self.token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.api_client = APIClient("https://api.github.com")
        self.api_client.as_token(self.token)
        self.issue_comment = APIResource(
            "repos/OnrampLab/transstellar/issues/{issue_id}/comments/{comment_id}",
            self.api_client,
        )
        self.issue_label = APIResource(
            "repos/OnrampLab/transstellar/issues/1/labels", self.api_client
        )

        self.comment_id = self.create_comment()
        self.should_delete_comment = True

    def teardown_method(self):
        if self.should_delete_comment:
            self.delete_comment()

    def create_comment(self):
        payload = {"body": f"test comment - {datetime.now()}"}
        json = self.issue_comment.create({"issue_id": 1}, payload)

        assert json["body"].startswith("test comment - ")

        return json["id"]

    def delete_comment(self):
        path_params = {"comment_id": self.comment_id}
        self.issue_comment.delete(path_params)

    def test_create(self):
        assert self.comment_id is not None

    def test_find(self):
        path_params = {"comment_id": self.comment_id}
        json = self.issue_comment.find(path_params)

        assert json["id"] == self.comment_id

    def test_list(self):
        path_params = {"issue_id": 1}
        json = self.issue_comment.list(path_params)

        assert len(json) > 0

    def test_update(self):
        payload = {"body": f"test updating comment - {datetime.now()}"}
        path_params = {"comment_id": self.comment_id}
        json = self.issue_comment.update(
            path_params,
            payload,
        )
        assert json["body"].startswith("test updating comment - ")

    def test_full_update(self):
        path_params = {"comment_id": self.comment_id}
        payload = {"labels": ["enhancement"]}
        labels_json = self.issue_label.full_update(
            path_params,
            payload,
        )

        assert labels_json[0]["name"] == "enhancement"

        payload = {"labels": []}
        labels_json = self.issue_label.full_update(
            path_params,
            payload,
        )

    def test_delete(self):
        self.delete_comment()

        self.should_delete_comment = False
