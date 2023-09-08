
# move frame creation into its own method
# need to make my own layout system to stop components from jumping around
# make sure elements have the right size before flash_card is drawn
# clean up chatgpts helpful mess
# probems sometimes have their order switched on reappearence
# implement difficulty levels
# implement options and saved users


import random
import tkinter as tk
from tkinter import ttk
from operator import add, sub, mul


class Problem:

    def __init__(self, fst_operand, snd_operand, operator):
        self.fst_operand = fst_operand
        self.snd_operand = snd_operand
        self.operator = operator
        self.result = operator(fst_operand, snd_operand)
        self.var_idx = random.randint(0, 2)
        self.answer = [fst_operand, snd_operand, self.result][self.var_idx]

    @property
    def question(self):
        symbol = {add: '+', sub: '-', mul: '*'}[self.operator]
        comps = [self.fst_operand, self.snd_operand, self.result]
        comps[self.var_idx] = None
        if random.randint(0, 1):
            return [comps[0], symbol, comps[1], '=', comps[2]]
        else:
            return [comps[2], '=', comps[0], symbol, comps[1]]


class FlashCardsApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.configure_window((1200, 325))
        self.main_frame = FlashCardsGame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.finished = lambda: self.destroy()
        self.mainloop()

    def configure_window(self, window_dims):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.winfo_screenheight() - window_dims[1]) // 2
        self.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")


class FlashCardsGame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.failed = False
        self.starting = None
        self.remaining = None
        self.problem = None
        self.current_card = None
        self.problems = self.get_problem_set()
        self.next_flashcard()

    @staticmethod
    def generate_problems(range_min, range_max, opr):
        probs = []
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, opr)
                if 0 <= prob.result <= 99:
                    probs.append(prob)
        random.shuffle(probs)
        return probs

    def get_problem_set(self):
        prob_set = (
            self.generate_problems(*User.add_range, add)[:User.num_of_adds] +
            self.generate_problems(*User.sub_range, sub)[:User.num_of_subs] +
            self.generate_problems(*User.mul_range, mul)[:User.num_of_muls])
        random.shuffle(prob_set)
        prob_set = prob_set[:User.num_of_probs]
        self.starting = len(prob_set)
        self.remaining = self.starting
        return prob_set

    def next_flashcard(self):
        if self.current_card:
            self.current_card.pack_forget()
            self.current_card.destroy()
        self.problem = random.choice(self.problems)
        self.current_card = FlashCard(
            parent=self,
            q_text=self.problem.question,
            prog_bar_values=(self.starting, self.starting - self.remaining),
            on_entered=self.on_entered,
            on_timeup=lambda: setattr(self, 'failed', True))
        self.current_card.pack(fill="both", expand=True)

    def on_entered(self, event):
        try:
            answer = int(event.widget.get())
        except ValueError:
            return
        if answer == self.problem.answer:
            if not self.failed:
                self.problems.remove(self.problem)
                self.remaining = len(self.problems)
            self.failed = False
            if self.remaining > 0:
                self.next_flashcard()
            else:
                self.finished()
        else:
            self.failed = True
            self.current_card.on_failed()


class FlashCard(tk.Frame):

    def __init__(self, parent, q_text, prog_bar_values, on_entered, on_timeup):
        super().__init__(parent)
        self.q_text, self.prog_bar_values = q_text, prog_bar_values
        self.timer, self.entry, self.timer_bar = User.timer, None, None
        self.timer_frame, self.prog_frame, self.question_frame = None, None, None
        self.make_layout()
        self.start_timer(on_timeup)
        self.bind("<Configure>", self.resize_elements)
        self.entry.bind("<Return>", on_entered)
        self.entry.bind("<KP_Enter>", on_entered)

    def make_layout(self):
        self.timer_frame = self.make_timer_frame(height=30)
        self.prog_frame = self.make_prog_frame(height=30)
        self.question_frame = self.make_question_frame()
        self.timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        self.prog_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        self.question_frame.pack(side='top', fill='y', expand=True)

    def make_timer_frame(self, height):
        timer_frame = ttk.Frame(self, height=height)
        try:
            duration = self.timer * 10
        except TypeError:
            duration = 1
        self.timer_bar = ttk.Progressbar(
            timer_frame, maximum=duration, value=duration * 10)
        self.timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return timer_frame

    def make_prog_frame(self, height):
        prog_frame = ttk.Frame(self, height=height)
        maximum, value = self.prog_bar_values
        prog_bar = ttk.Progressbar(prog_frame, maximum=maximum, value=value)
        prog_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return prog_frame

    def make_question_frame(self):
        question_frame = tk.Frame(self)
        for c in self.q_text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if c is not None:
                label = tk.Label(comp_frame, text=c)
                label.pack(padx=3, pady=3)
            else:
                self.entry = tk.Entry(comp_frame, width=2)
                self.entry.pack(padx=3, pady=3)
        self.entry.focus_set()
        return question_frame

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp_frame in self.question_frame.winfo_children():
            for widget in comp_frame.winfo_children():
                widget.config(font=("Arial", font_size))
        self.prog_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)

    def start_timer(self, on_timeup):
        if self.timer_bar['value'] <= 0:
            on_timeup()
            self.timer = False
        if self.timer:
            self.timer_bar['value'] -= 1
            self.after(100, lambda: self.start_timer(on_timeup))

    def on_failed(self):
        self.timer = False
        self.entry.delete(0, 'end')


class Olive:

    timer = None
    num_of_probs = None
    num_of_adds = 30
    num_of_subs = 30
    num_of_muls = 40
    add_opr_range = (2, 19)
    sub_opr_range = (2, 19)
    mul_opr_range = (1, 12)


class Clem:

    timer = None
    num_of_probs = None
    num_of_adds = 17
    num_of_subs = 17
    num_of_muls = 5
    add_range = (0, 9)
    sub_range = (0, 9)
    mul_range = (1, 2)


if __name__ == "__main__":

    User = Clem
    FlashCardsApp()


'''
class User:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(User, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_clem(self):
        self.timer = None
        self.num_of_probs = 40
        self.num_of_adds = None
        self.num_of_subs = None
        self.num_of_muls = 0
        self.add_opr_range = (0, 9)
        self.sub_opr_range = (0, 9)
        self.mul_opr_range = (0, 0)

    def set_olive(self):
        self.timer = None
        self.num_of_probs = None
        self.num_of_adds = 30
        self.num_of_subs = 30
        self.num_of_muls = 40
        self.add_opr_range = (2, 19)
        self.sub_opr_range = (2, 19)
        self.mul_opr_range = (1, 12)
'''
