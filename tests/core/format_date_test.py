from stadsarkiv_client.core.dynamic_settings import init_settings
from stadsarkiv_client.core.logging import get_log
import unittest
from unittest.mock import patch
from stadsarkiv_client.core.date_format import timezone_alter, date_format, date_format_day, _sanitize_date_string

init_settings()
log = get_log()


class TestDateFunctions(unittest.TestCase):

    @patch("stadsarkiv_client.core.date_format.log")
    def test_timezone_alter(self, mock_log):
        self.assertEqual(timezone_alter("2024-11-19 11:25:58", "Europe/Copenhagen"), "2024-11-19 12:25:58")
        self.assertEqual(timezone_alter("invalid-date", "Europe/Copenhagen"), "invalid-date")
        mock_log.exception.assert_called_once_with("Error in timezone_alter")

    @patch("stadsarkiv_client.core.date_format.log")
    def test_date_format(self, mock_log):
        self.assertEqual(date_format("2024-11-19T11:25:58"), "19. november 2024 11:25")
        self.assertEqual(date_format("invalid-date"), "invalid-date")
        mock_log.exception.assert_called_once_with("Error in date_format")

    @patch("stadsarkiv_client.core.date_format.log")
    def test_date_format_day(self, mock_log):
        self.assertEqual(date_format_day("2024-11-19"), "19. november 2024")
        self.assertEqual(date_format_day("invalid-date"), "invalid-date")
        mock_log.exception.assert_called_once_with("Error in date_format_day")

    def test_sanitize_date_string(self):
        # With microseconds
        self.assertEqual(_sanitize_date_string("2024-11-19T11:25:58.123456"), "2024-11-19T11:25:58")

        # Without microseconds
        self.assertEqual(_sanitize_date_string("2024-11-19T11:25:58"), "2024-11-19T11:25:58")

        # No dot present
        self.assertEqual(_sanitize_date_string("2024-11-19 11:25:58"), "2024-11-19 11:25:58")


if __name__ == "__main__":
    unittest.main()
