import logging
import time
from urllib.parse import urlparse


from src.database import Database
from src.llm_client import LlmClient
from src.sec_client import SecEdgarClient
from src.telegram_client import TelegramClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """
    Main function to run the SEC EDGAR Crypto Alert Service.
    """
    sec_client = SecEdgarClient()
    llm_client = LlmClient()
    telegram_client = TelegramClient()
    db = Database()

    while True:
        logging.info("Checking for new SEC filings...")
        latest_filings = sec_client.get_latest_filings()

        for filing in latest_filings:
            filing_id = extract_filing_id(filing["link"])
            if not db.filing_exists(filing_id):
                logging.info(f"Processing new filing: {filing['title']}")
                full_text = sec_client.get_full_filing_text(filing["link"])

                if full_text:
                    analysis = llm_client.analyze_filing(full_text)
                    if analysis["crypto_detected"]:
                        filing_details = {
                            "company_name": filing["title"].split(" - ")[1],
                            "form_type": filing["title"].split(" - ")[0],
                            "filing_date": filing["published"],
                            "link": filing["link"],
                        }
                        telegram_client.send_alert(filing_details, analysis["summary"])
                    db.add_filing(filing_id)
                else:
                    logging.warning(
                        f"Could not retrieve full text for {filing['link']}"
                    )
            else:
                logging.info(f"Skipping already processed filing: {filing['title']}")

        logging.info("Waiting for the next check...")
        time.sleep(300)  # Wait for 5 minutes


def extract_filing_id(url: str) -> str:
    """
    Extracts the accession number from the filing URL to use as a unique ID.
    Example: https://www.sec.gov/Archives/edgar/data/1234567/0001234567-25-000001-index.html -> 0001234567-25-000001
    """
    path = urlparse(url).path
    return path.split("/")[-1].replace("-index.html", "")


if __name__ == "__main__":
    main()
