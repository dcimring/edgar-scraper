import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aave_scraper import AaveScraper

class TestAaveScraper(unittest.TestCase):

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('playwright.sync_api.sync_playwright')
    def test_get_apy_rates_success(self, mock_sync_playwright):
        """
        Test that get_apy_rates successfully retrieves APY rates using Playwright.
        """
        mock_playwright = MagicMock()
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
        mock_browser = MagicMock()
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_page = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_page.goto.return_value = None # Mock successful navigation
        mock_page.wait_for_selector.return_value = None # Mock waiting for selector

        # Mock the page.content() to return the HTML content
        mock_page.content.return_value = """
        <html><body>
            <div data-cy="marketListItemListItem_USDT"><p data-cy="apy">1.23%</p></div>
            <div data-cy="marketListItemListItem_USDC"><p data-cy="apy">0.87%</p></div>
            <div data-cy="marketListItemListItem_DAI"><p data-cy="apy">0.55%</p></div>
        </body></html>
        """

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertEqual(rates['USDT'], '1.23%')
        self.assertEqual(rates['USDC'], '0.87%')
        self.assertEqual(rates['DAI'], '0.55%')
        mock_browser.close.assert_called_once() # Ensure browser is closed

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('playwright.sync_api.sync_playwright')
    def test_get_apy_rates_request_error(self, mock_sync_playwright):
        """
        Test that get_apy_rates handles a request exception (simulated by Playwright error).
        """
        mock_playwright = MagicMock()
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
        mock_browser = MagicMock()
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_page = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_page.goto.side_effect = Exception("Playwright error")

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertIsNone(rates['USDT'])
        self.assertIsNone(rates['USDC'])
        self.assertIsNone(rates['DAI'])

    @patch.dict(os.environ, {"USER_AGENT": "test_user_agent", "FROM_EMAIL": "test@example.com", "AAVE_URL": "http://test.aave.com"})
    @patch('playwright.sync_api.sync_playwright')
    def test_get_apy_rates_parsing_error(self, mock_sync_playwright):
        """
        Test that get_apy_rates handles parsing errors (e.g., APY not found).
        """
        mock_playwright = MagicMock()
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
        mock_browser = MagicMock()
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_page = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_page.goto.return_value = None # Mock successful navigation
        mock_page.wait_for_selector.return_value = None # Mock waiting for selector
        mock_page.content.return_value = b"<html><body><p>No APY rates here</p></body></html>"

        scraper = AaveScraper()
        rates = scraper.get_apy_rates()

        self.assertIsNone(rates['USDT'])
        self.assertIsNone(rates['USDC'])
        self.assertIsNone(rates['DAI'])
