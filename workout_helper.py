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

#FIXED: This will define the all_frame function
all_frames = []

# Font sizes increased to be clear and readable while moving around
FONT_TITLE = ("Arial", 22, "bold")
FONT_LABEL = ("Arial", 13, "bold")
FONT_ENTRY = ("Arial", 12)
FONT_BTN = ("Arial", 12, "bold")

# High-energy fitness app color scheme
COLOUR_BG = "#1e293b"        # Dark slate blue for the background
COLOUR_CARD = "#334155"      # Lighter slate blue for the containers
COLOUR_TEXT = "#ffffff"      # High contrast white for the text
COLOUR_ACCENT = "#0ea5e9"    # Neon blue for the buttons

def reset_and_go_home():
    # Making this function'global' will make any function that calls on it find it.
    global type_dropdown, date_entry, amount_entry, unit_dropdown
    
    type_dropdown.set("Select Type")
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    unit_dropdown.set("Select Unit")
    
    # Takes the user back to the main menu
    show_frame(main_frame)

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
    frame = tk.Frame(root, bg=COLOUR_BG)

    # Title heading for the member login page
    tk.Label(frame, text="FITNESS LOGIN", font=FONT_TITLE, fg=COLOUR_ACCENT, bg=COLOUR_BG).pack(pady=(120, 30))
    
    login_box = tk.Frame(frame, bg=COLOUR_CARD, padx=40, pady=30)
    login_box.pack()

    # Adds color and layout details to the entry frame
    tk.Label(login_box, text="Enter Name To Begin:", font=FONT_LABEL, fg=COLOUR_TEXT, bg=COLOUR_CARD).pack(anchor="w", pady=5)
    user_entry = tk.Entry(login_box, font=FONT_ENTRY, width=30)
    user_entry.pack(pady=5)
    
    def process_login():
        global current_user
        username = user_entry.get().strip()

        # Checks if the entry box is completely blank
        if username == "":
            messagebox.showerror("Error", "Please enter your name to start.")
            return
        current_user = username
        show_frame(main_frame)

    # Button that checks entry data and unlocks the main program
    tk.Button(frame, text="Enter Program", font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_ACCENT, width=20, pady=8, command=process_login).pack(pady=30)
    return frame

"""
    This will show the main menu, with the different options for the user to use:
    Add workout, View workout, Track Progress, Save & Exit.
"""
def main_menu():
    frame = tk.Frame(root, bg=COLOUR_BG)

    # Workout program Title and heading
    tk.Label(
        frame,
        text="Workout Helper",
        font=FONT_TITLE,
        fg=COLOUR_TEXT,
        bg=COLOUR_BG
    ).pack(pady=(60, 10))

    tk.Label(
        frame,
        text="Lets workout",
         font=FONT_LABEL,
        fg=COLOUR_ACCENT,
        bg=COLOUR_BG
    ).pack(pady=(0, 35))


# Buttons for the different options in the program:
# Add workout, View Workout, Track Progress, Save and Exit.

    tk.Button(
        frame, text="Add Workout",    
        width=22, pady=8,
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD,
        activebackground=COLOUR_ACCENT, activeforeground=COLOUR_TEXT,
        command=lambda: show_frame(add_frame)
    ).pack(pady=6)

# FIXED: Linked directly to view_screen so the data populates and navigates
    tk.Button(
        frame, text="View Workout",
        width=22, pady=8,
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD,
        activebackground=COLOUR_ACCENT, activeforeground=COLOUR_TEXT,
        command = view_screen
    ).pack(pady=6)
    
    # FIXED: Linked directly to progress_screen so the stats are compiled and shown
    tk.Button(
        frame, text="Track Progress",
        width=22, pady=8,
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD,
        activebackground=COLOUR_ACCENT, activeforeground=COLOUR_TEXT,
        command = progress_screen
    ).pack(pady=6)

    tk.Button(
        frame, text="Save and Exit",
        width=22, pady=8,
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD,
        activebackground=COLOUR_ACCENT, activeforeground=COLOUR_TEXT,
        command=save_and_exit
    ).pack(pady=6)

    return frame

"""
 Makes the 'Add Workout' work for the program.
 Includes input boxes for workout type, date, amount, and units.
 Checks for errors before saving everything to the workouts list.
"""
def add_workout():
 
