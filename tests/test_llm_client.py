import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm_client import LlmClient


class TestLlmClient(unittest.TestCase):

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("google.generativeai.GenerativeModel")
    def test_analyze_filing_crypto_detected(self, mock_model):
        """
        Test that analyze_filing correctly identifies crypto content and returns a summary.
        """
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.text = "This is a summary of the crypto content."
        mock_model.return_value.generate_content.return_value = mock_response

        client = LlmClient()
        result = client.analyze_filing(
            "This filing discusses our new blockchain initiative."
        )

        self.assertTrue(result["crypto_detected"])
        self.assertEqual(result["summary"], "This is a summary of the crypto content.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("google.generativeai.GenerativeModel")
    def test_analyze_filing_no_crypto(self, mock_model):
        """
        Test that analyze_filing correctly handles the 'NO_CRYPTO' response.
        """
        mock_response = MagicMock()
        mock_response.text = "NO_CRYPTO"
        mock_model.return_value.generate_content.return_value = mock_response

        client = LlmClient()
        result = client.analyze_filing("This filing is about something else.")

        self.assertFalse(result["crypto_detected"])
        self.assertIsNone(result["summary"])

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("google.generativeai.GenerativeModel")
    def test_analyze_filing_llm_error(self, mock_model):
        """
        Test that analyze_filing handles an exception from the LLM API.
        """
        mock_model.return_value.generate_content.side_effect = Exception(
            "Test LLM error"
        )

        client = LlmClient()
        result = client.analyze_filing("This will cause an error.")

        self.assertFalse(result["crypto_detected"])
        self.assertIsNone(result["summary"])


if __name__ == "__main__":
    unittest.main()
