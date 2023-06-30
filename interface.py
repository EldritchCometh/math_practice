import tkinter as tk
from tkinter import ttk


class FlashCardsGame(tk.Tk):

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window(window_width, window_height)
        self.current_frame = Problem(self)
        self.current_frame.pack(fill="both", expand=True)

    def window(self, window_width, window_height):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_width) // 2
        y = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def problem_entry(self, entry):
        print(entry)


class Problem(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.make_grid()
        self.question_frame, self.question = self.make_question()
        self.entry_frame, self.entry = self.make_entry()
        self.make_timer_bar()
        self.make_progress_bar()
        self.last_window_size = (parent.winfo_width(), parent.winfo_height())
        self.bind("<Configure>", self.resize_fonts)
        # see if I can pass parent to resize_fonts()

    def resize_fonts(self, event):
        window_width = event.widget.winfo_width()
        window_height = event.widget.winfo_height()
        window_size = (window_width, window_height)
        if window_size != self.last_window_size:
            self.last_window_size = window_size
            font_size = min(
                int(self.question_frame.winfo_width() * 0.176),
                int(self.question_frame.winfo_height() * 0.9))
            self.question.config(font=("Arial", font_size))
            self.entry.config(font=("Arial", font_size))

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.grid(row=0, column=0, sticky="nsew")
        label = ttk.Label(question_frame, text="22 + 22 =", font=("Arial", 108))
        label.place(relx=0.5, rely=0.5, anchor='center')
        return question_frame, label

    def make_entry(self):
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=1, sticky="nsew")
        entry = ttk.Entry(
            entry_frame, justify="center", width=2, font=("Arial", 108))
        entry.pack(fill="both", expand=True)
        parent = self.parent
        entry.bind("<Return>", lambda _: parent.problem_entry(entry.get()))
        entry.bind("<KP_Enter>", lambda _: parent.problem_entry(entry.get()))
        entry.focus_set()
        return entry_frame, entry

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

    def make_grid(self):
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1, minsize=20)
        self.grid_rowconfigure(2, weight=1, minsize=20)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)


if __name__ == "__main__":

    window = FlashCardsGame(1100, 200)
    window.mainloop()
