"""
gui.py

Purpose: Manages the graphical user interface (GUI) for the CubCar application, including lane status, race mode grid, and menu options.

Usage: Instantiate RaceGUI, call update_lane_status() and show_message(), then start().
"""

import tkinter as tk
from tkinter import ttk, Menu, messagebox
from config import Config
from logger import logger


class RaceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.race_mode_frame = None
        self._setup_menu()
        self._bind_shortcuts()

    def _setup_menu(self):
        """Sets up the menu and keyboard shortcuts."""
        menubar = Menu(self.root)
        self.config_menu = Menu(menubar, tearoff=0)
        self.config_menu.add_command(label="Configuration Screens", command=self._config_screen, accelerator="Ctrl+C")
        self.config_menu.add_command(label="Testing Sensors", command=self._test_sensors, accelerator="Ctrl+T")
        self.config_menu.add_command(label="Reporting", command=self._show_reports, accelerator="Ctrl+R")
        self.config_menu.add_separator()
        self.config_menu.add_command(label="Exit", command=self._exit_program, accelerator="Ctrl+Q")
        menubar.add_cascade(label="Menu", menu=self.config_menu)
        self.root.config(menu=menubar)
        logger.info("Menu setup complete.")

    def _bind_shortcuts(self):
        """Binds global keyboard shortcuts."""
        self.root.bind_all("<Control-c>", lambda event: self._config_screen())
        self.root.bind_all("<Control-t>", lambda event: self._test_sensors())
        self.root.bind_all("<Control-r>", lambda event: self._show_reports())
        self.root.bind_all("<Control-q>", lambda event: self._exit_program())

    def _exit_program(self):
        """Handles program exit."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            logger.info("Exiting program and cleaning up resources...")
            self.root.destroy()

    def _config_screen(self):
        """Placeholder for configuration screens."""
        messagebox.showinfo("Config", "Configuration screens placeholder")

    def _test_sensors(self):
        """Placeholder for testing sensors."""
        messagebox.showinfo("Testing", "Testing sensors placeholder")

    def _show_reports(self):
        """Placeholder for reporting."""
        messagebox.showinfo("Reporting", "Reporting placeholder")

    def update_lane_status(self, lane, status):
        """Updates the status of a specific lane in the GUI."""
        logger.info(f"Updating lane {lane} status to {status}")
        # TODO: Implement lane status update logic

    def show_message(self, msg):
        """Displays a message in the GUI."""
        logger.info(f"GUI message: {msg}")
        messagebox.showinfo("Message", msg)

    def setup_and_populate_race_mode_grid(self, race_manager):
        """Builds and displays the race mode grid."""
        try:
            if self.race_mode_frame is not None:
                logger.info("Destroying previous race mode grid...")
                self.race_mode_frame.destroy()
                self.race_mode_frame = None

            logger.info("Creating new race mode grid...")
            self.race_mode_frame = ttk.Frame(self.root)
            self.race_mode_frame.pack(pady=20, padx=20, fill="both", expand=True)

            headers = ["Lane", "Racer & Car", "Reaction Time", "Place", "Race Time"]
            for col, header in enumerate(headers):
                ttk.Label(self.race_mode_frame, text=header, font=("Helvetica", 20, "bold")).grid(row=0, column=col, padx=5, pady=5)

            row = 1
            for race in race_manager.races:
                lane_number = row
                racer_name = f"{race.get('RacerFirstName', 'Unknown')} {race.get('RacerLastName', '')}"
                car_name = race.get('RacerCarName', 'Unknown')
                reaction_time = "0.0000"
                place = "0"
                race_time = "0.0000"

                ttk.Label(self.race_mode_frame, text=str(lane_number), font=("Helvetica", 20)).grid(row=row, column=0, padx=5, pady=5)
                ttk.Label(self.race_mode_frame, text=f"{racer_name}\n{car_name}", font=("Helvetica", 18), justify="center").grid(row=row, column=1, padx=5, pady=5)
                tk.Label(self.race_mode_frame, text=reaction_time, font=("Helvetica", 20), fg="black").grid(row=row, column=2, padx=5, pady=5)
                tk.Label(self.race_mode_frame, text=place, font=("Helvetica", 20), fg="black").grid(row=row, column=3, padx=5, pady=5)
                tk.Label(self.race_mode_frame, text=race_time, font=("Helvetica", 20), fg="black").grid(row=row, column=4, padx=5, pady=5)
                row += 1

            self.root.update_idletasks()
            self.root.update()
            logger.info("Race mode grid created successfully.")
        except Exception as e:
            logger.error(f"Error creating race grid: {e}")

    def start(self):
        """Starts the GUI main loop."""
        try:
            logger.info("Starting GUI main loop...")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            raise