import logging
import sqlite3
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Database:
    """
    A class to handle the SQLite database for storing processed filing IDs.
    """

    def __init__(self, db_path: str = "processed_filings.db"):
        """
        Initializes the Database object and creates the database and table if they don't exist.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.connect()
        self.create_table()

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")

    def create_table(self):
        """
        Creates the 'processed_filings' table if it doesn't already exist.
        """
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_filings (
                    id TEXT PRIMARY KEY
                )
            """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def add_filing(self, filing_id: str):
        """
        Adds a filing ID to the processed_filings table.

        Args:
            filing_id: The unique ID of the filing to add.
        """
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO processed_filings (id) VALUES (?)", (filing_id,)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            logging.warning(f"Filing ID {filing_id} already exists in the database.")
        except sqlite3.Error as e:
            logging.error(f"Error adding filing ID {filing_id}: {e}")

    def filing_exists(self, filing_id: str) -> bool:
        """
        Checks if a filing ID already exists in the processed_filings table.

        Args:
            filing_id: The unique ID of the filing to check.

        Returns:
            True if the filing ID exists, False otherwise.
        """
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM processed_filings WHERE id = ?", (filing_id,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Error checking filing ID {filing_id}: {e}")
            return False

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
