"""
gui.py

Purpose: Defines the Tkinter-based GUI for race management, including lane status, countdown, and messages.

Usage: Instantiate RaceGUI, call update_lane_status() and show_message(), then start().
"""
import tkinter as tk
from config import Config
from logger import logger
class RaceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self._setup_widgets()

    def _setup_widgets(self):
        pass  # TODO: Define frames, buttons, labels, layout

    def update_lane_status(self, lane, status):
        pass  # TODO: Update GUI element

    def show_message(self, msg):
        logger.info(f"GUI message: {msg}")
        pass  # TODO: Display message in GUI

    def start(self):
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            raise
