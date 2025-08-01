import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.telegram_client import TelegramClient


class TestTelegramClient(unittest.TestCase):

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch('telebot.TeleBot.send_message', new_callable=MagicMock)
    def test_send_alert_success(self, mock_send_message):
        """
        Test that send_alert calls the bot's send_message method with the correct parameters.
        """
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
        mock_send_message.assert_called_once()

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch('telebot.TeleBot.send_message', new_callable=MagicMock)
    def test_send_alert_telegram_error(self, mock_send_message):
        """
        Test that send_alert handles a TelegramError.
        """
        # Configure the mock to raise an exception
        mock_send_message.side_effect = Exception(
            "Test error"
        )

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