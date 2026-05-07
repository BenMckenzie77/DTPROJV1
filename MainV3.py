# main.py
# NCEA Numeracy Quiz - main program
# Ben McKenzie 2026

# These import extra tools I need:
# tkinter lets me build the window and buttons
# random is used to shuffle the questions so they appear in a different order each time
# json lets me read the questions.json file
# os helps the program find the json file regardless of which folder it is saved in
import tkinter as tk
import random
import json
import os

# --- DYNAMIC FILE LOADING ---
# This part finds the folder where this script is saved and looks for questions.json there
# This prevents "File Not Found" errors on different computers
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "questions.json")

with open(json_path, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# Variables to track the quiz state
current_q = 0    # Which question number we are currently on
score = 0        # How many correct answers the user has got
questions = []   # The list of questions that will be shuffled
time_elapsed = 0 # Keeps track of how many seconds the quiz has been running
timer_job = None # A placeholder for the timer function so I can stop/start it

# --- THEME & STYLE SETTINGS ---
# Using the specific light blue hex code requested by the user
BG_COLOR = "#85E3FF" 
# Trebuchet MS is used as a 'softer' alternative to Arial
FONT_NAME = "Trebuchet MS" 

# Create the main window
window = tk.Tk()
window.title("Numeracy Quiz")
# Width is 750 to make sure long questions aren't squashed or cut off
window.geometry("750x480") 
window.resizable(False, False)
window.config(bg=BG_COLOR)

# --- HOME SCREEN ---
# This function builds and displays the home/title screen
def show_home():
    global timer_job
    # If the timer is running, stop it before going home
    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    # Clear the window of all current widgets to "change screens"
    for widget in window.winfo_children():
        widget.destroy()

    window.config(bg=BG_COLOR)

    # Title card: white background with a thick 2px black outline for a clean look
    # highlightthickness=2 ensures the black line goes right to the edge
    title_card = tk.Frame(window, bg="white", padx=30, pady=20, 
                          highlightthickness=2, highlightbackground="black")
    title_card.pack(pady=(50, 20), ipadx=10, ipady=6)

    tk.Label(title_card, text="NCEA Numeracy Co-Req Quiz",
             font=(FONT_NAME, 22, "bold"), bg="white", fg="black").pack(pady=(0, 6))
    
    tk.Label(title_card, text="Achievement Standards 91906 and 91907",
             font=(FONT_NAME, 12), bg="white", fg="black").pack()
    
    # Dynamically shows the total question count from the JSON file
    tk.Label(title_card, text=f"{len(QUESTIONS)} questions  |  70% to pass",
             font=(FONT_NAME, 11), bg="white", fg="black").pack(pady=(4, 0))

    # Start button: relief="flat" and highlightthickness=2 removes the white outer glow
    tk.Button(window, text="Start Quiz", command=start_quiz,
              font=(FONT_NAME, 13, "bold"), width=14, pady=8,
              bg="white", fg="black", relief="flat",
              highlightthickness=2, highlightbackground="black",
              activebackground="#e8e8e8", cursor="hand2").pack(pady=10)

    tk.Label(window, text="Ben McKenzie - Numeracy Quiz",
             font=(FONT_NAME, 9), bg=BG_COLOR, fg="black").pack(side="bottom", pady=10)


# --- START / RESTART QUIZ ---
# Resets the score and timer, shuffles the questions, and starts the clock
def start_quiz():
    global current_q, score, questions, time_elapsed
    current_q = 0
    score = 0
    time_elapsed = 0  
    questions = random.sample(QUESTIONS, len(QUESTIONS))
    show_question()
    update_timer()  


# --- TIMER FUNCTION ---
# This runs every 1 second (1000ms) to update the time display
def update_timer():
    global time_elapsed, timer_job
    time_elapsed += 1
    # divmod splits the total seconds into minutes and seconds
    mins, secs = divmod(time_elapsed, 60)
    
    if counter_label:
        counter_label.config(text=f"Question {current_q + 1} of {len(questions)}   |   Time: {mins:02d}:{secs:02d}")
    
    # This tells the window to run this same function again in 1 second
    timer_job = window.after(1000, update_timer)


# --- QUIZ SCREEN ---
# Global variables for the quiz widgets so they can be accessed by multiple functions
question_label = None
counter_label  = None
options_frame  = None
option_boxes   = []   
radio_buttons  = []   
selected       = None  
error_label    = None  
next_button    = None

def show_question():
    global question_label, counter_label, options_frame
    global option_boxes, radio_buttons, selected, error_label, next_button

    for widget in window.winfo_children():
        widget.destroy()

    window.config(bg=BG_COLOR)

    # wraplength=650 ensures the question text has room to spread out across the wider window
    question_label = tk.Label(window, text="", font=(FONT_NAME, 14), bg=BG_COLOR, fg="black",
                               wraplength=650, justify="center")
    question_label.pack(pady=(20, 5))

    # Shows the progress and the timer
    counter_label = tk.Label(window, text="", font=(FONT_NAME, 11, "bold"), bg=BG_COLOR, fg="black")
    counter_label.pack()

    selected = tk.StringVar()

    options_frame = tk.Frame(window, bg=BG_COLOR)
    options_frame.pack(pady=15)

    option_boxes  = []
    radio_buttons = []

    # Create 4 answer boxes
    for i in range(4):
        # highlightthickness=2 creates a bold black border around each white answer box
        box = tk.Frame(options_frame, bg="white", highlightthickness=2, 
                       highlightbackground="black", padx=15, pady=8)
        box.pack(fill="x", padx=60, pady=5, ipadx=10)

        # tristatevalue="x" is a trick to stop Mac computers from showing a blue minus sign
        rb = tk.Radiobutton(box, text="", variable=selected,
                            bg="white", fg="black", font=(FONT_NAME, 12),
                            anchor="w", activebackground="white", activeforeground="black",
                            selectcolor="black", cursor="hand2",
                            tristatevalue="x")
        rb.pack(anchor="w", fill="x")

        option_boxes.append(box)
        radio_buttons.append(rb)

    error_label = tk.Label(window, text="", fg="red", bg=BG_COLOR, font=(FONT_NAME, 10, "bold"))
    error_label.pack(pady=(2, 2))

    # The Check button - once clicked, it will turn the answer Green or Red
    next_button = tk.Button(window, text="Check", command=check_answer,
                            font=(FONT_NAME, 12, "bold"), width=12, pady=6,
                            bg="white", fg="black", relief="flat",
                            highlightthickness=2, highlightbackground="black",
                            activebackground="#e8e8e8", cursor="hand2")
    next_button.pack(pady=5)

    tk.Label(window, text="Ben McKenzie - Numeracy Quiz",
             font=(FONT_NAME, 9), bg=BG_COLOR, fg="black").pack(side="bottom", pady=10)

    load_question()


# Updates the text for the current question without redrawing the whole screen
def load_question():
    q = questions[current_q]
    question_label.config(text=f"Q{current_q + 1}. {q['question']}")
    selected.set("")
    error_label.config(text="")
    
    # Reset button back to enabled state with black text
    next_button.config(state="normal", text="Check", bg="white", fg="black")

    for i, rb in enumerate(radio_buttons):
        option_boxes[i].config(bg="white", highlightbackground="black")
        rb.config(text=q["options"][i], value=q["options"][i], bg="white", fg="black", state="normal")


# Checks if the answer is right and highlights the box green or red
def check_answer():
    global score
    ans = selected.get()
    
    # Stop the user if they haven't picked anything
    if ans == "":
        error_label.config(text="Please pick an answer!")
        return

    error_label.config(text="")
    # disabledforeground="black" forces the text to stay black even when the button is greyed out
    next_button.config(state="disabled", bg="#cccccc", disabledforeground="black")

    correct_ans = questions[current_q]["answer"]

    for i, rb in enumerate(radio_buttons):
        # Lock the radio buttons so they can't change their mind after checking
        rb.config(state="disabled")
        
        if rb.cget("value") == ans:
            if ans == correct_ans:
                option_boxes[i].config(bg="#a8f0a8") # Soft green for correct
                rb.config(bg="#a8f0a8", disabledforeground="black")
                score += 1
            else:
                option_boxes[i].config(bg="#f0a8a8") # Soft red for incorrect
                rb.config(bg="#f0a8a8", disabledforeground="black")
        else:
            rb.config(disabledforeground="black")

    # Wait for 1.2 seconds so the user can see the color result, then move to next question
    window.after(1200, advance_question)


def advance_question():
    global current_q
    current_q += 1
    if current_q < len(questions):
        load_question()
    else:
        show_result()


# --- RESULTS SCREEN ---
# Displays the final score and total time taken
def show_result():
    global timer_job
    # Stop the timer permanently when the quiz ends
    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    for widget in window.winfo_children():
        widget.destroy()

    total   = len(questions)
    percent = round((score / total) * 100)
    mins, secs = divmod(time_elapsed, 60)
    time_text = f"Total Time: {mins:02d}:{secs:02d}"

    # Determine if they passed based on the 70% threshold
    if percent >= 70:
        result_text   = f"You scored {score}/{total} ({percent}%) - PASSED!"
        result_colour = "green"
    else:
        result_text   = f"You scored {score}/{total} ({percent}%) - FAILED"
        result_colour = "red"

    window.config(bg=BG_COLOR)

    tk.Label(window, text="Quiz Finished!", font=(FONT_NAME, 20, "bold"),
             bg=BG_COLOR, fg="black").pack(pady=(40, 10))

    tk.Label(window, text=result_text, font=(FONT_NAME, 16, "bold"),
             fg=result_colour, bg=BG_COLOR).pack(pady=5)
             
    tk.Label(window, text=time_text, font=(FONT_NAME, 12),
             fg="black", bg=BG_COLOR).pack(pady=(0, 20))

    # Restart and Home buttons
    tk.Button(window, text="Try Again", command=start_quiz,
              font=(FONT_NAME, 11, "bold"), width=14, pady=8,
              bg="white", fg="black", relief="flat",
              highlightthickness=2, highlightbackground="black",
              activebackground="#e8e8e8", cursor="hand2").pack(pady=8)

    tk.Button(window, text="Back to Home", command=show_home,
              font=(FONT_NAME, 11, "bold"), width=14, pady=8,
              bg="white", fg="black", relief="flat",
              highlightthickness=2, highlightbackground="black",
              activebackground="#e8e8e8", cursor="hand2").pack()

    tk.Label(window, text="Ben McKenzie - Numeracy Quiz",
             font=(FONT_NAME, 9), bg=BG_COLOR, fg="black").pack(side="bottom", pady=10)


show_home()
window.mainloop()
