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


# TODO add more tests
