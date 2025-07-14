import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """
        Set up an in-memory SQLite database for testing.
        """
        self.db = Database(db_path=":memory:")

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        self.db.close()

    def test_add_and_check_filing(self):
        """
        Test that a filing can be added and checked for existence.
        """
        self.assertFalse(self.db.filing_exists("test_id_1"))
        self.db.add_filing("test_id_1")
        self.assertTrue(self.db.filing_exists("test_id_1"))

    def test_add_duplicate_filing(self):
        """
        Test that adding a duplicate filing does not raise an error.
        """
        self.db.add_filing("test_id_2")
        self.db.add_filing("test_id_2")
        self.assertTrue(self.db.filing_exists("test_id_2"))


if __name__ == "__main__":
    unittest.main()
