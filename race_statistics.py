"""
race_statistics.py

Purpose: Defines the RaceStatistics data class to store race-related statistics.
"""

from dataclasses import dataclass
from db_handler import execute_query  # Import the database handler

@dataclass
class RaceStatistics:
    RaceCounter: int
    RaceTime: str
    CurrentHeat: int

    @staticmethod
    def from_sql_result(sql_result):
        """
        Factory method to create a RaceStatistics instance from an SQL query result.

        Args:
            sql_result (tuple): A tuple containing the result of the SQL query
                                (RaceCounter, RaceTime, CurrentHeat).

        Returns:
            RaceStatistics: An instance of RaceStatistics populated with the query result.
        """
        return RaceStatistics(
            RaceCounter=sql_result[0],
            RaceTime=sql_result[1],
            CurrentHeat=sql_result[2]
        )

# Function to fetch race statistics
def fetch_race_statistics(track_id):
    """
    Fetches race statistics for a given track ID from the database.

    Args:
        track_id (int): The ID of the track to fetch statistics for.

    Returns:
        RaceStatistics: An instance of RaceStatistics populated with the query result.
    """
    # SQL query
    query = """
        SELECT MAX(A.RaceCounter) AS RaceCounter, 
               RIGHT(MIN(A.RaceTime), 9) AS RaceTime, 
               B.Heat 
        FROM raceresults A 
        INNER JOIN trackinformation B ON A.TrackID = B.TrackID 
        WHERE A.TrackID = %s AND A.RaceTime > 0;
    """

    # Execute the query using the database handler
    result = execute_query(query, (track_id,))

    # Check if a result was returned
    if result:
        return RaceStatistics.from_sql_result(result)
    else:
        print("No data found for the given TrackID.")
        return None

# Example usage
if __name__ == "__main__":
    track_id = 1  # Replace with the desired TrackID
    race_stats = fetch_race_statistics(track_id)

    if race_stats:
        print(race_stats)