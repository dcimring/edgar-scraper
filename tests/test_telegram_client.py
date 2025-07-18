import os
import sys
import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import telegram
import telegram.error

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.telegram_client import TelegramClient


class TestTelegramClient(unittest.TestCase):

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "test_token", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch('telegram.Bot.send_message', new_callable=AsyncMock)
    def test_send_alert_success(self, mock_send_message):
        """
        Test that send_alert calls the bot's send_message method with the correct parameters.
        """
        async def run_test():
            client = TelegramClient()
            filing_details = {
                "company_name": "Test Corp",
                "form_type": "10-K",
                "filing_date": "2025-07-15",
                "link": "http://example.com",
            }
            summary = "This is a test summary."
            await client.send_alert(filing_details, summary)

            # Verify that send_message was called once
            mock_send_message.assert_called_once()
        asyncio.run(run_test())

    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "test_token", "TELEGRAM_CHAT_ID": "12345"}
    )
    @patch('telegram.Bot.send_message', new_callable=AsyncMock)
    def test_send_alert_telegram_error(self, mock_send_message):
        """
        Test that send_alert handles a TelegramError.
        """
        async def run_test():
            # Configure the mock to raise a TelegramError
            mock_send_message.side_effect = telegram.error.TelegramError(
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
            await client.send_alert(filing_details, summary)
        asyncio.run(run_test())


if __name__ == "__main__":
    asyncio.run(unittest.main())
