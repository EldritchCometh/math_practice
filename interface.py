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
        self.q_comps = []
        self.problem = parent.problems.get_prob()
        self.font_size = parent.font_size
        self.init = True
        self.failed = False
        self.timer = False
        self.question_frame = None
        self.question = None
        self.entry = None
        self.progress_frame = None
        self.timer_frame = None
        self.make_progress_bar()
        self.make_timer_bar()
        self.make_question()
        self.bind("<Configure>", self.resize_elements)

    def make_progress_bar(self):
        self.progress_frame = ttk.Frame(self, height=30)
        self.progress_frame.pack(side='bottom', fill='x', padx=5, pady=(2, 4))
        progress_bar = ttk.Progressbar(self.progress_frame)
        progress_bar.place(relx=0, rely=0, relwidth=1, relheight=1)

    def make_timer_bar(self):
        self.timer_frame = ttk.Frame(self, height=30)
        self.timer_frame.pack(side='bottom', fill='x', padx=5, pady=(2, 4))
        timer_bar = ttk.Progressbar(self.timer_frame)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)

    def make_question(self):
        self.question_frame = tk.Frame(self)
        self.question_frame.pack(side='top', fill='y', expand=True)
        for t in self.text:
            comp_frame = tk.Frame(self.question_frame)
            comp_frame.pack(side='left', anchor='center')
            if t == '_':
                self.entry = tk.Entry(comp_frame, width=2, font=("Ariel", self.font_size))
                self.q_comps.append(self.entry)
                self.entry.pack()
            else:
                label = tk.Label(comp_frame, text=t, font=("Ariel", self.font_size))
                self.q_comps.append(label)
                label.pack()

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

    def resize_elements(self, _):
        w_height = self.winfo_height()
        prog_bars_heights = max(30, w_height * 0.05)
        self.progress_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)
        q_frame_height = w_height - (prog_bars_heights * 2 + 8)
        self.font_size = min(
            int(self.winfo_width() * 0.16),
            int(q_frame_height * 0.7))
        for comp in self.q_comps:
            comp.config(font=("Arial", self.font_size))


if __name__ == "__main__":

    window_dimensions = (1100, 200)
    game = FlashCardsGame(window_dimensions)
    game.root.mainloop()