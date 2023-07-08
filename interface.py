import tkinter as tk
from tkinter import ttk
from math_classes import MathProblems


class FlashCardsGame(tk.Tk):

    def __init__(self, window_dims):
        super().__init__()
        self.font = 132
        self.window(window_dims)
        self.problems = MathProblems()
        self.problem = self.problems.get_prob()
        self.current_frame = ProblemFrame(self.problem, self.font)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.entry.bind("<Return>", self.check_answer)
        self.current_frame.entry.bind("<KP_Enter>", self.check_answer)

    def window(self, window_dims):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.winfo_screenheight() - window_dims[1]) // 2
        self.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")

    def check_answer(self, event):
        if int(event.widget.get()) == self.problem.answer:
            self.problems.rem_prob(self.problem)
        self.font = self.current_frame.font_size
        self.problem = self.problems.get_prob()
        self.current_frame.destroy()
        self.current_frame = ProblemFrame(self.problem, self.font)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.entry.bind("<Return>", self.check_answer)
        self.current_frame.entry.bind("<KP_Enter>", self.check_answer)


class ProblemFrame(tk.Frame):

    def __init__(self, problem, font):
        super().__init__()
        self.init = True
        self.problem = problem
        self.question_frame = None
        self.question = None
        self.entry = None
        self.make_widgets()
        self.font_size = font
        self.bind("<Configure>", self.resize_fonts)

    def make_widgets(self):
        self.make_grid()
        self.make_question()
        self.make_entry()
        self.make_timer_bar()
        self.make_progress_bar()

    def make_grid(self):
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1, minsize=20)
        self.grid_rowconfigure(2, weight=1, minsize=20)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.grid(row=0, column=0, sticky="nsew")
        question = ttk.Label(question_frame, text=self.problem.question, font=("Arial", 108))
        question.place(relx=0.5, rely=0.5, anchor='center')
        self.question_frame = question_frame
        self.question = question

    def make_entry(self):
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=1, sticky="nsew")
        entry = ttk.Entry(
            entry_frame, justify="center", width=2, font=("Arial", 108))
        entry.pack(fill="both", expand=True)
        entry.focus_set()
        self.entry = entry

    def make_timer_bar(self):
        timer_frame = tk.Frame(self)
        timer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        timer = ttk.Progressbar(timer_frame, maximum=100, value=100)
        timer.pack(fill="both", expand=True)

    def make_progress_bar(self):
        prog_frame = tk.Frame(self)
        prog_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        prog = ttk.Progressbar(prog_frame, maximum=100, value=100)
        prog.pack(fill="both", expand=True)

    def resize_fonts(self, _):
        self.question.config(font=("Arial", self.font_size))
        self.entry.config(font=("Arial", self.font_size))
        if self.init:
            self.init = False
            return
        self.font_size = min(
            int(self.question_frame.winfo_width() * 0.176),
            int(self.question_frame.winfo_height() * 0.9))


if __name__ == "__main__":

    window_dimensions = (1100, 200)
    window = FlashCardsGame(window_dimensions)
    window.mainloop()
