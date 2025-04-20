"""
workflows.py

Purpose: Orchestrates race workflows by coordinating GUI, database, and device communications.

Usage: Instantiate RaceWorkflow, call run() to begin the main loop.
"""

from db_handler import DatabaseHandler
from comms.serial_comm import SerialCommunicator
from comms.socket_comm import SocketCommunicator
from gui import RaceGUI
from config import Config
from logger import logger
from race_manager import RaceManager
import RPi.GPIO as GPIO
import time


class RaceWorkflow:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseHandler()
        self.gui = RaceGUI()
        self.serial = SerialCommunicator(self.config.ARDUINO_PORT, self.config.ARDUINO_BAUD)
        self.socket_comm = None  # TODO: Initialize socket communicators for remote devices
        self.relay_shifter = None  # TODO: Initialize relay shifter if applicable
        self.race_manager = RaceManager(self.db, 0, 1, self.config.TRACK_NUMBER, self.config.RACE_START_MODE)

    def run(self):
        """
        Starts the main workflow loop.
        """
        try:
            logger.info("Starting RaceWorkflow...")
            self.initialize_program()
            self.gui.start()  # Start the GUI main loop
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        finally:
            self.shutdown()

    def initialize_program(self):
        """
        Initializes the program by setting up configuration, database connection, and devices.
        """
        logger.info("Initializing program...")
        self.setup_gpio_and_relays()
        self.gui.show_message("Program Initialized")

    def setup_gpio_and_relays(self):
        """
        Configures GPIO pins and relay hardware.
        """
        logger.info("Setting up GPIO pins and relays...")
        # TODO: Add GPIO and relay setup logic.

    def increment_race_counter(self):
        """
        Increments the race counter.
        """
        self.race_manager.increment_race_counter()
        logger.info(f"Race counter incremented to {self.race_manager.get_current_race_counter()}")

    def close_starting_gates(self):
        """
        Displays the close starting gates modal and waits for gates to close.
        """
        logger.info("Displaying close starting gates modal...")
        self.gui.show_message("Close Starting Gates")
        while not self.gates_closed():
            time.sleep(0.1)
        logger.info("Starting gates closed.")

    def gates_closed(self):
        """
        Checks if the starting gates are closed.
        """
        # TODO: Implement logic to check if gates are closed.
        return True

    def using_loading_modal(self):
        """
        Determines if the loading modal should be used based on the race mode.
        """
        return self.config.RACE_START_MODE.lower() not in ["free"]

    def load_racers(self):
        """
        Loads racers into lanes using the loading modal.
        """
        logger.info("Loading racers...")
        for lane in range(1, self.config.NUMBER_LANES + 1):
            while True:
                rfid = self.read_rfid_card()
                racer_info = self.lookup_racer_info(rfid)
                if racer_info:
                    self.race_manager.initialize_race_entry(
                        self.race_manager.get_current_race_counter(),
                        lane,
                        rfid,
                        racer_info
                    )
                    self.gui.show_message(f"Lane {lane}: {racer_info['RacerFirstName']} {racer_info['RacerLastName']}")
                    self.wait_for_rfid_button_press()
                    break
                else:
                    self.gui.show_message("Racer not found. Try again.")

    def read_rfid_card(self):
        """
        Reads RFID card data for racer identification.
        """
        logger.info("Reading RFID card...")
        # TODO: Add RFID card reading logic.
        return "sample_rfid"

    def lookup_racer_info(self, rfid):
        """
        Looks up racer information in the database.
        """
        logger.info(f"Looking up racer info for RFID: {rfid}")
        # TODO: Add logic to query racer information from the database.
        return {"RacerFirstName": "John", "RacerLastName": "Doe", "RacerCarName": "Speedster"}

    def wait_for_rfid_button_press(self):
        """
        Waits for the RFID pad button to be pressed and released.
        """
        logger.info("Waiting for RFID button press...")
        # TODO: Implement logic to wait for button press.

    def using_timer_modal(self):
        """
        Determines if the timer modal should be used based on the race mode.
        """
        return self.config.RACE_START_MODE.lower() in ["drag", "collaborate"]

    def start_race_with_timer(self):
        """
        Starts the race using the timer modal.
        """
        logger.info("Starting race with timer modal...")
        self.gui.show_message("Starting Countdown Timer")
        self.wait_for_rfid_button_press()
        self.activate_countdown_timer()
        self.monitor_lane_buttons()

    def activate_countdown_timer(self):
        """
        Activates the countdown timer.
        """
        logger.info("Activating countdown timer...")
        # TODO: Add logic to activate countdown timer.

    def start_race_without_timer(self):
        """
        Starts the race without using the timer modal.
        """
        logger.info("Starting race without timer modal...")
        if self.config.RACE_START_MODE.lower() == "starter":
            self.wait_for_rfid_button_press()
            self.trigger_all_relays()
        elif self.config.RACE_START_MODE.lower() == "free":
            logger.info("Free mode: No relays involved, simple start switch used.")

    def trigger_all_relays(self):
        """
        Triggers all relays for the race start.
        """
        logger.info("Triggering all relays...")
        # TODO: Add logic to trigger all relays.

    def monitor_race(self):
        """
        Monitors the race, capturing completion times and updating the GUI.
        """
        logger.info("Monitoring race...")
        for lane in range(1, self.config.NUMBER_LANES + 1):
            if self.ir_sensor_triggered(lane):
                self.record_finish(lane)

    def ir_sensor_triggered(self, lane):
        """
        Checks if the IR sensor for a specific lane has been triggered.
        """
        # TODO: Implement logic to check IR sensor.
        return False

    def record_finish(self, lane):
        """
        Records the finish time for a specific lane.
        """
        logger.info(f"Recording finish for lane {lane}...")
        # TODO: Capture race completion time and update race manager.

    def handle_race_completion(self):
        """
        Handles race completion logic, including database writes and resets.
        """
        logger.info("Handling race completion...")
        for lane in range(1, self.config.NUMBER_LANES + 1):
            if not self.ir_sensor_triggered(lane):
                self.record_timeout(lane)
        self.update_database_with_results()
        self.gui.show_message("Race Complete")

    def record_timeout(self, lane):
        """
        Records a timeout for a specific lane.
        """
        logger.info(f"Recording timeout for lane {lane}...")
        # TODO: Set race time, reaction time, and placing to zero for the lane.

    def update_database_with_results(self):
        """
        Updates the database with race results.
        """
        logger.info("Updating database with race results...")
        # TODO: Write race results to the database.

    def shutdown(self):
        """
        Shuts down the workflow and cleans up resources.
        """
        logger.info("Shutting down workflow...")
        try:
            GPIO.cleanup()
            self.db.close()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
