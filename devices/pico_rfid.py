"""
pico_rfid.py

Purpose: Handles specific communication logic for the Pico RFID device.
"""

from logger import logger
from threading import Lock

# Thread-safe global variables
lock = Lock()
latest_rfid = None

def handle_pico_command(command):
    """
    Handles commands sent from the Pico RFID device.

    Args:
        command (str): The command received from the Pico device.

    Returns:
        str: The response to send back to the Pico device.
    """
    global latest_rfid

    try:
        if command == "RESET_LEDS":
            reset_leds()
            return "LEDs reset"
        elif command.startswith("RFID"):
            _, rfid = command.split(":")
            update_latest_rfid(rfid)
            lane = get_current_lane()
            increment_current_lane()
            return f"Lane {lane} assigned to RFID {rfid}"
        else:
            logger.warning(f"Unknown command from Pico: {command}")
            return "Unknown command"
    except Exception as e:
        logger.error(f"Error handling Pico command: {e}")
        return "Error"


def reset_leds():
    """
    Resets LEDs (placeholder for actual LED reset logic).
    """
    logger.info("Resetting LEDs...")
    # TODO: Implement LED reset logic


def update_latest_rfid(rfid):
    """
    Updates the latest RFID value in a thread-safe manner.
    """
    global latest_rfid
    with lock:
        latest_rfid = rfid
        logger.info(f"Updated latest RFID: {rfid}")


def get_latest_rfid():
    """
    Retrieves the latest RFID value in a thread-safe manner.
    """
    global latest_rfid
    with lock:
        return latest_rfid


