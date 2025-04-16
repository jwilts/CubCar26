"""
serial_comm.py

Purpose: Manages serial communication with Arduino Nano over a specified port and baud rate.
Includes methods to send and receive framed messages with logging and error handling.

Usage: Instantiate SerialCommunicator with port and baud, then call send() and read().
"""
import serial
from logger import logger
class SerialCommunicator:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            logger.info(f"Serial port {port} opened at {baud}bps")
        except serial.SerialException as e:
            logger.error(f"Serial open error: {e}")
            raise

    def send(self, message: str):
        try:
            self.ser.write(message.encode())
            logger.debug(f"Sent over serial: {message}")
        except Exception as e:
            logger.error(f"Serial send error: {e}")
            raise

    def read(self) -> str:
        try:
            line = self.ser.readline().decode().strip()
            logger.debug(f"Received from serial: {line}")
            return line
        except Exception as e:
            logger.error(f"Serial read error: {e}")
            raise
