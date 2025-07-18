import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.keyword_analyzer import KeywordAnalyzer

class TestKeywordAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = KeywordAnalyzer()

    def test_analyze_filing_crypto_detected(self):
        """
        Test that analyze_filing correctly identifies crypto content and returns a summary.
        """
        sample_text = "This document discusses our new blockchain initiative and digital assets."
        result = self.analyzer.analyze_filing(sample_text)

        self.assertTrue(result['crypto_detected'])
        self.assertIn("blockchain", result['summary'])
        self.assertIn("digital assets", result['summary'])

    def test_analyze_filing_no_crypto(self):
        """
        Test that analyze_filing correctly handles text with no crypto content.
        """
        sample_text = "This document discusses our financial performance."
        result = self.analyzer.analyze_filing(sample_text)

        self.assertFalse(result['crypto_detected'])
        self.assertIsNone(result['summary'])

    def test_analyze_filing_case_insensitivity(self):
        """
        Test that keyword detection is case-insensitive.
        """
        sample_text = "This document mentions BITCOIN and Ethereum."
        result = self.analyzer.analyze_filing(sample_text)

        self.assertTrue(result['crypto_detected'])
        self.assertIn("Bitcoin", result['summary'])
        self.assertIn("Ethereum", result['summary'])

    def test_analyze_filing_multiple_keywords_same_line(self):
        """
        Test that multiple keywords in the same line are detected and included.
        """
        sample_text = "We are investing in blockchain and NFTs."
        result = self.analyzer.analyze_filing(sample_text)

        self.assertTrue(result['crypto_detected'])
        self.assertIn("blockchain", result['summary'])
        self.assertIn("NFT", result['summary'])

    def test_analyze_filing_partial_word_no_match(self):
        """
        Test that partial word matches are not detected.
        """
        sample_text = "The soldier walked through the consolation fields."
        result = self.analyzer.analyze_filing(sample_text)

        self.assertFalse(result['crypto_detected'])
        self.assertIsNone(result['summary'])

    def test_analyze_filing_removes_html_tags(self):
        """
        Test that all HTML tags are removed from the snippet.
        """
        sample_text = "<p>This is a <b>blockchain</b> related sentence with <i>multiple</i> tags.</p>"
        result = self.analyzer.analyze_filing(sample_text)

        self.assertTrue(result['crypto_detected'])
        self.assertNotIn("<p>", result['summary'])
        self.assertNotIn("<b>", result['summary'])
        self.assertNotIn("<i>", result['summary'])
        self.assertIn("This is a blockchain related sentence with multiple tags.", result['summary'])

if __name__ == '__main__':
    unittest.main()