import tkinter as tk
from tkinter import messagebox

# Name of the file that going to be used to store workout data.
WORKOUT_FILE = "Workouts.txt"

# This list will hold all the workouts as dictionaries.
workouts = []

"""
    This function tries to open the workout file and load data into the list.
    If the file doesn't exist yet, the list will stay empty.
    Each line in the file is stored as: type, date, amount, unit
"""
def load_workouts():
    try:# This will try to open and read the workout file.
        file = open(WORKOUT_FILE, "r")
        lines = file.readlines()
        file.close()

 # This will loop through each line and split it into a dictionary.
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
    except FileNotFoundError:  # If the file doesn't exist the list will stay empty.
        workouts = []

"""
    Saves all workouts from the list to the text file. 
    Each workout will be saved in one line as: type,date,amount,unit
"""
def save_workouts():
    file = open(WORKOUT_FILE, "w")
    for w in workouts:
        line = w["type"] + "|" + w["date"] + "|" + w["amount"] + "|" + w["unit"] + "\n"
        file.write(line)
    file.close()


"""
    Hides all frames then shows only the one passed in.
    This function helps us switch between screens.
"""
def show_frame(frame):
    for f in all_frames:
        f.pack_forget()
    frame.pack(fill="both", expand=True)


"""
    This will show the main menu, with the different options for the user to use:
    Add workout, View workout, Track Progress, Save & Exit.
"""
def main_menu():
    frame = tk.Frame(root, bg="white")

    # Workout program Title and heading
    tk.Label(
            text="Workout Helper",
    ).pack(pady=(60, 10))

    tk.Label(
            frame,
            text="Lets workout",
    ).pack(pady=(0, 35))


# Buttons for the different options in the program:
# Add workout, View Workout, Track Progress, Save and Exit.

    tk.Button(
        frame, text="Add Workout",    
        width=22, pady=8,
        command=lambda: show_frame(add_frame)
    ).pack(pady=6)

    tk.Button(
        frame, text="View Workout",
        width=22, pady=8,
        command=view_workout
    ).pack(pady=6)
    
    tk.Button(
        frame, text="Track Progress",
        width=22, pady=8,
        command=track_progress
    ).pack(pady=6)

    tk.Button(
        frame, text="Save and Exit",
        width=22, pady=8,
        command=save_and_exit
    ).pack(pady=6)


"""
 Makes the 'Add Workout' work for the program.
 Includes input boxes for workout type, date, amount, and units.
 Checks for errors before saving everything to the workouts list.
"""
def add_frames():
    frame = tk.Frame(root)

    tk.label(
        frame, text="Add Workout",
    ).pack(pady=(25, 18))

 # Forms a container using the grid layout
    form = tk.Frame(frame)
    form.pack(padx=80)

 # Workout type option
    tk.Label(
        form, text="Workout Type:", anchor="w" 
    ).grid(row=0, column=0, sticky="w", pady=7)
    type_entry = tk.Entry(form, width=26)
    type_entry.grid(row=0, column=1, padx=12, pady=7)

# Setting the Data into a Date, Month, Year
    tk.Label(
        form, text="Date (DD/MM/YYYY):", anchor="w"
    ).grid(row=1, column=0, sticky="w", pady=7)
    date_entry = tk.Entry(form, width=26)
    date_entry.grid(row=1, column=1, padx=12, pady=7)

# Asking the amount
    tk.Label(
        form, text="amount: ", anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=7)

    tk.Label(
        form, text="Unit  (km / reps / mins):", anchor="w"
    ).grid(row=3, column=0, sticky="w", pady=7)
    unit_entry = tk.Entry(form, width=26)
    unit_entry.grid(row=3, column=1, padx=12, pady=7)

"""
    Reads the information inputed and checks them to see if they are valid or not.
    If valid: add to workouts list and show success.
    If invalid: shows an error message and does not save.
"""
def saving_data():
    workout_type = type_entry.get().strip()
    date= date_entry.get().strip()
    amount= amount_entry.get().strip()
    unit= unit_entry.get().strip()
    if workout_type == "" or date == "" or amount == "" or unit == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

  # Checking if the amount is a number 
    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
    
# If it's a Valid input, then add workout to the list 
    new_workout = {
        "type":   workout_type,
        "date":   date,
        "amount": amount,
        "unit":   unit
    }
    workouts.append(new_workout)


# Clear amount so it's ready for next entry
    amount_entry.delete(0, tk.END)

# Show success message then go back to main menu
    messagebox.showinfo("Success", "Workout added successfully!")
    show_frame(main_frame)

# Save and Back buttons
    btn_row = tk.Frame(frame)
    btn_row.pack(pady=18)

    tk.Button(
        btn_row, text="Save Workout",
        command=handle_save, width=16, pady=7, fg="white"
    ).pack(side="left", padx=8)
        
    tk.Button(
        btn_row, text="Back",
        command=lambda: show_frame(main_frame),
        width=10, pady=7
    ).pack(side="left", padx=8)


"""
    This function builds and returns the View Workouts frame.
    Has a text box that gets filled with workout data when opened.
"""
def view_frames():
    frame = tk.Frame(root)
    tk.Label(
        frame, text="View Workouts",
        font=("Arial", 18, "bold")
    ).pack(pady=(25, 12))

# Text box to display the workout list
    text_box = tk.Text(
        frame, width=58, height=14,
        font=("Courier", 10), state="disabled" # This "disabled" stops the user typing in it
    )
    text_box.pack(padx=16)

# Store reference to the text box on the frame object,  so view_screen() can update it.
    frame.text_box = text_box

    tk.Button(
        frame, text="Back",
        command=lambda: show_frame(main_frame),
        width=10, pady=6
    ).pack(pady=10)

    return frame

"""
    Fills the view text box with  workout data
    then navigates to the view screen.
    Checks if the list is empty first.
"""

def view_screen():
    text_box = view_frame.text_box
 
# This enables editing so they can update the content
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    
#    
    if len(workouts) == 0:
        text_box.insert(tk.END, "No workouts logged yet.\n")
        text_box.insert(tk.END, "Use 'Add Workout' to get started.\n")
    else: #
        header = f"  {'Type':<16} {'Date':<14} {'Amount':<10} Unit\n"
        text_box.insert(tk.END, header)
        text_box.insert(tk.END, "  " + "-" * 50 + "\n")
        for w in workouts:
            line = (
                f"  {w['type']:<16} {w['date']:<14}"
                f" {w['amount']:<10} {w['unit']}\n"
            )
            text_box.insert(tk.END, line)
 
 #
    text_box.config(state="disabled")
    show_frame(view_frame)



load_workouts()
root = tk.TK()
root.title("Workout Program")
root.mainloop