import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sec_client import SecEdgarClient

# Load environment variables for tests
load_dotenv()

class TestSecEdgarClient(unittest.TestCase):

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com"})

    @patch("src.sec_client.requests.get")
    def test_get_latest_filings_success(self, mock_get):
        """
        Test that get_latest_filings successfully parses a valid RSS feed.
        """
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>8-K - Example Corp (0001234567)</title>
    <link href="https://www.sec.gov/Archives/edgar/data/1234567/0001234567-25-000001-index.html"/>
    <summary>Report of unscheduled material events or corporate changes.</summary>
    <published>2025-07-14T10:00:00-04:00</published>
  </entry>
</feed>"""
        mock_get.return_value = mock_response

        client = SecEdgarClient()
        filings = client.get_latest_filings()

        self.assertEqual(len(filings), 1)
        self.assertEqual(filings[0]["title"], "8-K - Example Corp (0001234567)")
        self.assertEqual(
            filings[0]["link"],
            "https://www.sec.gov/Archives/edgar/data/1234567/0001234567-25-000001-index.html",
        )

    @patch("src.sec_client.requests.get")
    def test_get_latest_filings_request_error(self, mock_get):
        """
        Test that get_latest_filings handles a request exception.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        client = SecEdgarClient()
        filings = client.get_latest_filings()

        self.assertEqual(len(filings), 0)

    @patch("src.sec_client.requests.get")
    def test_get_latest_filings_parsing_error(self, mock_get):
        """
        Test that get_latest_filings handles an RSS parsing error.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<xml>invalid</xml>"  # Malformed XML
        mock_get.return_value = mock_response

        client = SecEdgarClient()
        filings = client.get_latest_filings()

        self.assertEqual(len(filings), 0)

    @patch("src.sec_client.requests.get")
    def test_get_full_filing_text_success(self, mock_get):
        """
        Test that get_full_filing_text successfully extracts text from a filing.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "This is the full filing text."
        mock_get.return_value = mock_response

        client = SecEdgarClient()
        # Use a realistic SEC filing index URL for testing
        filing_url = "https://www.sec.gov/Archives/edgar/data/1234567/000123456725000001/0001234567-25-000001-index.htm"
        text = client.get_full_filing_text(filing_url)

        self.assertEqual(text, "This is the full filing text.")
        # Verify that requests.get was called with the correct .txt URL
        expected_doc_url = "https://www.sec.gov/Archives/edgar/data/1234567/000123456725000001/0001234567-25-000001.txt"
        mock_get.assert_called_once_with(expected_doc_url, headers=client.headers, timeout=10)

    @patch("src.sec_client.requests.get")
    def test_get_full_filing_text_request_error(self, mock_get):
        """
        Test that get_full_filing_text handles a request exception.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        client = SecEdgarClient()
        filing_url = "https://www.sec.gov/Archives/edgar/data/1234567/0001234567-25-000001-index.htm"
        text = client.get_full_filing_text(filing_url)

        self.assertIsNone(text)

    @patch("src.sec_client.requests.get")
    def test_get_full_filing_text_invalid_url(self, mock_get):
        """
        Test that get_full_filing_text handles an invalid filing URL format.
        """
        client = SecEdgarClient()
        filing_url = "https://www.sec.gov/invalid/url"
        text = client.get_full_filing_text(filing_url)

        self.assertIsNone(text)
        mock_get.assert_not_called() # Ensure no request is made for invalid URL


if __name__ == "__main__":
    unittest.main()
