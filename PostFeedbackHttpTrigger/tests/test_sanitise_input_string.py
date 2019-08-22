import unittest

from SharedCode.utils import sanitise_input_string


class TestSanitiseInputString(unittest.TestCase):
    def test_with_valid_encoded_url(self):
        input_url = "https://prod-discover-uni.azurewebsites.net/course-finder/results/?subject_query=%22Artificial+intelligence%22&institution_query=&mode_query=Part-time&countries_query=England"
        sanitised_url = sanitise_input_string(input_url)
        self.assertEqual(input_url, sanitised_url)

    def test_with_some_chars_not_permitted(self):
        input_str = "<script>;"
        expected_sanitised_str = "script"
        sanitised_str = sanitise_input_string(input_str)
        self.assertEqual(expected_sanitised_str, sanitised_str)


# TODO add more tests
