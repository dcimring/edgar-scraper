1. Introduction


  This document outlines the requirements for a new feature to periodically scrape APY (Annual Percentage Yield) rates for selected stablecoins from the Aave platform and dispatch them as
  a Telegram alert. This aims to provide stakeholders with timely updates on decentralized finance (DeFi) lending rates.

  2. Functional Requirements


   * FR-001: Daily APY Rate Retrieval: The system shall attempt to retrieve the current supply APY rates for USDT, USDC, and DAI once every 24 hours. The exact time of day for this retrieval
     shall be configurable (e.g., via an environment variable).
   * FR-002: Aave Data Source: The system shall target the Aave V3 Ethereum market page (https://app.aave.com/) as the source for APY rates.
   * FR-003: APY Data Extraction: For each of the specified stablecoins (USDT, USDC, DAI), the system shall identify and extract its numerical supply APY value.
       * If a stablecoin's APY data cannot be found or extracted, it should be noted as "N/A" or similar in the alert.
   * FR-004: Telegram Alert Generation: The system shall generate a concise Telegram alert message containing the retrieved APY rates. The message format shall clearly label each stablecoin
     and its corresponding APY.
       * Example format:

   1         📊 Daily Aave APY Rates 📊
   2
   3         USDT: X.XX%
   4         USDC: Y.YY%
   5         DAI: Z.ZZ%
   6
   7         (Rates as of [Timestamp])

   * FR-005: Telegram Alert Dispatch: The generated APY alert message shall be sent to the pre-configured Telegram chat using the existing TelegramClient module.

  3. Non-Functional Requirements


   * NFR-001: Reliability: The APY retrieval process shall be robust to temporary network issues or Aave website loading delays. It shall implement appropriate retry mechanisms for web
     requests.
   * NFR-002: Error Handling: All errors encountered during web scraping (e.g., page not found, parsing issues), data extraction, or Telegram dispatch shall be logged with sufficient detail
     for debugging.
   * NFR-003: Maintainability: The web scraping logic shall be encapsulated within a dedicated, separate module to promote modularity and ease of maintenance.
   * NFR-004: Configurability: The Aave URL and the daily alert time (e.g., hour of day) shall be configurable via environment variables.
   * NFR-005: Performance: The daily APY retrieval and alert process should complete within a reasonable timeframe (e.g., under 60 seconds) to avoid impacting other scheduled tasks.
   * NFR-006: Security: API keys (Telegram) and any potential future Aave API keys shall continue to be handled securely via environment variables.

  4. Technical Architecture Overview


   * New Module: A new Python module, src/aave_scraper.py, will be created to handle the logic for fetching and parsing the Aave page.
   * Scraping Strategy:
       * The initial approach will involve using requests to fetch the Aave page content and BeautifulSoup to parse the HTML.
       * Consideration: Aave is a Single-Page Application (SPA) that heavily relies on JavaScript to render its content. Direct requests and BeautifulSoup might not retrieve the fully
         rendered page. If this proves to be the case, a headless browser solution (e.g., selenium or playwright) will be considered as an alternative, which would introduce additional
         dependencies and complexity.
   * Scheduling: The daily execution of the APY alert will be integrated into the main.py application loop. A mechanism to track the last successful APY alert dispatch time will be
     implemented to ensure it runs only once per day.
   * Data Flow:
       1. main.py (or a new scheduler component) triggers aave_scraper.py daily.
       2. aave_scraper.py fetches and parses the Aave page, extracts APY rates.
       3. aave_scraper.py returns the extracted APY data (e.g., {'USDT': 'X.XX%', 'USDC': 'Y.YY%', 'DAI': 'Z.ZZ%'}).
       4. main.py (or the scheduler) formats the data into a Telegram message.
       5. main.py (or the scheduler) dispatches the message using TelegramClient.
   * Dependencies: requests and BeautifulSoup are already part of the project. If a headless browser is required, selenium or playwright would be added.