# This will set up a style controller for the dropdown boxes
    style = ttk.Style()
    style.theme_use('clam') #'clam' will allow a custom colouring of dropdown fields
    
# This will make the Combobox style to be more readable
    style.configure("TCombobox", # FIXED: I added "font=FONT_ENTRY" inside the style configure to force the dropdown text 
                    fieldbackground="#ffffff", # Makes the field box pure white
                    foreground="#000000", # Makes the text bold pure black
                    background=COLOUR_ACCENT, # Makes the arrow button neon blue
                    font=FONT_ENTRY)

    global type_dropdown, date_entry, amount_entry, unit_dropdown

    frame = tk.Frame(root, bg=COLOUR_BG)

    tk.Label(
        frame, text="Add Workout",
        font=FONT_TITLE, fg=COLOUR_ACCENT, bg=COLOUR_BG
    ).pack(pady=(25, 18))

 # Forms a container using the grid layout
    form = tk.Frame(frame, bg=COLOUR_CARD, padx=40, pady=25)
    form.pack(padx=80)

# Dropdown code for workout option selection
    tk.Label(form, text="Workout Type:", font=FONT_LABEL, fg=COLOUR_TEXT, bg=COLOUR_CARD, anchor="w").grid(row=0, column=0, sticky="w", pady=7)
    type_dropdown = ttk.Combobox(form, values=["Push Ups", "Handstand", "Running", "Weightlifting", "Squats", "Cycling", "Pull Ups"], width=24, state="readonly") #FIXED: Adjusted width to 24 so it lines up with entry fields perfectly
    type_dropdown.grid(row=0, column=1, padx=12, pady=7)
    type_dropdown.set("Select Type")

# Setting the Data into a Date, Month, Year
    tk.Label( #FIXED: Added font, fg, and bg to this label
        form, text="Date (DD/MM/YYYY):", font=FONT_LABEL, fg=COLOUR_TEXT, bg=COLOUR_CARD, anchor="w",
    ).grid(row=1, column=0, sticky="w", pady=7)
    date_entry = tk.Entry(form, font=FONT_ENTRY, width=26) # FIXED: added Font
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
        form, text="Amount: ", font=FONT_LABEL, fg=COLOUR_TEXT, bg=COLOUR_CARD, anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=7)
    amount_entry = tk.Entry(form,  font=FONT_ENTRY, width=26)
    amount_entry.grid(row=2, column=1, padx=12, pady=7)
    

    # Dropdown Code for Unit selection
    # FIXED: Added font, fg and bg properties to this label. As well as removed font=FONT_ENTRY
    tk.Label(form, text="Unit  (km / reps / mins):",  font=FONT_LABEL, fg=COLOUR_TEXT, bg=COLOUR_CARD, anchor="w").grid(row=3, column=0, sticky="w", pady=7)
    unit_dropdown = ttk.Combobox(form, values=["reps", "mins", "km", "kg",  "lbs", "meters"], width=24, state="readonly") #FIXED: Adjusted width to 24
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
    
        reset_and_go_home()

    # Save and Back buttons
    # FIXED: These buttons are now unindented so they display when the frame loads
    btn_row = tk.Frame(frame, bg=COLOUR_BG)
    btn_row.pack(pady=18)

    tk.Button(
        btn_row, text="Save Workout", font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_ACCENT, width=16, pady=7,
        command = saving_data, 
    ).pack(side="left", padx=8)
        
    tk.Button(
        btn_row, text="Back", font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD, width=10, pady=7,
        command=reset_and_go_home,
    ).pack(side="left", padx=8)
    return frame

"""
    This function builds and returns the View Workouts frame.
    Has a text box that gets filled with workout data when opened.
"""
def view_workout():
    frame = tk.Frame(root, bg=COLOUR_BG)
    tk.Label(
        frame, text="View Workouts",
        font=FONT_TITLE, fg=COLOUR_ACCENT, bg=COLOUR_BG
    ).pack(pady=(25, 12))

# Text box to display the workout list
    text_box = tk.Text(
        frame, width=65, height=14,
        # This "disabled" stops the user typing in it
        font=("Courier", 11), state="disabled",
        bg=COLOUR_CARD, fg=COLOUR_TEXT, insertbackground=COLOUR_TEXT
    )
    text_box.pack(padx=16)

