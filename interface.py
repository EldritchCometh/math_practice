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
        self.text = ['19', '+', '_', '=', '31']
        self.problem = parent.problems.get_prob()
        self.font_size = parent.font_size
        self.init = True
        self.failed = False
        self.timer = False
        self.question_frame = None
        self.question = None
        self.entry = None
        self.make_question()
        self.make_timer_bar()
        self.make_progress_bar()
        self.bind("<Configure>", self.resize_fonts)

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.pack(fill='y', padx=10, pady=10, expand=True)
        for t in self.text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left')
            if t == '_':
                self.entry = tk.Entry(comp_frame)
                self.entry.pack()
            else:
                label = tk.Label(comp_frame, text=t, font=("Ariel", 16))
                label.pack()

    def make_timer_bar(self):
        timer_frame = tk.Frame(self, height=30)
        timer_frame.pack(fill='x', padx=5, pady=2)
        timer_frame.pack_propagate(0)
        timer_bar = ttk.Progressbar(timer_frame)
        timer_bar.pack(fill='both', expand=1)

    def make_progress_bar(self):
        prog_frame = tk.Frame(self, height=30)
        prog_frame.pack(fill='x', padx=5, pady=(2, 4))
        prog_frame.pack_propagate(0)
        prog_bar = ttk.Progressbar(prog_frame)
        prog_bar.pack(fill='both', expand=1)

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
