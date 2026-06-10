import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # dropdown code option
from datetime import datetime # Added for calendar checks 

# Version 2 User Tracker
current_user = ""

# Name of the file that going to be used to store workout data.
WORKOUT_FILE = "Workouts.txt"

# This list will hold all the workouts as dictionaries.
workouts = []

# Font sizes increased to be clear and readable while moving around
FONT_TITLE = ("Arial", 22, "bold")
FONT_LABEL = ("Arial", 13, "bold")
FONT_ENTRY = ("Arial", 12)
FONT_BTN = ("Arial", 12, "bold")

# High-energy fitness app color scheme
COLOR_BG = "#1e293b"        # Dark slate blue for the background
COLOR_CARD = "#334155"      # Lighter slate blue for the containers
COLOR_TEXT = "#ffffff"      # High contrast white for the text
COLOR_ACCENT = "#0ea5e9"    # Neon blue for the buttons

"""
    This function tries to open the workout file and load data into the list.
    If the file doesn't exist yet, the list will stay empty.
    Each line in the file is stored as: type, date, amount, unit
"""
def load_workouts():
# This will try to open and read the workout file.
    global workouts
    try:
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
    This will show a personalised login and signup page for fitness members on startup.
    It securely captures the username so individual profiles can manage their own data.
"""
def login_screen():
    frame = tk.Frame(root, bg=COLOR_BG)

    # Title heading for the member login page
    tk.Label(frame, text="FITNESS MEMBER LOGIN", font=FONT_TITLE, fg=COLOR_ACCENT, bg=COLOR_BG).pack(pady=(120, 30))
    
    login_box = tk.Frame(frame, bg=COLOR_CARD, padx=40, pady=30)
    login_box.pack()

    # Adds color and layout details to the entry frame
    tk.Label(login_box, text="Username / Member Name:", font=FONT_LABEL, fg=COLOR_TEXT, bg=COLOR_CARD).pack(anchor="w", pady=5)
    user_entry = tk.Entry(login_box, font=FONT_ENTRY, width=30)
    user_entry.pack(pady=5)
    
    def process_login():
        global current_user
        username = user_entry.get().strip()

        # Checks if the entry box is completely blank
        if username == "":
            messagebox.showerror("Error", "Please enter your member name to start.")
            return
        current_user = username
        show_frame(main_frame)

    # Button that checks entry data and unlocks the main program
    tk.Button(frame, text="Enter Program", font=FONT_BTN, fg=COLOR_TEXT, bg=COLOR_ACCENT, width=20, pady=8, command=process_login).pack(pady=30)
    return frame

"""
    Wipes all previously inputted data from the form fields.
    This resets dropdowns and text boxes before loading the add workout screen.
"""
def reset_input():
    ropdown.set("Select Type")
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    unit_dropdown.set("Select Unit")
    show_frame(add_frame)
"""
    This will show the main menu, with the different options for the user to use:
    Add workout, View workout, Track Progress, Save & Exit.
"""
def main_menu():
    frame = tk.Frame(root, bg="#f0f0f0")

    # Workout program Title and heading
    tk.Label(
        frame,
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

# FIXED: Linked directly to view_screen so the data populates and navigates
    tk.Button(
        frame, text="View Workout",
        width=22, pady=8,
        command = view_screen
    ).pack(pady=6)
    
    # FIXED: Linked directly to progress_screen so the stats are compiled and shown
    tk.Button(
        frame, text="Track Progress",
        width=22, pady=8,
        command = progress_screen
    ).pack(pady=6)

    tk.Button(
        frame, text="Save and Exit",
        width=22, pady=8,
        command=save_and_exit
    ).pack(pady=6)

    return frame

"""
 Makes the 'Add Workout' work for the program.
 Includes input boxes for workout type, date, amount, and units.
 Checks for errors before saving everything to the workouts list.
