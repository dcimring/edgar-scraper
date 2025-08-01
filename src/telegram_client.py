import logging
import os

import telebot
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
        self.bot = telebot.TeleBot(bot_token)

    def send_sec_alert(self, filing_details: dict, summary: str):
        """
        Sends a formatted alert message to the configured Telegram chat.

        Args:
            filing_details: A dictionary containing filing details like company name, form type, etc.
            summary: The summary of the crypto-related content from the LLM.
        """
        company_name = filing_details.get('company_name', 'N/A')
        form_type = filing_details.get('form_type', 'N/A')
        filing_date = filing_details.get('filing_date', 'N/A')
        link = filing_details.get('link', 'N/A')

        message = f"""🚨 *New Crypto Filing Alert* 🚨

*Company*: {company_name}
*Form*: {form_type}
*Date*: {filing_date}
*Link*: [{link}]({link})

*Snippet*: {summary}
        """
        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="Markdown",
            )
            logging.info(
                f"Successfully sent alert for {filing_details.get('company_name')}"
            )
        except Exception as e:
            logging.error(f"Error sending Telegram alert: {e}")

    def send_aave_alert(self, apy_rates: dict):
        """
        Sends a formatted alert message with Aave APY rates.

        Args:
            apy_rates: A dictionary with stablecoin tickers as keys and their APY rates as values.
        """
        message = f"""📊 *Daily Aave APY Rates* 📊

*USDT*: {apy_rates.get('USDT', 'N/A')}
*USDC*: {apy_rates.get('USDC', 'N/A')}
*DAI*: {apy_rates.get('DAI', 'N/A')}
        """
        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="Markdown",
            )
            logging.info("Successfully sent Aave APY rates alert.")
        except Exception as e:
            logging.error(f"Error sending Aave APY rates alert: {e}")


if __name__ == "__main__":
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
    client.send_sec_alert(sample_filing, summary)

    aave_rates = {
        'USDT': '1.23%',
        'USDC': '0.87%',
        'DAI': '0.55%'
    }
    client.send_aave_alert(aave_rates)