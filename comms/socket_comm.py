"""
socket_comm.py

Purpose: Manages TCP/IP socket communication with remote ESP32 and Pico devices.
Handles connection, send, receive, and cleanup with timeouts and logging.

Usage: Instantiate with target host, call connect(), then send() / receive(), and close().
"""
import socket
from logger import logger
from config import Config
class SocketCommunicator:
    def __init__(self, host, port=Config.SOCKET_PORT):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Config.SOCKET_TIMEOUT)

    def connect(self):
        try:
            self.sock.connect(self.addr)
            logger.info(f"Socket connected to {self.addr}")
        except socket.error as e:
            logger.error(f"Socket connect error: {e}")
            raise

    def send(self, data: bytes):
        try:
            self.sock.sendall(data)
            logger.debug(f"Sent over socket: {data}")
        except socket.error as e:
            logger.error(f"Socket send error: {e}")
            raise

    def receive(self, bufsize=1024) -> bytes:
        try:
            data = self.sock.recv(bufsize)
            logger.debug(f"Received from socket: {data}")
            return data
        except socket.error as e:
            logger.error(f"Socket receive error: {e}")
            raise

    def close(self):
        self.sock.close()
        logger.info("Socket closed")
