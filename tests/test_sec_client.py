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
        # Mock the response for the index page
        mock_index_response = MagicMock()
        mock_index_response.status_code = 200
        mock_index_response.content = b"""
            <html><body>
                <a href="/Archives/edgar/data/1234567/0001234567-25-000001/filing-document.htm">filing-document.htm</a>
            </body></html>
        """

        # Mock the response for the filing document
        mock_doc_response = MagicMock()
        mock_doc_response.status_code = 200
        mock_doc_response.content = (
            b"<html><body><p>This is the filing text.</p></body></html>"
        )

        # Set the side_effect to return the appropriate mock response
        mock_get.side_effect = [mock_index_response, mock_doc_response]

        client = SecEdgarClient()
        text = client.get_full_filing_text("http://example.com/index.html")

        self.assertEqual(text, "This is the filing text.")


if __name__ == "__main__":
    unittest.main()
