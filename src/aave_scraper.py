import logging
import os
import re
from typing import Dict, Optional

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

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

    async def get_apy_rates(self) -> Dict[str, Optional[str]]:
        """
        Retrieves APY rates for USDT, USDC, and DAI from Aave.

        Returns:
            A dictionary with stablecoin tickers as keys and their APY rates as values.
            Returns None for a stablecoin if its APY cannot be found.
        """
        apy_rates = {'USDT': None, 'USDC': None, 'DAI': None}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=self.headers['User-Agent'])
            try:
                await page.goto(self.aave_url)
                
                # Wait for the elements to be present
                await page.wait_for_selector('[data-cy^="marketListItemListItem_"]', timeout=20000)

                soup = BeautifulSoup(await page.content(), 'html.parser')

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
                await browser.close()
        return apy_rates

if __name__ == '__main__':
    import asyncio
    async def main():
        scraper = AaveScraper()
        rates = await scraper.get_apy_rates()
        print(rates)
    asyncio.run(main())