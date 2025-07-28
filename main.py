import logging
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse


from src.database import Database
from src.keyword_analyzer import KeywordAnalyzer
from src.sec_client import SecEdgarClient
from src.telegram_client import TelegramClient
from src.aave_scraper import AaveScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    """
    Main function to run the SEC EDGAR Crypto Alert Service.
    """
    sec_client = SecEdgarClient()
    keyword_analyzer = KeywordAnalyzer()
    telegram_client = TelegramClient()
    aave_scraper = AaveScraper()
    db = Database()

    last_apy_alert_time = None # Initialize to None to send alert on first run

    while True:
        current_time = datetime.now()

        # Check for daily Aave APY alert
        if last_apy_alert_time is None or (current_time - last_apy_alert_time) >= timedelta(days=1):
            logging.info("Sending daily Aave APY alert...")
            apy_rates = await aave_scraper.get_apy_rates()
            if apy_rates:
                message = f"""📊 Daily Aave APY Rates 📊\n\nUSDT: {apy_rates.get('USDT', 'N/A')}\nUSDC: {apy_rates.get('USDC', 'N/A')}\nDAI: {apy_rates.get('DAI', 'N/A')}\n\n(Rates as of {current_time.strftime('%Y-%m-%d %H:%M:%S')})"""
                await telegram_client.send_alert({'company_name': 'Aave APY Rates', 'form_type': 'Daily Alert', 'filing_date': current_time.strftime('%Y-%m-%d'), 'link': aave_scraper.aave_url}, message)
                last_apy_alert_time = current_time
            else:
                logging.warning("Could not retrieve Aave APY rates.")

        logging.info("Checking for new SEC filings...")
        latest_filings = sec_client.get_latest_filings()

        for filing in latest_filings:
            filing_id = extract_filing_id(filing["link"])
            if not db.filing_exists(filing_id):
                logging.info(f"Processing new filing: {filing['title']}")
                full_text = sec_client.get_full_filing_text(filing["link"])

                if full_text:
                    analysis = keyword_analyzer.analyze_filing(full_text)
                    if analysis["crypto_detected"]:
                        filing_details = {
                            "company_name": filing["title"].split(" - ")[1],
                            "form_type": filing["title"].split(" - ")[0],
                            "filing_date": filing["published"] if filing["published"] is not None else "N/A",
                            "link": filing["link"],
                        }
                        await telegram_client.send_alert(filing_details, analysis["summary"][:200])
                    db.add_filing(filing_id)
                else:
                    logging.warning(
                        f"Could not retrieve full text for {filing['link']}"
                    )
            else:
                logging.info(f"Skipping already processed filing: {filing['title']}")

        logging.info("Waiting for the next check...")
        await asyncio.sleep(300)  # Wait for 5 minutes


def extract_filing_id(url: str) -> str:
    """
    Extracts the accession number from the filing URL to use as a unique ID.
    Example: https://www.sec.gov/Archives/edgar/data/1234567/0001234567-25-000001-index.html -> 0001234567-25-000001
    """
    path = urlparse(url).path
    return path.split("/")[-1].replace("-index.html", "").replace("-index.htm", "")


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
