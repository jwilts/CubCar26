"""
cubcar26/__init__.py

Package initializer for the cubcar26 application. Defines package metadata, version, and imports key modules.

Usage: Implicitly executed on import to set up package-level variables.
"""

__version__ = "1.0.0"
__author__ = "Jeff Wilts"
__email__ = "pjwilts4@gmail.com"

# Import key modules for package-level access
from .config import Config
from .db_handler import DatabaseHandler
from .race_manager import RaceManager

# Package-level variables
config = Config()
db_handler = DatabaseHandler()