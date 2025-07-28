import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import requests

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aave_scraper import AaveScraper

class TestAaveScraper(unittest.TestCase):

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('src.aave_scraper.requests.get')
    def test_get_apy_rates_success(self, mock_get):
        """
        Test that get_apy_rates successfully retrieves APY rates.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        # This HTML is a simplified representation. You'll need to adjust based on actual Aave HTML.
        mock_response.content = b"""
        <html><body>
            <div class="MuiBox-root css-1d0y800"><p>USDT</p><p>1.23%</p></div>
            <div class="MuiBox-root css-1d0y800"><p>USDC</p><p>0.87%</p></div>
            <div class="MuiBox-root css-1d0y800"><p>DAI</p><p>0.55%</p></div>
        </body></html>
        """
        mock_get.return_value = mock_response

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertEqual(rates['USDT'], '1.23%')
        self.assertEqual(rates['USDC'], '0.87%')
        self.assertEqual(rates['DAI'], '0.55%')

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('src.aave_scraper.requests.get')
    def test_get_apy_rates_request_error(self, mock_get):
        """
        Test that get_apy_rates handles a request exception.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertIsNone(rates['USDT'])
        self.assertIsNone(rates['USDC'])
        self.assertIsNone(rates['DAI'])

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('src.aave_scraper.requests.get')
    def test_get_apy_rates_parsing_error(self, mock_get):
        """
        Test that get_apy_rates handles parsing errors (e.g., APY not found).
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body><p>No APY rates here</p></body></html>"
        mock_get.return_value = mock_response

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertIsNone(rates['USDT'])
        self.assertIsNone(rates['USDC'])
        self.assertIsNone(rates['DAI'])

if __name__ == '__main__':
    unittest.main()