# Store reference to the text box on the frame object,  so view_screen() can update it.
    frame.text_box = text_box

    tk.Button(
        frame, text="Back",
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD, width=10, pady=6,
        command=lambda: show_frame(main_frame),
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
    
    # This gets data matching the logged in user
    user_data = [w for w in workouts if w.get("user", "test") == current_user or current_user == "test"]

# This will check if there is enough data
    if len(user_data) == 0:
        text_box.insert(tk.END, "No workouts logged yet for member.\n")
        text_box.insert(tk.END, "Use 'Add Workout' to get started.\n")
    else: #
        header = f"  {'Type':<16} {'Date':<14} {'Amount':<10} Unit\n"
        text_box.insert(tk.END, header)
        text_box.insert(tk.END, "  " + "-" * 50 + "\n")
        for w in user_data:
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
    frame = tk.Frame(root, bg=COLOUR_BG)
 
    tk.Label(
        frame, text="Track Progress Results",
        font=FONT_TITLE, fg=COLOUR_ACCENT , bg=COLOUR_BG
    ).pack(pady=(25, 12))
 
 # This will show a text box for the progress summary
    progress_text = tk.Text(
        frame, width=65, height=14,
        font=("Courier", 11), state="disabled",
        bg=COLOUR_CARD, fg=COLOUR_TEXT
    )
    progress_text.pack(padx=16)

 # This will store references so progress_screen() can update it
    frame.progress_text = progress_text
 
    tk.Button(
        frame, text="Back",
        font=FONT_BTN, fg=COLOUR_TEXT, bg=COLOUR_CARD,
        command=reset_and_go_home,  # FIXED: I took away the lambda block so the global function works properly
        width=10, pady=6,
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

# This filters data so calculations are private to only the user
    user_data = [w for w in workouts if w.get("user", "test") == current_user or current_user == "test"] # FIXED: I add a keyword to check old historical data so the lines load for "test"


# This will check if there is enough data
    if len(user_data) == 0:
        p_text.insert(tk.END, f"\n  Not enough data to show progress for member: {current_user}.\n\n")
        p_text.insert(tk.END, "  Add at least one workout first.\n")
    else:
        # If there's enough data, it will calculate and display the progress 
        p_text.insert(tk.END, f"  FITNESS LOG ANALYSIS FOR: {current_user.upper()}\n")
        p_text.insert(tk.END, f"  Total sessions logged: {len(user_data)}\n")
        p_text.insert(tk.END, "  " + "=" * 52 + "\n\n")
        p_text.insert(tk.END, f"  {'EXERCISE TYPE':<18} {'SESSIONS':<12} {'PERSONAL RECORD (PR)':<15}\n")
        p_text.insert(tk.END, "  " + "-" * 52 + "\n")

# This will Scans entries to locate maximum values achieved per exercise type
        # It uses a dictionary to track counts
        stats = {}  # FIXED: I added this loop inside the else statement block
        for w in user_data:
            w_type = w["type"]
            amount = float(w["amount"])
            unit = w["unit"]
                
            if w_type not in stats:
                    stats[w_type] = {"count": 0, "max_value": amount, "unit": unit}

            # Added session count tracker
            stats[w_type]["count"] += 1

            # If the current amount is bigger than our old max, overwrite it as the new Personal Record
            if amount > stats[w_type]["max_value"]:
                stats[w_type]["max_value"] = amount

    for w_type, data in stats.items():
        line = f"  {w_type:<18} {data['count']:<12} {data['max_value']} {data['unit']}\n"
        p_text.insert(tk.END, line)
 
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
style.configure("TCombobox", fieldbackground=COLOUR_CARD, background=COLOUR_ACCENT, foreground=COLOUR_TEXT, arrowcolor=COLOUR_TEXT)

main_frame = None
add_frame = None
view_frame = None
track_frame = None
login_frame = None
all_frames = []

main_frame = main_menu()
add_frame = add_workout()
view_frame = view_workout()
track_frame = track_progress()
login_frame = login_screen()

all_frames = [main_frame, add_frame, view_frame, track_frame, login_frame]

show_frame(login_frame)

root.protocol("WM_DELETE_WINDOW", save_and_exit)

root.mainloop()