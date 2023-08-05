import tkinter as tk
from tkinter import ttk
from math_classes import MathProblems
from users import *


class FlashCardsGame:

    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.configure_window((1200, 325))
        self.problems = MathProblems(user)
        self.current_frame = ProblemFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def configure_window(self, window_dims):
        self.root.title("Arithmetic Flashcards")
        x = (self.root.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.root.winfo_screenheight() - window_dims[1]) // 2
        self.root.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")

    def get_new_prob(self):
        if self.problems.remaining <= 0:
            self.root.destroy()
            return
        self.current_frame.destroy()
        self.current_frame = ProblemFrame(self)
        self.current_frame.pack(fill="both", expand=True)


class ProblemFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.problem = parent.problems.get_prob()
        self.failed = False
        self.q_comps = []
        self.font_size = None
        self.progress_frame = None
        self.timer_frame = None
        self.make_timer_bar()
        self.make_progress_bar()
        self.make_question()
        self.bind("<Configure>", self.resize_elements)

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.pack(side='top', fill='y', expand=True, padx=6, pady=6)
        for t in self.problem.question_text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if t == '_':
                entry = tk.Entry(comp_frame, width=2)
                self.q_comps.append(entry)
                entry.pack(padx=3, pady=3)
                entry.focus_set()
                entry.bind("<Return>", self.check_answer)
                entry.bind("<KP_Enter>", self.check_answer)
            else:
                label = tk.Label(comp_frame, text=t)
                self.q_comps.append(label)
                label.pack(padx=3, pady=3)

    def make_progress_bar(self):
        self.progress_frame = ttk.Frame(self, height=30)
        self.progress_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        maximum = self.parent.problems.num_starting_probs
        progress_bar = ttk.Progressbar(
            self.progress_frame,
            maximum=maximum,
            value=(maximum - self.parent.problems.remaining))
        progress_bar.place(relx=0, rely=0, relwidth=1, relheight=1)

    def make_timer_bar(self):
        self.timer_frame = ttk.Frame(self, height=30)
        self.timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        timer_duration = self.parent.user.timer or 1
        timer_bar = ttk.Progressbar(
            self.timer_frame,
            maximum=timer_duration * 10,
            value=timer_duration * 10)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        if self.parent.user.timer:
            self.update_timer_bar(timer_bar)

    def update_timer_bar(self, timer_bar):
        if not timer_bar.winfo_exists():
            return
        elif self.failed:
            return
        elif timer_bar['value'] <= 0:
            self.failed = True
        else:
            timer_bar['value'] -= 1
        self.after(100, lambda: self.update_timer_bar(timer_bar))

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        self.font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp in self.q_comps:
            comp.config(font=("Arial", self.font_size))
        self.progress_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)

    def check_answer(self, event):
        try:
            answer = int(event.widget.get())
        except ValueError:
            return
        if answer == self.problem.variable:
            if not self.failed:
                self.parent.problems.rem_prob(self.problem)
            self.parent.get_new_prob()
        else:
            self.failed = True
            event.widget.delete(0, 'end')


if __name__ == "__main__":

    olive = Olive()
    game = FlashCardsGame(olive)
    game.root.mainloop()
