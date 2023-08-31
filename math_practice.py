
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
        prob = random.choice(self.problems)
        prog_value = self.starting - self.remaining
        self.current_card = FlashCard(self, prob, self.starting, prog_value)
        self.current_card.entry.bind("<Return>", self.on_entered)
        self.current_card.entry.bind("<KP_Enter>", self.on_entered)
        self.current_card.pack(fill="both", expand=True)

    def on_failed(self):
        self.failed = True
        self.current_card.on_failed()

    def on_entered(self, event):
        try:
            answer = int(event.widget.get())
        except ValueError:
            return
        if answer == self.current_card.problem.answer:
            if not self.failed:
                self.problems.remove(self.current_card.problem)
                self.remaining = len(self.problems)
            self.failed = False
            if self.remaining > 0:
                self.next_flashcard()
            else:
                self.finished()
        else:
            self.on_failed()


class FlashCard(tk.Frame):

    def __init__(self, parent, prob, prog_max, prog_value):
        super().__init__(parent)
        self.problem = prob
        self.timer = User.timer
        self.font_size = None
        self.timer_frame, self.timer_bar = self.make_timer_bar()
        self.prog_frame = self.make_prog_bar(prog_max, prog_value)
        self.question_comps, self.entry = self.make_question()
        self.bind("<Configure>", self.resize_elements)
        self.start_timer()

    def make_question(self):
        question_frame = tk.Frame(self)
        question_frame.pack(side='top', fill='y', expand=True, padx=6, pady=6)
        question_comps = []
        for c in self.problem.question:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if c is not None:
                label = tk.Label(comp_frame, text=c)
                question_comps.append(label)
                label.pack(padx=3, pady=3)
            else:
                entry = tk.Entry(comp_frame, width=2)
                entry.pack(padx=3, pady=3)
                question_comps.append(entry)
        entry.focus_set()
        return question_comps, entry

    def make_prog_bar(self, maximum, value):
        prog_frame = ttk.Frame(self, height=30)
        prog_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        prog_bar = ttk.Progressbar(prog_frame, maximum=maximum, value=value)
        prog_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return prog_frame

    def make_timer_bar(self):
        timer_frame = ttk.Frame(self, height=30)
        timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        duration = User.timer or 1
        timer_bar = ttk.Progressbar(
            timer_frame, maximum=duration * 10, value=duration * 10)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return timer_frame, timer_bar

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        self.font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp in self.question_comps:
            comp.config(font=("Arial", self.font_size))
        self.prog_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)

    def start_timer(self):
        if self.timer_bar['value'] <= 0:
            self.master.event_generate("<<TimeUp>>", when='tail')
            self.timer = False
        if self.timer:
            self.timer_bar['value'] -= 1
            self.after(100, lambda: self.start_timer())

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

    timer = 10
    num_of_probs = 3
    num_of_adds = None
    num_of_subs = None
    num_of_muls = 0
    add_range = (0, 3)
    sub_range = (0, 3)
    mul_range = (0, 12)


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
