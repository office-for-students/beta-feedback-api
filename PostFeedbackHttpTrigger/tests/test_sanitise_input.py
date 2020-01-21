import unittest

from SharedCode.utils import sanitise_url_string, sanitise_question_string


class TestSanitiseUrlString(unittest.TestCase):
    def test_with_permitted_url(self):
        input_url = (
            "https://prod-discover-uni.azurewebsites.net/course-finder/"
            "results/?subject_query=%22Artificial+intelligence%22&institution_query"
            "=&mode_query=Part-time&countries_query=England"
        )
        sanitised_url = sanitise_url_string(input_url)
        self.assertEqual(input_url, sanitised_url)

    def test_with_some_chars_not_permitted(self):
        bad_str = "<script>;"
        expected_sanitised_str = "script"
        sanitised_str = sanitise_url_string(bad_str)
        self.assertEqual(expected_sanitised_str, sanitised_str)


class TestSanitiseQuestionString(unittest.TestCase):
    def test_with_valid_input_str_1(self):
        valid_str = "I like discoveruni. It's really useful! :?& fred@acme.com"
        sanitised_str = sanitise_question_string(valid_str)
        self.assertEqual(valid_str, sanitised_str)

    def test_with_valid_input_str_2(self):
        valid_str = "how_was_this_useful"
        sanitised_str = sanitise_question_string(valid_str)
        self.assertEqual(valid_str, sanitised_str)

    def test_with_some_chars_not_permitted(self):
        bad_str = "<script>;#%="
        expected_sanitised_str = "script"
        sanitised_str = sanitise_question_string(bad_str)
        self.assertEqual(expected_sanitised_str, sanitised_str)


# TODO add more tests
