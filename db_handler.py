"""
db_handler.py

Purpose: Provides DatabaseHandler class for managing MySQL connections, queries, transactions, and error handling.

Usage: Instantiate DatabaseHandler in workflows to perform safe queries and execute commands.
"""

import mysql.connector
from logger import logger
from config import Config

class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASS,
                database=Config.DB_NAME
            )
            self.cursor = self.conn.cursor(dictionary=True)
            logger.info("Database connection established")
        except mysql.connector.Error as err:
            logger.error(f"DB connection error: {err}")
            raise

    def query(self, sql, params=None, fetch_one=False):
        """
        Executes a SELECT query and fetches results.

        Args:
            sql (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.
            fetch_one (bool): If True, fetch only the first result. Otherwise, fetch all results.

        Returns:
            list[dict] or dict: A list of rows as dictionaries if fetch_one is False,
                                or a single row as a dictionary if fetch_one is True.
        """
        try:
            self.cursor.execute(sql, params or ())
            if fetch_one:
                return self.cursor.fetchone()
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"DB query error: {err}")
            raise

    def execute(self, sql, params=None):
        """
        Executes a non-SELECT query (e.g., INSERT, UPDATE, DELETE).

        Args:
            sql (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.

        Returns:
            None
        """
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            logger.debug("DB execute committed")
        except mysql.connector.Error as err:
            self.conn.rollback()
            logger.error(f"DB execute error: {err}")
            raise

    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.conn.close()
        logger.info("Database connection closed")