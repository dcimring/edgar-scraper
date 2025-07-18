import logging
import re
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KeywordAnalyzer:
    """
    A client for analyzing text content for crypto-related keywords.
    """

    CRYPTO_KEYWORDS = [
        'crypto', 'cryptocurrency', 'stablecoin', 'blockchain', 'digital assets',
        'tokens', 'NFT', 'Web3', 'DLT', 'cryptographic', 'mining', 'DeFi', 'DAO',
        'Bitcoin', 'BTC', 'Ethereum', 'ETH', 'Tether', 'USDT', 'XRP', 'BNB',
        'Solana', 'SOL', 'USD Coin', 'USDC', 'Dogecoin', 'DOGE', 'TRON', 'TRX',
        'Cardano', 'ADA'
    ]

    def analyze_filing(self, filing_text: str) -> Dict[str, Optional[str]]:
        """
        Analyzes the filing text for crypto-related keywords and generates a snippet.

        Args:
            filing_text: The full text of the SEC filing.

        Returns:
            A dictionary containing the analysis result.
            If crypto content is found, it returns {'crypto_detected': True, 'summary': '...'}.
            If not, it returns {'crypto_detected': False, 'summary': None}.
        """
        detected_keywords = []
        snippet = []
        lines = filing_text.splitlines()

        for line in lines:
            for keyword in self.CRYPTO_KEYWORDS:
                if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                    detected_keywords.append(keyword)
                    cleaned_line = re.sub(r'<[^>]*>', '', line.strip())
                    snippet.append(cleaned_line)
                    break  # Move to the next line once a keyword is found in the current line

        if detected_keywords:
            # Create a unique list of detected keywords
            unique_keywords = list(set(detected_keywords))
            summary_text = f"Crypto keywords detected: {', '.join(unique_keywords)}. " \
                           f"Snippet: {' '.join(snippet[:3])}..."
            return {'crypto_detected': True, 'summary': summary_text}
        else:
            return {'crypto_detected': False, 'summary': None}

if __name__ == '__main__':
    analyzer = KeywordAnalyzer()
    sample_text_crypto = "This document discusses our investment in blockchain technology and digital assets."
    analysis_crypto = analyzer.analyze_filing(sample_text_crypto)
    print(f"Crypto Analysis: {analysis_crypto}")

    sample_text_no_crypto = "This document discusses our financial performance."
    analysis_no_crypto = analyzer.analyze_filing(sample_text_no_crypto)
    print(f"No Crypto Analysis: {analysis_no_crypto}")