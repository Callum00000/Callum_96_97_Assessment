import tkinter as tk
from tkinter import messagebox

# Name of the file that going to beused to store workout data
WORKOUT_FILE = "Workouts.txt"

# This list will hold all the workouts as dictionaries
workouts = []

"""
    This def tries to open the workout file and load data into the list.
    If the file doesn't exist yet, the list will stay empty.
    Each line in the file is stored as: type, date, amount, unit
"""
def load_workouts():
    try:# This will try to open and read the workout file
        file = open(WORKOUT_FILE, "r")
        lines = file.readlines()
        file.close()

 # This will loop through each line and split it into a dictionary
        for line in lines:
            line = line.strip()
            if line != "":
                parts = line.split("|")
                workout = {
                    "type":   parts[0],
                    "date":   parts[1],
                    "amount": parts[2],
                    "unit":   parts[3]
                }
                workouts.append(workout)
    except FileNotFoundError:  # If the file doesn't exist yet, the list will stay empty
        workouts = []

"""
    Saves all workouts from the list to the text file. Each workout will be saved in one line as: type,date,amount,unit
"""
def save_workouts():
    file = open(WORKOUT_FILE, "w")
    for w in workouts:
        line = w["type"] + "|" + w["date"] + "|" + w["amount"] + "|" + w["unit"] + "\n"
        file.write(line)
    file.close()

"""
    The main menu has four buttons: Add Workout, View Workouts,
    Track Progress, and Save and Exit.
"""
# This will show the main menu, with the different options for the user to use:  
def main_menu():

    # Workout program Title
    tk.Label(
        text="Workout Helper",
    ).pack(pady=(60, 10))

tk.Button(
    text="",
    
)

