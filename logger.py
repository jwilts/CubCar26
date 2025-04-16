"""
logger.py

Purpose: Sets up application-wide logging with console and rotating-file handlers.

Usage: Import `logger` to log messages from any module.
"""
import logging
from logging.handlers import RotatingFileHandler
from config import Config
logger = logging.getLogger('cubcar')
logger.setLevel(Config.LOG_LEVEL)
console = logging.StreamHandler()
console.setLevel(Config.LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
file_handler = RotatingFileHandler('cubcar.log', maxBytes=1e6, backupCount=3)
file_handler.setLevel(Config.LOG_LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)