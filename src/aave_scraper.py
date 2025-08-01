import logging
import os
import re
from typing import Dict, Optional

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AaveScraper:
    """
    A client for scraping APY rates from Aave.
    """

    def __init__(self):
        self.aave_url = os.getenv('AAVE_URL', 'https://app.aave.com/')
        user_agent = os.getenv('USER_AGENT', 'BlackHatMedia/1.0 (daniel@blackhatmedia.com)')
        from_email = os.getenv('FROM_EMAIL', 'daniel@blackhatmedia.com')
        self.headers = {'User-Agent': user_agent, 'From': from_email}

    def get_apy_rates(self) -> Dict[str, Optional[str]]:
        """
        Retrieves APY rates for USDT, USDC, and DAI from Aave.

        Returns:
            A dictionary with stablecoin tickers as keys and their APY rates as values.
            Returns None for a stablecoin if its APY cannot be found.
        """
        apy_rates = {'USDT': None, 'USDC': None, 'DAI': None}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=self.headers['User-Agent'])
            try:
                page.goto(self.aave_url)
                
                # Wait for the elements to be present
                page.wait_for_selector('[data-cy^="marketListItemListItem_"]', timeout=20000)

                soup = BeautifulSoup(page.content(), 'html.parser')

                for ticker in apy_rates.keys():
                    # Find the parent div for the asset
                    asset_div = soup.find('div', attrs={'data-cy': f'marketListItemListItem_{ticker}'})
                    if asset_div:
                        # Find the APY within this asset's div
                        apy_element = asset_div.find('p', attrs={'data-cy': 'apy'})
                        if apy_element:
                            apy_rates[ticker] = apy_element.get_text(strip=True)

            except Exception as e:
                logging.error(f"Error scraping Aave APY rates with Playwright: {e}")
            finally:
                browser.close()
        return apy_rates

if __name__ == '__main__':
    scraper = AaveScraper()
    rates = scraper.get_apy_rates()
    print(rates)