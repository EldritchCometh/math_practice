import tkinter as tk
from tkinter import ttk
from math_classes import *


countdown_id = None
num_starting_probs = 50
timer_duration = 5
failed = False


def make_window(window_size):

    window = tk.Tk()
    window.title("Arithmetic Flashcards")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_size[0]) // 2
    y = (screen_height - window_size[1]) // 2
    window.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")

    return window


def question(window, probs):

    global failed
    global num_starting_probs
    failed = False
    prob = probs.get_prob()
    global timer_duration

    for widget in window.winfo_children():
        widget.destroy()

    window.grid_rowconfigure(0, weight=5)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(0, weight=5)
    window.grid_columnconfigure(1, weight=1)

    question_frame = tk.Frame(window)
    question_frame.grid(row=0, column=0, sticky="nsew")
    label = ttk.Label(question_frame, text=prob.question, font=("Arial", 108))
    label.place(relx=0.5, rely=0.5, anchor='center')

    def check_answer(_):
        if not entry.get():
            print("no entry")
            return
        if int(entry.get().strip()) == prob.answer:
            global failed
            if not failed:
                probs.rem_prob(prob)
            if len(probs.probs) > 0:
                question(window, probs)
            else:
                window.destroy()
        else:
            failed = True
            if countdown_id:
                window.after_cancel(countdown_id)
            entry.delete(0, 'end')
    entry_frame = tk.Frame(window)
    entry_frame.grid(row=0, column=1, sticky="nsew")
    entry = ttk.Entry(
        entry_frame, justify="center", width=2, font=("Arial", 108))
    entry.pack(fill="both", expand=True)
    entry.bind("<Return>", check_answer)
    entry.bind("<KP_Enter>", check_answer)
    entry.focus_set()

    def resize_fonts(_=None):
        global window_size
        if not window_size == (window.winfo_width(), window.winfo_height()):
            window_size = (window.winfo_width(), window.winfo_height())
            font_size = min(
                int(window_size[0] * 0.11),
                int(window_size[1] * 0.7))
            label.config(font=("Arial", font_size))
            entry.config(font=("Arial", font_size))
    window.bind("<Configure>", resize_fonts)
    window.after_idle(resize_fonts)

    def timeout():
        global failed
        failed = True
    def countdown(time_period, timer_bar):
        if timer_bar.winfo_exists():
            value = timer_bar['value']
            if value > 0:
                timer_bar['value'] = value - 1
                global countdown_id
                countdown_id = window.after(
                    time_period, countdown, time_period, timer_bar)
            else:
                timeout()
    timer_frame = tk.Frame(window)
    timer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    timer = ttk.Progressbar(
        timer_frame, mode='determinate', maximum=100, value=100)
    timer.pack(fill="both", expand=True)
    countdown(timer_duration*10, timer)

    prog_frame = tk.Frame(window)
    prog_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
    progress = ttk.Progressbar(
        prog_frame,
        mode='determinate',
        maximum=num_starting_probs,
        value=len(problems.probs)
    )
    progress.pack(fill="both", expand=True)


window_size = (1100, 200)
window = make_window(window_size)

add_probs = AdditionProblems(1, 10)
sub_probs = SubtractionProblems(1, 10)
problems = MathProblems(num_starting_probs, add_probs, sub_probs)
question(window, problems)

window.mainloop()
