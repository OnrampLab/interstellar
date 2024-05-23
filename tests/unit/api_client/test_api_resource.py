import os
from datetime import datetime

from transstellar.api_client import APIResource
from transstellar.api_client.api_client import APIClient


class TestAPIResource:
    def setup_method(self):
        self.token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.api_client = APIClient("https://api.github.com")
        self.api_client.as_token(self.token)
        self.issue_comment = APIResource(
            "repos/OnrampLab/transstellar/issues/1/comments", self.api_client
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
        json = self.issue_comment.create(payload)

        assert json["body"].startswith("test comment - ")

        return json["id"]

    def delete_comment(self):
        self.issue_comment.delete(
            self.comment_id, "repos/OnrampLab/transstellar/issues/comments"
        )

    def test_create(self):
        assert self.comment_id is not None

    def test_find(self):
        json = self.issue_comment.find(
            self.comment_id, "repos/OnrampLab/transstellar/issues/comments"
        )

        assert json["id"] == self.comment_id

    def test_update(self):
        payload = {"body": f"test updating comment - {datetime.now()}"}
        json = self.issue_comment.update(
            self.comment_id,
            payload,
            "repos/OnrampLab/transstellar/issues/comments",
        )
        assert json["body"].startswith("test updating comment - ")

    def test_full_update(self):
        payload = {"labels": ["enhancement"]}
        labels_json = self.issue_label.full_update(
            None,
            payload,
            "repos/OnrampLab/transstellar/issues/1/labels",
        )

        assert labels_json[0]["name"] == "enhancement"

        payload = {"labels": []}
        labels_json = self.issue_label.full_update(
            None,
            payload,
            "repos/OnrampLab/transstellar/issues/1/labels",
        )

    def test_delete(self):
        self.delete_comment()

        self.should_delete_comment = False
