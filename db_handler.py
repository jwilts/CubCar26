"""
db_handler.py

Purpose: Provides DatabaseHandler class for managing MySQL connections, queries, transactions, and error handling.

Usage: Instantiate DatabaseHandler in workflows to perform safe queries and execute commands.
"""

import mysql.connector
from mysql.connector import Error
from logger import logger
from config import Config
import time

class DatabaseHandler:
    def __init__(self, max_retries=3, retry_delay=2):
        """
        Initializes the DatabaseHandler with a connection to the database.

        Args:
            max_retries (int): Maximum number of retries for transient errors.
            retry_delay (int): Delay in seconds between retries.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
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
        Executes a SELECT query and fetches results with retry logic.

        Args:
            sql (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.
            fetch_one (bool): If True, fetch only the first result. Otherwise, fetch all results.

        Returns:
            list[dict] or dict: A list of rows as dictionaries if fetch_one is False,
                                or a single row as a dictionary if fetch_one is True.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                self.cursor.execute(sql, params or ())
                if fetch_one:
                    result = self.cursor.fetchone()
                else:
                    result = self.cursor.fetchall()
                logger.debug(f"DB query executed successfully: {sql}")
                return result
            except mysql.connector.Error as err:
                logger.error(f"DB query error: {err}")
                retries += 1
                if retries < self.max_retries:
                    logger.warning(f"Retrying query... Attempt {retries}/{self.max_retries}")
                    time.sleep(self.retry_delay)
                else:
                    logger.critical(f"Query failed after {self.max_retries} attempts: {sql}")
                    raise

    def execute(self, sql, params=None):
        """
        Executes a non-SELECT query (e.g., INSERT, UPDATE, DELETE) with retry logic.

        Args:
            sql (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.

        Returns:
            None
        """
        retries = 0
        while retries < self.max_retries:
            try:
                self.cursor.execute(sql, params or ())
                self.conn.commit()
                logger.debug(f"DB execute committed successfully: {sql}")
                return
            except mysql.connector.Error as err:
                logger.error(f"DB execute error: {err}")
                self.conn.rollback()
                retries += 1
                if retries < self.max_retries:
                    logger.warning(f"Retrying execute... Attempt {retries}/{self.max_retries}")
                    time.sleep(self.retry_delay)
                else:
                    logger.critical(f"Execute failed after {self.max_retries} attempts: {sql}")
                    raise

    def close(self):
        """
        Closes the database connection and cursor.
        """
        try:
            self.cursor.close()
            self.conn.close()
            logger.info("Database connection closed")
        except Error as err:
            logger.error(f"Error closing database connection: {err}")