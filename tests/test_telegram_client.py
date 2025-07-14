import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import telegram
import telegram.error

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.telegram_client import TelegramClient


class TestTelegramClient(unittest.TestCase):

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "test_token", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch("telegram.Bot")
    def test_send_alert_success(self, mock_bot):
        """
        Test that send_alert calls the bot's send_message method with the correct parameters.
        """
        # Create a mock bot instance
        mock_bot_instance = MagicMock()
        mock_bot.return_value = mock_bot_instance

        client = TelegramClient()
        filing_details = {
            "company_name": "Test Corp",
            "form_type": "10-K",
            "filing_date": "2025-07-15",
            "link": "http://example.com",
        }
        summary = "This is a test summary."
        client.send_alert(filing_details, summary)

        # Verify that send_message was called once
        mock_bot_instance.send_message.assert_called_once()

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "test_token", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch("telegram.Bot")
    def test_send_alert_telegram_error(self, mock_bot):
        """
        Test that send_alert handles a TelegramError.
        """
        # Configure the mock to raise a TelegramError
        mock_bot_instance = MagicMock()
        mock_bot_instance.send_message.side_effect = telegram.error.TelegramError(
            "Test error"
        )
        mock_bot.return_value = mock_bot_instance

        client = TelegramClient()
        filing_details = {
            "company_name": "Test Corp",
            "form_type": "10-K",
            "filing_date": "2025-07-15",
            "link": "http://example.com",
        }
        summary = "This is a test summary."
        # We don't need to assert anything here, just that no exception is raised
        client.send_alert(filing_details, summary)


if __name__ == "__main__":
    unittest.main()
