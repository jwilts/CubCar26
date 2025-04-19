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

    # Track settings
    TRACK_NUMBER = 1  # What is this track's number? MUST BE UNIQUE
    NUMBER_LANES = 3  # How many lanes is the track (2, 3, 4)

    # Race Start Mode
    RACE_START_MODE = "drag"  # Mode to use for starting races
    # "drag" (default) -- All lanes are started independently by drag race tree and servos on each lane. 
    # Both racer response time and car race time are captured in the database.
    # "collaborate" -- All lanes are counted down by drag race tree, but after all buttons are pushed, then all lanes
    # are triggered simultaneously. Both racer response time and car race time are captured in the database.
    # "starter" -- Button on the remote RFID pad is used as a trigger to start the race.
    # Drag race tree gives visual countdown to the race starting.
    # "fast" -- Button on the remote RFID pad is used as the trigger to start the race. No drag race tree is used.
    # "simple" -- No countdown timer, no relays used. A single switch at the top of the track triggers the start.
    # "free" -- Simple start + no RFID + no database.

    RACE_MAX_RACE_TIME = 20  # How long in seconds should a race be before timing out (default 12 seconds)
    RACE_MIN_RACE_TIME = 1  # Default minimum race time (ignore LDR trips before this time)
    RACE_SLOW_BEAVER_TIME = 5  # Time for slow start in "drag" or "collaborate" modes (default 3 seconds)

    # LED settings
    LED_WINNERLIGHTS_RGB = "RGB"  # Color order for winner lights (RGB, RBG, GRB, etc.)
    LED_WINNERLIGHTS_DEF = ["RED", "GREEN", "BLUE", "YELLOW"]  # Default colors for each lane's winner light
    # Colors: BLACK = (0, 0, 0), RED = (255, 0, 0), YELLOW = (255, 150, 0), GREEN = (0, 255, 0), 
    # CYAN = (0, 255, 255), BLUE = (0, 0, 255), PURPLE = (180, 0, 255), WHITE = (255, 255, 255)

    LED_WINNERLIGHTS_BRIGHTNESS = 100  # Brightness value (0-255) for winner lights

    @staticmethod
    def show_config():
        """Prints all config settings for debugging."""
        for key, value in Config.__dict__.items():
            if not key.startswith("__"):
                print(f"{key}: {value}")


