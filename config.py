"""
config.py

Purpose: Central configuration for CubCar application. Defines constants and loads environment variables for database, communication, GUI, and logging settings.

Usage: Import Config class to access application settings across modules.
"""
import os
class Config:
    # Database settings
    DB_HOST = os.getenv('DB_HOST', '192.168.0.18')
    DB_USER = os.getenv('DB_USER', 'cubcaradmin')
    DB_PASS = os.getenv('DB_PASS', 'cubsrock')
    DB_NAME = os.getenv('DB_NAME', 'cubcar')

    # Serial port for Arduino Nano
    ARDUINO_PORT = os.getenv('ARDUINO_PORT', '/dev/ttyS0')
    ARDUINO_BAUD = 57600

    # Socket settings
    SOCKET_PORT = 12345
    SOCKET_TIMEOUT = 5  # seconds

    # GUI settings
    WINDOW_TITLE = "CubCar Race Tracker"
    WINDOW_SIZE = "800x480"

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
