"""
socket_comm.py

Purpose: Provides a generic socket communication interface for handling multiple devices.
"""

import socket
import threading
from logger import logger
from config import Config  # Import Config for IP and port configuration


class SocketCommunicator:
    def __init__(self):
        """
        Initializes the SocketCommunicator with host and port from Config.
        """
        self.host = Config.SOCKET_HOST if hasattr(Config, 'SOCKET_HOST') else "0.0.0.0"
        self.port = Config.SOCKET_PORT
        self.server_socket = None
        self.running = False
        self.device_handlers = {}  # Dictionary to store handlers for specific devices

    def register_device_handler(self, device_name, handler_function):
        """
        Registers a handler function for a specific device.

        Args:
            device_name (str): The name of the device (e.g., "PICO").
            handler_function (function): The function to handle communication with the device.
        """
        self.device_handlers[device_name] = handler_function
        logger.info(f"Registered handler for device: {device_name}")

    def start_server(self):
        """
        Starts the socket server to listen for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        logger.info(f"Socket server started on {self.host}:{self.port}")

        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"New connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            logger.error(f"Error in server loop: {e}")
        finally:
            self.shutdown()

    def handle_client(self, client_socket):
        """
        Handles communication with a connected client.
        """
        try:
            while True:
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break

                logger.info(f"Received data: {data}")
                # Parse the device name from the incoming data
                if "|" in data:
                    device_name, command = data.split("|", 1)
                    if device_name in self.device_handlers:
                        # Call the registered handler for the device
                        response = self.device_handlers[device_name](command)
                        client_socket.send(response.encode())
                    else:
                        logger.warning(f"No handler registered for device: {device_name}")
                        client_socket.send(b"Unknown device\n")
                else:
                    logger.warning(f"Invalid data format: {data}")
                    client_socket.send(b"Invalid data format\n")

        except (ConnectionResetError, socket.error) as e:
            logger.warning(f"Connection error: {e}")
        finally:
            client_socket.close()
            logger.info("Client connection closed")

    def shutdown(self):
        """
        Shuts down the socket server and releases resources.
        """
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            logger.info("Socket server shut down")
