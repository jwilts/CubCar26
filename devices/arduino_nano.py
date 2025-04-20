"""
arduino_nano.py

Purpose: Wraps SerialCommunicator to provide specific commands and parsing for Arduino Nano track sensors.

Usage: Instantiate ArduinoNanoInterface, call send_effect_command() and send_lcd_command().

Supported Commands:
1. LED Control:
   Command Format: "LED|<led_number>|<bank>|<place>|<effect>|<brightness>|<color>\n"
   - led_number: The LED strip to control (1, 2, or 3).
   - bank: The bank of LEDs to control (e.g., for grouped LEDs).
   - place: The number of LEDs to light up in the bank.
   - effect: The effect to apply (e.g., "OFF", "BREATHING", "CHASER", "RAINBOW", "BLINK", "CONFETTI", "SINELON", "BPM", "JUGGLE", "LIGHT_UP_BANK", "LIGHT_PLACE", "FULL", "FLASH").
   - brightness: The brightness level (0-255).
   - color: The base color for the effect (e.g., "RED", "GREEN", "BLUE", "WHITE").

2. LCD Control:
   Command Format: 
   - "CLEAR_LCD\n": Clears the LCD display.
   - "DISPLAY_LCD|<row>|<message>\n": Displays a message on the specified row of the LCD.

After processing a command, the Arduino sends back an "<ACK>" to confirm reception and processing.
"""

from comms.serial_comm import SerialCommunicator
from logger import logger


class ArduinoNanoInterface:
    def __init__(self, port, baudrate=9600, timeout=1):
        """
        Initializes the ArduinoNanoInterface with a SerialCommunicator instance.

        Args:
            port (str): The serial port to connect to (e.g., "/dev/ttyUSB0").
            baudrate (int): The baud rate for the serial connection.
            timeout (int): Timeout for the serial connection in seconds.
        """
        try:
            self.serial_comm = SerialCommunicator(port, baudrate, timeout)
            logger.info(f"ArduinoNanoInterface initialized on port {port} at {baudrate}bps.")
        except Exception as e:
            logger.error(f"Failed to initialize ArduinoNanoInterface: {e}")
            self.serial_comm = None

    def send_effect_command(self, led_number, effect, bank, place, brightness, color, debug=False):
        """
        Sends an LED effect command to the Arduino Nano.

        Args:
            led_number (int): The LED strip to control (1, 2, or 3).
            effect (str): The effect to apply (e.g., "OFF", "BREATHING", "CHASER", "RAINBOW").
            bank (int): The bank of LEDs to control.
            place (int): The number of LEDs to light up in the bank.
            brightness (int): The brightness level (0-255).
            color (str): The base color for the effect (e.g., "RED", "GREEN", "BLUE").
            debug (bool): If True, logs the command being sent.
        """
        if not self.serial_comm:
            logger.error("Serial connection not initialized. Cannot send LED command.")
            return

        command = f"LED|{led_number}|{bank}|{place}|{effect}|{brightness}|{color}\n"
        if debug:
            logger.debug(f"Sending LED command: {command.strip()}")
        try:
            self.serial_comm.send(command)
        except Exception as e:
            logger.error(f"Error sending LED command: {e}")

    def send_lcd_command(self, action, row=None, message=None):
        """
        Sends an LCD command to the Arduino Nano.

        Args:
            action (str): The action to perform (e.g., "CLEAR", "DISPLAY").
            row (int, optional): The row number for the display (required for "DISPLAY").
            message (str, optional): The message to display (required for "DISPLAY").
        """
        if not self.serial_comm:
            logger.error("Serial connection not initialized. Cannot send LCD command.")
            return

        try:
            if action == "CLEAR":
                self.serial_comm.send("CLEAR_LCD\n")
            elif action == "DISPLAY" and row is not None and message is not None:
                command = f"DISPLAY_LCD|{row}|{message}\n"
                self.serial_comm.send(command)
            else:
                logger.warning(f"Invalid LCD command: action={action}, row={row}, message={message}")
        except Exception as e:
            logger.error(f"Error sending LCD command: {e}")

    def close(self):
        """
        Closes the serial connection to the Arduino Nano.
        """
        if self.serial_comm:
            self.serial_comm.close()
            logger.info("ArduinoNanoInterface connection closed.")