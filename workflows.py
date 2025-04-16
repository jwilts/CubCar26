"""
workflows.py

Purpose: Orchestrates race workflows by coordinating GUI, database, and device communications.

Usage: Instantiate RaceWorkflow, call run() to begin the main loop, use start_race() and record_finish() internally.
"""
from db_handler import DatabaseHandler
from comms.serial_comm import SerialCommunicator
from comms.socket_comm import SocketCommunicator
from gui import RaceGUI
from config import Config
from logger import logger

class RaceWorkflow:
    def __init__(self):
        self.db = DatabaseHandler()
        self.gui = RaceGUI()
        self.serial = SerialCommunicator(Config.ARDUINO_PORT, Config.ARDUINO_BAUD)
        # TODO: init socket communicators for remote devices

    def run(self):
        try:
            self.gui.start()
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        finally:
            self.shutdown()

    def start_race(self):
        pass  # TODO: countdown, gate control

    def record_finish(self, lane, time_ms):
        pass  # TODO: write result to DB

    def shutdown(self):
        logger.info("Shutting down workflow")
        self.db.close()
        # TODO: close communications
