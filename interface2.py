import tkinter as tk
from tkinter import ttk


class FlashCardsGame:

    def __init__(self, window_dims):
        self.root = tk.Tk()
        self.configure_window(window_dims)
        self.current_frame = ProblemFrame()
        self.current_frame.pack(fill="both", expand=True)

    def configure_window(self, window_dims):
        self.root.title("Arithmetic Flashcards")
        x = (self.root.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.root.winfo_screenheight() - window_dims[1]) // 2
        self.root.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")


class ProblemFrame(tk.Frame):

    def __init__(self):
        super().__init__()
        self.text = ['19', '+', '_', '=', '31']
        self.entry = None
        self.make_question_frame()
        self.make_timer_bar()
        self.make_progress_bar()

    def make_question_frame(self):
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


window_dimensions = (1100, 200)
game = FlashCardsGame(window_dimensions)
game.root.mainloop()
