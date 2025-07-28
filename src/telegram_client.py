import logging
import os

import telegram
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TelegramClient:
    """
    A client for sending messages to a Telegram chat.
    """

    def __init__(self):
        """
        Initializes the TelegramClient, configuring the bot.
        """
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not bot_token or not self.chat_id:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables not set."
            )
        self.bot = telegram.Bot(token=bot_token)

    def _escape_markdown_v2(self, text: str) -> str:
        """
        Helper function to escape special characters for MarkdownV2.
        """
        escape_chars = '_*[]()~`>#+-=|{}.!'
        return "".join(['\\' + char if char in escape_chars else char for char in text])

    async def send_alert(self, filing_details: dict, summary: str):
        """
        Sends a formatted alert message to the configured Telegram chat.

        Args:
            filing_details: A dictionary containing filing details like company name, form type, etc.
            summary: The summary of the crypto-related content from the LLM.
        """
        company_name = self._escape_markdown_v2(filing_details.get('company_name', 'N/A'))
        form_type = self._escape_markdown_v2(filing_details.get('form_type', 'N/A'))
        filing_date = self._escape_markdown_v2(filing_details.get('filing_date', 'N/A'))
        link = self._escape_markdown_v2(filing_details.get('link', 'N/A'))
        summary = self._escape_markdown_v2(summary)

        message = f"""🚨 *New Crypto Filing Alert\\!* 🚨

*Company*: {company_name}
*Form*: {form_type}
*Date*: {filing_date}
*Link*: [{link}]({link})

*Snippet*: {summary}
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
            )
            logging.info(
                f"Successfully sent alert for {filing_details.get('company_name')}"
            )
        except telegram.error.TelegramError as e:
            logging.error(f"Error sending Telegram alert: {e}")


if __name__ == "__main__":
    async def main():
        # This is an example of how to use the TelegramClient.
        # You would need to have a .env file with your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.
        client = TelegramClient()
        sample_filing = {
            'company_name': 'Example Corp',
            'form_type': '8-K',
            'filing_date': '2025-07-14',
            'link': 'https://www.sec.gov/example-filing'
        }
        summary = "This is a test summary."
        await client.send_alert(sample_filing, summary)

    import asyncio
    asyncio.run(main())
