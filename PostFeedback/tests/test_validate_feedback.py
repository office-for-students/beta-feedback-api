import json
import unittest

from feedback_test_utils import get_string
from validators import validate_feedback
from SharedCode.exceptions import ValidationError


class TestValidateFeedback(unittest.TestCase):
    def test_with_too_long_feedback(self):
        feedback_too_long = json.loads(get_string("fixtures/feedback_4001_chars.json"))
        with self.assertRaises(ValidationError):
            validate_feedback(feedback_too_long)

    def test_with_4000_char_feedback(self):
        feedback_too_long = json.loads(get_string("fixtures/feedback_4000_chars.json"))
        try:
            validate_feedback(feedback_too_long)
        except ValidationError:
            self.fail("validate_feedback raised unexpected ValidationError")

    def test_with_valid_feedback(self):
        success = True
        valid_feedback = json.loads(get_string("fixtures/valid_feedback.json"))
        try:
            validate_feedback(valid_feedback)
        except ValidationError:
            success = False

        # Check we
        self.assertTrue(success, "Failed valid feedback")


# TODO add more tests
