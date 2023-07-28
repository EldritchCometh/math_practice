import tkinter as tk
from tkinter import ttk
from math_classes import MathProblems


class FlashCardsGame:

    def __init__(self, window_dims):
        self.root = tk.Tk()
        self.font_size = 132
        self.timer_duration = 30
        self.configure_window(window_dims)
        self.problems = MathProblems()
        self.current_frame = ProblemFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def configure_window(self, window_dims):
        self.root.title("Arithmetic Flashcards")
        x = (self.root.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.root.winfo_screenheight() - window_dims[1]) // 2
        self.root.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")


class ProblemFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.problem = parent.problems.get_prob()
        self.font_size = parent.font_size
        self.init = True
        self.failed = False
        self.timer = False
        self.question_frame = None
        self.question = None
        self.entry = None
        self.make_widgets()
        self.bind("<Configure>", self.resize_fonts)

    def make_widgets(self):
        self.configure_grid()
        self.make_question()
        self.make_entry()
        self.make_timer_bar()
        self.make_progress_bar()

    def configure_grid(self):
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1, minsize=20)
        self.grid_rowconfigure(2, weight=1, minsize=20)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.grid(row=0, column=0, sticky="nsew")
        question = ttk.Label(question_frame, text=self.problem.question)
        question.config(font=("Arial", self.parent.font_size))
        question.place(relx=0.5, rely=0.5, anchor='center')
        self.question_frame = question_frame
        self.question = question

    def make_entry(self):
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=1, sticky="nsew")
        entry = ttk.Entry(entry_frame, justify="center", width=2)
        entry.config(font=("Arial", self.parent.font_size))
        entry.pack(fill="both", expand=True)
        entry.focus_set()
        entry.bind("<Return>", self.check_answer)
        entry.bind("<KP_Enter>", self.check_answer)
        self.entry = entry

    def make_timer_bar(self):
        timer_frame = tk.Frame(self)
        timer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        timer = ttk.Progressbar(
            timer_frame,
            maximum=self.parent.timer_duration * 10,
            value=self.parent.timer_duration * 10)
        timer.pack(fill="both", expand=True)
        self.update_timer_bar(timer)

    def make_progress_bar(self):
        prog_frame = tk.Frame(self)
        prog_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        maximum = self.parent.problems.num_starting_probs
        prog = ttk.Progressbar(
            prog_frame,
            maximum=maximum,
            value=(maximum - self.parent.problems.remaining))
        prog.pack(fill="both", expand=True)

    def check_answer(self, event):
        try:
            answer = int(event.widget.get())
        except ValueError:
            return
        if answer == self.problem.answer:
            if not self.failed:
                self.parent.problems.rem_prob(self.problem)
            self.parent.get_new_prob()
        else:
            self.failed = True
            event.widget.delete(0, 'end')

    def update_timer_bar(self, timer):
        if not timer.winfo_exists():
            return
        if self.failed:
            return
        if timer['value'] <= 0:
            self.failed = True
        if self.timer:
            timer['value'] -= 1
        self.after(100, lambda: self.update_timer_bar(timer))

    def resize_fonts(self, _):
        if self.init:
            self.init = False
            return
        self.font_size = min(
            int(self.question_frame.winfo_width() * 0.176),
            int(self.question_frame.winfo_height() * 0.9))
        self.question.config(font=("Arial", self.font_size))
        self.entry.config(font=("Arial", self.font_size))


if __name__ == "__main__":

    window_dimensions = (1100, 200)
    game = FlashCardsGame(window_dimensions)
    game.root.mainloop()
