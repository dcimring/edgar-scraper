import logging
import os
from typing import Dict, Optional

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class LlmClient:
    """
    A client for interacting with a Large Language Model (LLM) for content analysis.
    """

    def __init__(self):
        """
        Initializes the LlmClient, configuring the generative AI model.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_filing(self, filing_text: str) -> Dict[str, Optional[str]]:
        """
        Analyzes the filing text for crypto-related content and generates a summary.

        Args:
            filing_text: The full text of the SEC filing.

        Returns:
            A dictionary containing the analysis result.
            If crypto content is found, it returns {'crypto_detected': True, 'summary': '...'}.
            If not, it returns {'crypto_detected': False, 'summary': None}.
        """
        prompt = f"""Analyze the following SEC filing text for crypto-related content.
        The keywords to look for are: 'crypto', 'cryptocurrency', 'Bitcoin', 'Ethereum', 'stablecoin', 'blockchain', 'digital assets', 'tokens', 'NFT', 'Web3', 'DLT', 'cryptographic', 'mining', 'DeFi', 'DAO'.

        If found, provide a concise summary (max 100 words) of the relevant sections.
        If no crypto content is found, respond with 'NO_CRYPTO'.

        Filing Text: {filing_text[:20000]}
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            if response_text == "NO_CRYPTO":
                return {"crypto_detected": False, "summary": None}
            else:
                return {"crypto_detected": True, "summary": response_text}

        except Exception as e:
            logging.error(f"Error analyzing filing with LLM: {e}")
            return {"crypto_detected": False, "summary": None}


if __name__ == "__main__":
    # This is an example of how to use the LlmClient.
    # You would need to have a .env file with your GEMINI_API_KEY.
    # client = LlmClient()
    # sample_text = "This filing discusses our new blockchain initiative."
    # analysis = client.analyze_filing(sample_text)
    # print(analysis)
    pass