"""
def add_frame():
    global type_dropdown, date_entry, amount_entry, unit_dropdown

    frame = tk.Frame(root, bg=COLOR_BG)

    tk.Label(
        frame, text="Add Workout",
        font=FONT_TITLE, fg=COLOR_ACCENT, bg=COLOR_BG
    ).pack(pady=(25, 18))

 # Forms a container using the grid layout
    form = tk.Frame(frame, bg=COLOR_CARD, padx=40, pady=25)
    form.pack(padx=80)

# Dropdown code for workout option selection
    tk.Label(form, text="Workout Type:", font=FONT_LABEL, fg=COLOR_TEXT, bg=COLOR_CARD, anchor="w").grid(row=0, column=0, sticky="w", pady=7)
    type_dropdown = ttk.Combobox(form, values=["Push Ups", "Handstand", "Running", "Weightlifting", "Squats", "Cycling", "Pull Ups"], width=23, state="readonly")
    type_dropdown.grid(row=0, column=1, padx=12, pady=7)
    type_dropdown.set("Select Type")

# Setting the Data into a Date, Month, Year
    tk.Label(
        form, text="Date (DD/MM/YYYY):", anchor="w"
    ).grid(row=1, column=0, sticky="w", pady=7)
    date_entry = tk.Entry(form, width=26)
    date_entry.grid(row=1, column=1, padx=12, pady=7)

# This will automatically adds slashes as the user types 
    def auto_slash(event):
        if event.keysym == "Backspace":
            return
        cur_text = date_entry.get()
        if len(cur_text) == 2 or len(cur_text) == 5:
            date_entry.insert(tk.END, "/")

# This binds the keyboard event to the date text box
    date_entry.bind("<KeyRelease>", auto_slash)

# Asking the amount
    tk.Label(
        form, text="Amount: ", font=FONT_LABEL, fg=COLOR_TEXT, bg=COLOR_CARD, anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=7)
    amount_entry = tk.Entry(form,  font=FONT_ENTRY, width=26)
    amount_entry.grid(row=2, column=1, padx=12, pady=7)
    

    # Dropdown Code for Unit selection
    tk.Label(form, text="Unit  (km / reps / mins):", anchor="w").grid(row=3, column=0, sticky="w", pady=7)
    unit_dropdown = ttk.Combobox(form,  font=FONT_ENTRY, values=["reps", "mins", "km", "kg",  "lbs", "meters"], width=23, state="readonly")
    unit_dropdown.grid(row=3, column=1, padx=12, pady=7)
    unit_dropdown.set("Select Unit")

    """
        Reads the information inputed and checks them to see if they are valid or not.
        If valid: add to workouts list and show success.
        If invalid: shows an error message and does not save.
    """
    def saving_data():
    # Creating the Dropdown code
        workout_type = type_dropdown.get()
        date = date_entry.get()
        amount = amount_entry.get()
        unit = unit_dropdown.get().strip()
        if workout_type == "Select Type" or unit == "Select Unit" or workout_type == "" or date == "" or amount == "" or unit == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

    # Checking if the calendar is using datetime to stop impossible dates
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid, real calendar date.")
            return 

    # Checking if the amount is a valid number 
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return # I added this so it stops saving data if it hits an error


    # If it's a Valid input, then add workout to the list 
        new_workout = {
            "user":   current_user,
            "type":   workout_type,
            "date":   date,
            "amount": amount,
            "unit":   unit
        }
        workouts.append(new_workout)
        save_workouts()

    # Show success message then go back to main menu
        messagebox.showinfo("Success", "Workout added successfully!")
        show_frame(main_frame)

    # Save and Back buttons
    # FIXED: These buttons are now unindented so they display when the frame loads
    btn_row = tk.Frame(frame, bg=COLOR_BG)
    btn_row.pack(pady=18)

    tk.Button(
        btn_row, text="Save Workout", font=FONT_BTN, fg=COLOR_TEXT, bg=COLOR_ACCENT, width=16, pady=7,
        command = saving_data, 
    ).pack(side="left", padx=8)
        
    tk.Button(
        btn_row, text="Back", font=FONT_BTN, fg=COLOR_TEXT, bg=COLOR_CARD, width=10, pady=7,
        command=lambda: show_frame(main_frame),
    ).pack(side="left", padx=8)
    return frame

"""
    This function builds and returns the View Workouts frame.
    Has a text box that gets filled with workout data when opened.
"""
def view_workout():
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
 
 # Disables editing again
    text_box.config(state="disabled")
    show_frame(view_frame)


"""
    This Function builds and returns the Track Progress frame.
    Has a text box that shows a summary when opened.
"""

def track_progress():
    frame = tk.Frame(root, bg="#f0f0f0")
 
    tk.Label(
        frame, text="Track Progress",
        font=("Arial", 18, "bold"), bg="#f0f0f0"
    ).pack(pady=(25, 12))
 
 # This will show a text box for the progress summary
    progress_text = tk.Text(
        frame, width=58, height=14,
        font=("Courier", 10), state="disabled"
    )
    progress_text.pack(padx=16)

 # This will store references so progress_screen() can update it
    frame.progress_text = progress_text
 
    tk.Button(
        frame, text="Back",
        command=lambda: show_frame(main_frame),
        width=10, pady=6
    ).pack(pady=10)
    return frame

"""
    Checks if there is enough data to show progress.
    If no workouts logged: shows an insufficient data message.
    If workouts exist: calculates and displays session counts.
"""

def progress_screen():
    # FIXED: Changed from track_progress.progress_text to track_frame.progress_text
    p_text = track_frame.progress_text
    p_text.config(state="normal")
    p_text.delete("1.0", tk.END)

# This will check if there is enough data
    if len(workouts) == 0:
        # If there is not enough data, this mesage will show 
        p_text.insert(tk.END, " Not enough data to show progress.\n\n")
        p_text.insert(tk.END, " add at least one workout first.\n")
    else:
        # If there's enough data, it will calculate and display the progress 
        p_text.insert(tk.END, f"  Total sessions logged: {len(workouts)}\n")
        p_text.insert(tk.END, "  " + "-" * 35 + "\n\n")

# This will count how many sessions per workout type
        # It uses a dictionary to track counts
        type_counts = {}
        for w in workouts:
            w_type = w["type"]
            if w_type not in type_counts:
                type_counts[w_type] = 0
            type_counts[w_type] += 1

    p_text.insert(tk.END, "  Sessions by type:\n")
    for w_type, count in type_counts.items():
        p_text.insert(tk.END, f"    {w_type}: {count} session(s)\n")
 
    # This will disable editing again
    p_text.config(state="disabled")

     # FIXED: Changed from show_frame(track_progress) to show_frame(track_frame)
    show_frame(track_frame)
 
"""
    Saves all workouts to the text file then closes the program.
"""
def save_and_exit():
    save_workouts()
    messagebox.showinfo("Saved", "Workouts saved!\nGoodbye.")
    root.destroy()
  

load_workouts()
root = tk.Tk()
root.title("Workout Program")

# FIXED: Automatically launches the app window fully maximized on startup
root.state('zoomed')

# Sets the style parameters for the standard dropdown menus
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=COLOR_CARD, background=COLOR_ACCENT, foreground=COLOR_TEXT, arrowcolor=COLOR_TEXT)

main_frame = main_menu()
add_frame = add_frame()
view_frame = view_workout()
track_frame = track_progress()
login_frame = login_screen()

all_frames = [main_frame, add_frame, view_frame, track_frame, login_frame]

show_frame(login_frame)

root.protocol("WM_DELETE_WINDOW", save_and_exit)

root.mainloop()