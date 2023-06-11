import tkinter as tk

def check_answer():
    # Check the user's answer and provide feedback
    pass

def generate_question():
    # Generate a new arithmetic question
    pass

def next_question():
    # Clear the answer entry and generate a new question
    pass

# Create the main window
window = tk.Tk()
window.title("Arithmetic Flashcards")

# Create the question label
question_label = tk.Label(window, text="Question: 2 + 3")
question_label.pack()

# Create the answer entry field
answer_entry = tk.Entry(window)
answer_entry.pack()

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=check_answer)
submit_button.pack()

# Create the next button
next_button = tk.Button(window, text="Next", command=next_question)
next_button.pack()

# Start the main loop
window.mainloop()
