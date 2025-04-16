"""
main.py

Purpose: Entry point for CubCar application. Initializes and starts the RaceWorkflow.

Usage: Run `python main.py` to launch the tracker GUI and workflow.
"""
from workflows import RaceWorkflow
if __name__ == '__main__':
    wf = RaceWorkflow()
    wf.run()
