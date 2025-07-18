import logging
import os
from typing import Dict, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SecEdgarClient:
    """
    A client for interacting with the SEC EDGAR system to retrieve company filings.
    """

    SEC_RSS_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=only&start=0&count=100&output=atom"

    def __init__(self):
        """
        Initializes the SecEdgarClient with a User-Agent header.
        """
        user_agent = os.getenv('USER_AGENT', 'BlackHatMedia/1.0 (daniel@blackhatmedia.com)')
        from_email = os.getenv('FROM_EMAIL', 'daniel@blackhatmedia.com')
        self.headers = {'User-Agent': user_agent, 'From': from_email}

    def get_latest_filings(self) -> List[Dict[str, str]]:
        """
        Retrieves the latest filings from the SEC EDGAR RSS feed.

        Returns:
            A list of dictionaries, where each dictionary represents a filing
            and contains details such as title, link, summary, and filing date.
            Returns an empty list if the feed cannot be fetched or parsed.
        """
        try:
            response = requests.get(self.SEC_RSS_URL, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            feed = feedparser.parse(response.content)

            if feed.bozo:
                logging.error(f"Error parsing RSS feed: {feed.bozo_exception}")
                return []

            filings = []
            for entry in feed.entries:
                filings.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "published": entry.get("published"),
                    }
                )
            return filings

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching SEC EDGAR RSS feed: {e}")
            return []

    def get_full_filing_text(self, filing_url: str) -> Optional[str]:
        """
        Retrieves the full text of a filing from its URL.

        Args:
            filing_url: The URL of the filing's index page.

        Returns:
            The full text of the filing, or None if it cannot be retrieved.
        """
        try:
            parsed_url = urlparse(filing_url)
            path_parts = parsed_url.path.split('/')
            if len(path_parts) < 7: # Ensure there are enough parts for CIK and accession number
                logging.warning(f"Invalid filing URL format: {filing_url}")
                return None

            cik = path_parts[4]
            accession_no_dashes = path_parts[5]
            accession_no_with_dashes = path_parts[6].replace('-index.htm', '')

            # Construct the full URL for the .txt document
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/{accession_no_with_dashes}.txt"

            # Fetch the document content
            doc_response = requests.get(doc_url, headers=self.headers, timeout=10)
            doc_response.raise_for_status()

            return doc_response.text

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching filing text from {filing_url}: {e}")
            return None


if __name__ == "__main__":
    client = SecEdgarClient()
    latest_filings = client.get_latest_filings()
    if latest_filings:
        for filing in latest_filings:
            print(f"Title: {filing['title']}")
            print(f"Link: {filing['link']}")
            print(f"Published: {filing['published']}")
            print("-" * 20)
