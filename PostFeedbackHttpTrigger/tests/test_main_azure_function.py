
import json
import unittest
from unittest import mock

import azure.functions as func

from feedback_test_utils import get_string
from PostFeedbackHttpTrigger import main


class TestMainAzureFunction(unittest.TestCase):
    @mock.patch("feedback_creator.utils.get_collection_link")
    @mock.patch("feedback_creator.utils.get_cosmos_client")
    def test_with_missing_mandatory_param(self, mock_get_collection_link, mock_get_cosmos_client):


        invalid_feedback_body = get_string('fixtures/missing_is_useful.json')
        invalid_feedback_body = bytearray(invalid_feedback_body, 'utf8')
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="POST",
            body=invalid_feedback_body,
            url=f"/api/",
        )

        # Call the main Azure Function entry point with the request.
        resp = main(req)

        # Check status code
        self.assertEqual(resp.status_code, 400)

"""
        # Check content type
        headers = dict(resp.headers)
        self.assertEqual(headers["content-type"], "application/json")

        # Do some checking of the returned error message.
        error_msg = json.loads(resp.get_body().decode("utf-8"))
        self.assertEqual(error_msg["errors"][0]["error"], "Bad Request")
        self.assertEqual(
            error_msg["errors"][0]["error_values"][0]["Parameter Error"],
            "Invalid parameter passed",
        )
"""


# TODO add more tests
