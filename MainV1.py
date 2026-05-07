# main.py
# NCEA Numeracy Quiz - main program (VERSION 1 - BASIC)
# Ben McKenzie 2026

# These import extra tools I need:
# tkinter lets me build the window and buttons
# random is used to shuffle the questions so they appear in a different order each time
# json lets me read the questions.json file
import tkinter as tk
import json
import os

# --- FILE LOADING ---
# Finding the file path so it works on any computer
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "questions.json")

# Open the questions file and load all the questions into a variable called QUESTIONS
with open(json_path, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# These three variables keep track of where we are in the quiz
current_q = 0
score = 0
questions = QUESTIONS  # In V1, we just use the list as-is without shuffling

# Create the main window
window = tk.Tk()
window.title("Numeracy Quiz")
window.geometry("500x400") # Smaller, more basic size

# --- HOME SCREEN ---
def show_home():
    for widget in window.winfo_children():
        widget.destroy()

    # Basic labels without the "Card" frame
    tk.Label(window, text="Numeracy Quiz", font=("Arial", 18)).pack(pady=20)
    tk.Label(window, text="20 Questions").pack()

    # Simple button
    tk.Button(window, text="Start", command=start_quiz, width=10).pack(pady=20)

# --- START QUIZ ---
def start_quiz():
    global current_q, score
    current_q = 0
    score = 0
    show_question()

# --- QUIZ SCREEN ---
selected = None

def show_question():
    global selected
    for widget in window.winfo_children():
        widget.destroy()

    q_data = questions[current_q]

    # Simple question label
    tk.Label(window, text=f"Question {current_q + 1}", font=("Arial", 12)).pack(pady=10)
    tk.Label(window, text=q_data["question"], wraplength=400).pack(pady=10)

    selected = tk.StringVar()

    # Basic Radiobuttons without the fancy white boxes or padding
    for option in q_data["options"]:
        tk.Radiobutton(window, text=option, variable=selected, value=option).pack(anchor="w", padx=50)

    # Simple button
    tk.Button(window, text="Next", command=next_question).pack(pady=20)

def next_question():
    global current_q, score

    if selected.get() == "":
        return # Just does nothing if not selected (very basic)

    if selected.get() == questions[current_q]["answer"]:
        score += 1

    current_q += 1

    if current_q < len(questions):
        show_question()
    else:
        show_result()

# --- RESULTS SCREEN ---
def show_result():
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text="Finished!", font=("Arial", 18)).pack(pady=20)
    tk.Label(window, text=f"Score: {score}/{len(questions)}").pack(pady=10)
    
    tk.Button(window, text="Restart", command=show_home).pack(pady=10)

# Start the program
show_home()
window.mainloop()
