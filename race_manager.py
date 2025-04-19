"""
race_manager.py

Purpose: Manages race operations, including racer information, race results, and database interactions.
"""

from db_handler import DatabaseHandler

class RaceManager:
    def __init__(self, db_handler, race_counter, heat, track_number, race_start_mode):
        print("Progress: Initializing RaceManager...")
        self.db_handler = db_handler  # Use DatabaseHandler instance
        self.race_counter = race_counter
        self.heat = heat
        self.races = []  # Local storage for race data
        self.recorded_lanes = set()  # Tracks lanes with recorded reaction times
        self.track_number = track_number
        self.race_start_mode = race_start_mode.lower()  # Normalize mode
        self.racing_start_times = {}  # Store individual start times per lane
        print("Progress: RaceManager initialized.")

    def initialize_race_entry(self, race_id, lane, rfid, racer_info):
        if any(race["Lane"] == lane for race in self.races):
            return
        self.races.append({
            "RacerID": racer_info["RacerID"],
            "RaceCounter": race_id,
            "RaceCarNumber": racer_info["RacerCarNumber"],
            "TrackID": self.track_number,
            "Heat": self.heat,
            "Lane": lane,
            "RacerCarName": racer_info["RacerCarName"],
            "RacerPack": racer_info["RacerPack"],
            "RaceTime": "00.000000",
            "ReactionTime": "00.000000",
            "Placing": 0,
            "RacerRFID": rfid,
            "RacerFirstName": racer_info["RacerFirstName"],
            "RacerLastName": racer_info["RacerLastName"],
            "RaceMode": self.race_start_mode
        })

    def assign_racer_info(self, lane, racer_info):
        for race in self.races:
            if race["Lane"] == lane:
                race.update(racer_info)
                return 

    def record_reaction_time(self, lane, reaction_time):
        for race in self.races:
            if race["Lane"] == lane and race["ReactionTime"] == "00.000000":
                race["ReactionTime"] = reaction_time
                print(f"Progress: Recorded reaction time for lane {lane}: {reaction_time}")
                return

    def record_race_finish(self, lane, race_time, place):
        for race in self.races:
            if race["Lane"] == lane:
                race["RaceTime"] = race_time
                race["Placing"] = place
                print(f"Progress: Recorded finish for lane {lane}: RaceTime = {race_time}, Placing = {place}")
                return

    def get_racer_info(self, rfid):
        print(f"Progress: Querying racer info for RFID {rfid}...")
        query = """
        SELECT 
            RI.RacerID,
            RI.RacerFirstName, 
            RI.RacerLastName, 
            RI.RacerPack,
            PN.PackName, 
            RI.RacerRFID, 
            RI.RacerCarName, 
            RI.RacerCarNumber, 
            RI.RacerInclude, 
            RI.RacerCarChecked, 
            RI.RacerCarWeight, 
            RI.RacerPhoto
        FROM racerinfo RI LEFT OUTER JOIN packnames PN ON RI.RacerPack = PN.ID
        WHERE RacerRFID = %s
        """
        try:
            racer_info = self.db_handler.query(query, (rfid,), fetch_one=True)
            print("Progress: Racer info retrieved." if racer_info else "Progress: Racer info not found.")
            return racer_info
        except Exception as e:
            print(f"Unexpected error in get_racer_info: {e}")
            return None

    def write_races_to_db(self):
        if self.race_start_mode == "free":
            print("Progress: Free mode active. Skipping database writes.")
            return
        print("Progress: Writing race results to the database...")
        query = """
        INSERT INTO raceresults (RacerID, RaceCounter, RaceCarNumber, TrackID, Heat, Lane, CarName, Pack, RaceTime, ReactionTime, Placing, RacerRFID, RacerFirstName, RacerLastName, RaceMode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            for race in self.races:
                self.db_handler.execute(query, (
                    race["RacerID"],
                    race["RaceCounter"],
                    race["RaceCarNumber"],
                    race["TrackID"],
                    race["Heat"],
                    race["Lane"],
                    race["RacerCarName"],
                    race["RacerPack"],
                    race["RaceTime"],
                    race["ReactionTime"],
                    race["Placing"],
                    race["RacerRFID"],
                    race["RacerFirstName"],
                    race["RacerLastName"],
                    race["RaceMode"]
                ))
            print("Progress: Race results successfully written to the database.")
            self.races.clear()
        except Exception as e:
            print("Database Error during write:", e)

    def get_reaction_time(self, lane_index):
        for race in self.races:
            if race["Lane"] == lane_index:
                return race["ReactionTime"]
        return 0.0

    def get_current_race_counter(self):
        return self.race_counter

    def increment_race_counter(self):
        self.race_counter += 1
        print(f"Progress: Race counter incremented to {self.race_counter}.")

    def is_duplicate_rfid(self, rfid):
        for race in self.races:
            if race["RacerRFID"] == rfid:
                return True
        return False