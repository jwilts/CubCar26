"""
serial_comm.py

Purpose: Manages serial communication with Arduino Nano over a specified port and baud rate.
Includes methods to send and receive framed messages with logging and error handling.

Usage: Instantiate SerialCommunicator, then call send() and read().
"""

import serial
from logger import logger
from config import Config  # Import Config for port and baud rate configuration


class SerialCommunicator:
    def __init__(self, port=None, baud=None, timeout=1):
        """
        Initializes the SerialCommunicator with the specified port and baud rate.

        Args:
            port (str, optional): The serial port to connect to (e.g., "/dev/ttyUSB0").
                                  Defaults to Config.SERIAL_PORT.
            baud (int, optional): The baud rate for the serial connection.
                                  Defaults to Config.SERIAL_BAUD.
            timeout (int): Timeout for the serial connection in seconds.
        """
        self.port = port or Config.SERIAL_PORT
        self.baud = baud or Config.SERIAL_BAUD

        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=timeout)
            logger.info(f"Serial port {self.port} opened at {self.baud}bps")
        except serial.SerialException as e:
            logger.error(f"Serial open error: {e}")
            raise

    def send(self, message: str):
        """
        Sends a message over the serial connection.

        Args:
            message (str): The message to send.
        """
        try:
            self.ser.write(message.encode())
            logger.debug(f"Sent over serial: {message}")
        except Exception as e:
            logger.error(f"Serial send error: {e}")
            raise

    def read(self) -> str:
        """
        Reads a message from the serial connection.

        Returns:
            str: The message received from the serial connection.
        """
        try:
            line = self.ser.readline().decode().strip()
            logger.debug(f"Received from serial: {line}")
            return line
        except Exception as e:
            logger.error(f"Serial read error: {e}")
            raise

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Serial connection closed.")
